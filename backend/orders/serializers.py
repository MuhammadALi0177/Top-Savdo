from rest_framework import serializers
from .models import Order, OrderItem, Product
from accounts.models import CreditLimit
from django.db.models import Sum # Jami savdoni hisoblash uchun kerak
from django.contrib.auth import get_user_model

# 🟢 User bu yerda ham kerak (OrderCreateSerializer ichida dealer maydoni uchun)
User = get_user_model()

# 1. Mahsulotlar uchun oddiy serializer
class ProductSerializer(serializers.ModelSerializer):
    # dealer_company yoki shunga o'xshash diler maydoni bo'lsa, unga read_only=True beramiz
    class Meta:
        model = Product
        fields = '__all__' # yoki hamma maydonlar ro'yxati
        # ENGI MUHIM QATOR: Dilerni majburiy maydonlar ro'yxatidan chiqaramiz
        read_only_fields = ['dealer']


# 2. Tarixni ko'rayotganda ichki mahsulotlar nomi ko'rinishi uchun serializer
class OrderItemDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'price_at_order']


# 3. ASOSIY TARIX SERIALIZERI (Tarixni ko'rish va moliyaviy holatni chiqarish uchun)
class OrderHistorySerializer(serializers.ModelSerializer):
    # Id raqamlar o'rniga foydalanuvchilarga tushunarli nomlarni bog'laymiz
    client_store_name = serializers.CharField(source='client.client_profile.store_name', read_only=True)
    client_address = serializers.CharField(source='client.client_profile.address', read_only=True, default=None)
    client_phone = serializers.CharField(source='client.phone_number', read_only=True, default=None)
    dealer_company_name = serializers.CharField(source='dealer.dealer_profile.company_name', read_only=True)
    dealer_phone = serializers.CharField(source='dealer.phone_number', read_only=True, default=None)
    courier_name = serializers.CharField(source='courier.username', read_only=True, default="Tayyinlanmagan")
    courier_phone = serializers.CharField(source='courier.phone_number', read_only=True, default=None)
    courier_id = serializers.IntegerField(source='courier.id', read_only=True, default=None)

    # 🟢 YANGI QO'SHILGAN MOLIYAVIY MAYDONLAR:
    client_credit_limit = serializers.SerializerMethodField()
    client_current_debt = serializers.SerializerMethodField()
    client_total_purchased = serializers.SerializerMethodField()

    # Buyurtma ichidagi barcha mahsulotlar ro'yxati
    items = OrderItemDetailSerializer(many=True, read_only=True)
    
    # Statusning odam tushunadigan o'zbekcha matni
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'client_store_name', 'client_address', 'client_phone',
            'dealer_company_name', 'dealer_phone',
            'courier_name', 'courier_phone', 'courier_id',
            'status', 'status_display', 'total_amount', 'paid_amount', 
            'debt_amount', 'items', 'created_at',
            'client_credit_limit', 'client_current_debt', 'client_total_purchased' # <--- bularni fields'ga qo'shdik
        ]

    def get_client_credit_limit(self, obj):
        """ Magazinchining ushbu diler oldidagi umumiy qarz limiti """
        limit = CreditLimit.objects.filter(dealer=obj.dealer, client=obj.client).first()
        return limit.limit_amount if limit else 0

    def get_client_current_debt(self, obj):
        """ Magazinchining ushbu dilerdan ayni vaqtdagi joriy qarzi """
        limit = CreditLimit.objects.filter(dealer=obj.dealer, client=obj.client).first()
        return limit.current_debt if limit else 0

    def get_client_total_purchased(self, obj):
        """ Magazinchining shu dilerdan shu vaqtgacha jami sotib olgan tavarlari summasi """
        # Faqat DELIVERED (Etkazib berilgan) buyurtmalar hisoblanadi (otmen bo'lganlari qo'shilmaydi)
        total = Order.objects.filter(
            client=obj.client,
            dealer=obj.dealer,
            status='DELIVERED'
        ).aggregate(sum_amount=Sum('total_amount'))['sum_amount']
        
        return total if total else 0


# 4. BUYURTMA BERISH SERIALIZERI (Faqat magazinchi zakaz berayotganda ishlaydi)
class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_order']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    dealer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='DEALER'),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Order
        fields = ['id', 'client', 'dealer', 'paid_amount', 'items', 'total_amount']
        read_only_fields = ['id', 'client', 'total_amount']

    def validate(self, data):
        request = self.context.get('request')
        client = request.user

        items = data['items']
        if not items:
            raise serializers.ValidationError("Savatda hech qanday mahsulot yo'q!")

        dealer = data.get('dealer')
        if not dealer:
            dealer = items[0]['product'].dealer
            if not dealer:
                raise serializers.ValidationError(
                    "Bu mahsulotga diler biriktirilmagan, buyurtma berib bo'lmaydi!"
                )
        data['dealer'] = dealer
        data['client'] = client

        paid_amount = data['paid_amount']
        total_amount = sum(item['quantity'] * item['price_at_order'] for item in items)
        
        if paid_amount > total_amount:
            raise serializers.ValidationError("To'langan summa umumiy summadan ko'p bo'lishi mumkin emas!")

        debt_amount = total_amount - paid_amount

        if debt_amount > 0:
            try:
                limit_obj = CreditLimit.objects.get(dealer=dealer, client=client)
                if limit_obj.current_debt + debt_amount > limit_obj.limit_amount:
                    raise serializers.ValidationError(
                        f"Qarz limiti yetarli emas! Mavjud qarz: {limit_obj.current_debt} so'm, "
                        f"Yangi qarz: {debt_amount} so'm, Limit: {limit_obj.limit_amount} so'm."
                    )
            except CreditLimit.DoesNotExist:
                raise serializers.ValidationError("Ushbu diler magazinshiga qarzga mol berish uchun limit ajratmagan!")

        data['total_amount'] = total_amount
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            product = item_data['product']
            product.stock -= item_data['quantity']
            product.save()

        if order.debt_amount > 0:
            limit_obj = CreditLimit.objects.get(dealer=order.dealer, client=order.client)
            limit_obj.current_debt += order.debt_amount
            limit_obj.save()

        return order


# =========================================================================
# 🟢 ADMIN PANEL FOYDALANUVCHILARI VA FERMALAR UCHUN JADID SIZ CHIQARGAN QATORLAR:
# =========================================================================
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdminListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='dealer_profile.company_name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'role', 'company_name']