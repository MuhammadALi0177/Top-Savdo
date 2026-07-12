from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Order, Product, OrderItem
from .serializers import OrderCreateSerializer, OrderHistorySerializer, ProductSerializer
from accounts.models import CreditLimit
from django.contrib.auth import get_user_model
from django.db.models import Sum, F, DecimalField
from django.utils import timezone

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Product.objects.all()
        if user.role == 'DEALER':
            return Product.objects.filter(dealer=user)
        return Product.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            fallback_user = User.objects.filter(role='DEALER').first() or User.objects.first()
            serializer.save(dealer=fallback_user)
        else:
            serializer.save(dealer=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Order.objects.filter(client=user).order_by('-created_at')
        elif user.role == 'DEALER':
            return Order.objects.filter(dealer=user).order_by('-created_at')
        elif user.role == 'COURIER':
            return Order.objects.filter(courier=user).order_by('-created_at')
        return Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=False, methods=['post'], url_path='update_limit')
    def update_limit(self, request):
        user = request.user
        if user.role != 'DEALER':
            return Response({"message": "Faqat dilerlar limitni o'zgartira oladi!"}, status=status.HTTP_403_FORBIDDEN)
        new_limit = request.data.get('limit')
        if new_limit is None:
            return Response({"message": "Limit qiymati yuborilmadi!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
           CreditLimit.objects.filter(dealer=user).update(limit_amount=float(new_limit))
           clients = User.objects.filter(role='CLIENT')
        except Exception as e:
            return Response({"message": f"Xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='dealer_stats')
    def dealer_stats(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'DEALER':
            return Response({"message": "Faqat dilerlar statistikani ko'ra oladi!"}, status=status.HTTP_403_FORBIDDEN)

        now = timezone.now()

        # 🟢 YANGI: ?month=4&year=2026 orqali istalgan oy statistikasini tanlash
        # imkoniyati. Yubormasa, joriy oy ishlatiladi.
        try:
            selected_month = int(request.query_params.get('month', now.month))
            if selected_month < 1 or selected_month > 12:
                raise ValueError
        except (TypeError, ValueError):
            selected_month = now.month

        try:
            selected_year = int(request.query_params.get('year', now.year))
        except (TypeError, ValueError):
            selected_year = now.year

        def calc(qs):
            agg = qs.aggregate(
                revenue=Sum(F('price_at_order') * F('quantity'), output_field=DecimalField(max_digits=14, decimal_places=2)),
                cost=Sum(F('product__cost_price') * F('quantity'), output_field=DecimalField(max_digits=14, decimal_places=2)),
            )
            revenue = agg['revenue'] or 0
            cost = agg['cost'] or 0
            return revenue, cost, revenue - cost

        base_qs = OrderItem.objects.filter(order__dealer=user, order__status='DELIVERED')
        total_sales, total_cost, total_profit = calc(base_qs)
        monthly_qs = base_qs.filter(order__created_at__year=selected_year, order__created_at__month=selected_month)
        monthly_sales, monthly_cost, monthly_profit = calc(monthly_qs)
        total_orders_count = Order.objects.filter(dealer=user, status='DELIVERED').count()
        monthly_orders_count = Order.objects.filter(
            dealer=user, status='DELIVERED',
            created_at__year=selected_year, created_at__month=selected_month,
        ).count()

        return Response({
            "selected_month": selected_month,
            "selected_year": selected_year,
            "monthly_sales": monthly_sales,
            "monthly_cost": monthly_cost,
            "monthly_profit": monthly_profit,
            "monthly_orders_count": monthly_orders_count,
            "total_sales": total_sales,
            "total_cost": total_cost,
            "total_profit": total_profit,
            "total_orders_count": total_orders_count,
        })

    @action(detail=False, methods=['get'], url_path='my_clients')
    def my_clients(self, request):
        user = request.user
        if user.role != 'DEALER':
            return Response({"message": "Faqat dilerlar bu ro'yxatni ko'ra oladi!"}, status=status.HTTP_403_FORBIDDEN)
        clients = User.objects.filter(role='CLIENT').select_related('client_profile')
        data = []
        for client in clients:
            limit_obj = CreditLimit.objects.filter(dealer=user, client=client).first()
            store_name = getattr(getattr(client, 'client_profile', None), 'store_name', None) or client.phone_number
            data.append({
                "id": client.id,
                "store_name": store_name,
                "phone_number": client.phone_number,
                "limit_amount": limit_obj.limit_amount if limit_obj else 0,
                "current_debt": limit_obj.current_debt if limit_obj else 0,
            })
        return Response(data)

    @action(detail=False, methods=['post'], url_path='set_client_limit')
    def set_client_limit(self, request):
        user = request.user
        if user.role != 'DEALER':
            return Response({"message": "Faqat dilerlar limit belgilay oladi!"}, status=status.HTTP_403_FORBIDDEN)
        client_id = request.data.get('client_id')
        new_limit = request.data.get('limit')
        if not client_id or new_limit is None:
            return Response({"message": "Magazinchi va limit qiymati yuborilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            client = User.objects.get(id=client_id, role='CLIENT')
        except User.DoesNotExist:
            return Response({"message": "Bunday magazinchi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
        try:
            new_limit = float(new_limit)
            if new_limit < 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({"message": "Limit musbat son bo'lishi shart!"}, status=status.HTTP_400_BAD_REQUEST)
        limit_obj, created = CreditLimit.objects.get_or_create(
            dealer=user, client=client, defaults={'limit_amount': new_limit}
        )
        if not created:
            limit_obj.limit_amount = new_limit
            limit_obj.save()
        store_name = getattr(getattr(client, 'client_profile', None), 'store_name', None) or client.phone_number
        return Response({"message": f"{store_name} uchun limit muvaffaqiyatli yangilandi!"})

    # 🟢 YANGI: Diler magazinchining qarzini kamaytiradi yoki to'liq nolga tushiradi
    @action(detail=False, methods=['post'], url_path='reduce_client_debt')
    def reduce_client_debt(self, request):
        user = request.user
        if user.role != 'DEALER':
            return Response({"message": "Faqat dilerlar qarzni o'zgartira oladi!"}, status=status.HTTP_403_FORBIDDEN)

        client_id = request.data.get('client_id')
        clear_all = request.data.get('clear', False)
        amount = request.data.get('amount')

        if not client_id:
            return Response({"message": "Magazinchi tanlanishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = User.objects.get(id=client_id, role='CLIENT')
        except User.DoesNotExist:
            return Response({"message": "Bunday magazinchi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        try:
            limit_obj = CreditLimit.objects.get(dealer=user, client=client)
        except CreditLimit.DoesNotExist:
            return Response({"message": "Bu magazinchi uchun limit/qarz topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        store_name = getattr(getattr(client, 'client_profile', None), 'store_name', None) or client.phone_number

        if clear_all:
            limit_obj.current_debt = 0
            limit_obj.save()
            return Response({
                "message": f"{store_name} ning qarzi to'liq yopildi (0 so'm).",
                "current_debt": limit_obj.current_debt,
            })

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({"message": "Kamaytirish summasi musbat son bo'lishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

        new_debt = float(limit_obj.current_debt) - amount
        if new_debt < 0:
            new_debt = 0
        limit_obj.current_debt = new_debt
        limit_obj.save()
        return Response({
            "message": f"{store_name} ning qarzi {amount} so'mga kamaytirildi. Qolgan qarz: {new_debt} so'm.",
            "current_debt": limit_obj.current_debt,
        })

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_order(self, request, pk=None):
        order = self.get_object()
        if request.user.role != 'DEALER' or order.dealer != request.user:
            return Response({"message": "Ruxsat berilmagan!"}, status=status.HTTP_403_FORBIDDEN)
        if order.status != 'PENDING':
            return Response({"message": "Bu buyurtmani tasdiqlab bo'lmaydi!"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'ACCEPTED'
        order.save()
        return Response({"message": "Buyurtma diler tomonidan tasdiqlandi va tayyorlanmoqda."})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.client != request.user and order.dealer != request.user:
            return Response({"message": "Ruxsat berilmagan!"}, status=status.HTTP_403_FORBIDDEN)
        if order.status in ['SHIPPED', 'DELIVERED', 'CANCELED']:
            return Response({"message": "Yuk yo'lga chiqib bo'lgan yoki bekor qilingan!"}, status=status.HTTP_400_BAD_REQUEST)
        if order.debt_amount > 0:
            try:
                limit_obj = CreditLimit.objects.get(dealer=order.dealer, client=order.client)
                limit_obj.current_debt -= order.debt_amount
                limit_obj.save()
            except CreditLimit.DoesNotExist:
                pass
        order.status = 'CANCELED'
        order.save()
        return Response({"message": "Buyurtma muvaffaqiyatli bekor qilindi, qarzlar qayta hisoblandi."})

    @action(detail=True, methods=['post'], url_path='request-courier')
    def request_courier(self, request, pk=None):
        order = self.get_object()
        if order.dealer != request.user or order.status != 'ACCEPTED':
            return Response({"message": "Noto'g'ri buyurtma holati yoki ruxsat yo'q!"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'COURIER_REQUESTED'
        order.save()
        return Response({"message": "Kuryerlarga buyurtma haqida so'rov yuborildi."})

    # 🟢🟢🟢 YANGI: Kuryer hali hech kim olmagan buyurtmalarni ko'radi
    @action(detail=False, methods=['get'], url_path='available_deliveries')
    def available_deliveries(self, request):
        user = request.user
        if user.role != 'COURIER':
            return Response({"message": "Faqat kuryerlar bu ro'yxatni ko'ra oladi!"}, status=status.HTTP_403_FORBIDDEN)
        qs = Order.objects.filter(status='COURIER_REQUESTED', courier__isnull=True).order_by('-created_at')
        serializer = OrderHistorySerializer(qs, many=True)
        return Response(serializer.data)

    # 🟢🟢🟢 YANGI: Kuryer buyurtmani o'ziga biriktirib oladi
    @action(detail=True, methods=['post'], url_path='accept-delivery')
    def accept_delivery(self, request, pk=None):
        user = request.user
        if user.role != 'COURIER':
            return Response({"message": "Faqat kuryerlar buyurtmani qabul qila oladi!"}, status=status.HTTP_403_FORBIDDEN)

        order = Order.objects.filter(pk=pk).first()
        if order is None:
            return Response({"message": "Bunday buyurtma topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != 'COURIER_REQUESTED' or order.courier_id is not None:
            return Response({"message": "Bu buyurtma allaqachon boshqa kuryer tomonidan olingan yoki hozircha mavjud emas!"}, status=status.HTTP_400_BAD_REQUEST)

        order.courier = user
        order.save()
        return Response({"message": "Buyurtma sizga muvaffaqiyatli biriktirildi! Endi diler yukni sizga topshiradi."})

    @action(detail=True, methods=['post'], url_path='ship')
    def ship_order(self, request, pk=None):
        order = self.get_object()
        if order.dealer != request.user or order.status != 'COURIER_REQUESTED':
            return Response({"message": "Avval kuryer chaqirilishi kerak!"}, status=status.HTTP_400_BAD_REQUEST)
        courier_id = request.data.get('courier_id')
        if not courier_id:
            return Response({"message": "Yukni qaysi kuryer olganini ko'rsating!"}, status=status.HTTP_400_BAD_REQUEST)
        order.courier_id = courier_id
        order.status = 'SHIPPED'
        order.save()
        return Response({"message": "Yuk kuryerga berildi. Magazinshiga 'Yuk yo'lda' xabarnomasi ketdi."})

    @action(detail=True, methods=['post'], url_path='deliver')
    def deliver_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'SHIPPED':
            return Response({"message": "Bu yuk hali yo'lga chiqmagan!"}, status=status.HTTP_400_BAD_REQUEST)

        # 🟢 YANGI: faqat shu buyurtmaga biriktirilgan kuryer yopa oladi
        if request.user.role == 'COURIER' and order.courier_id != request.user.id:
            return Response({"message": "Bu buyurtma sizga biriktirilmagan!"}, status=status.HTTP_403_FORBIDDEN)

        order.status = 'DELIVERED'
        order.save()
        return Response({"message": "Buyurtma magazinshiga yetkazildi va muvaffaqiyatli yopildi!"})
    

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]