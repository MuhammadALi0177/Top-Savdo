from rest_framework import serializers
from .models import Category, Brand, Product, BundleItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']
        # Agar image yuklamoqchi bo'lmasangiz, quyidagini qo'shib qo'ying:
        extra_kwargs = {
            'image': {'required': False},
            'slug': {'required': False} # Test uchun
        }

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']

# products/serializers.py
class ProductCreateSerializer(serializers.ModelSerializer):
    # Aniq ImageField ekanligini ko'rsatamiz
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        # 🟢 'dealer' shu yerga qo'shilmaydi — u view ichida (perform_create)
        # avtomatik so'rov yuborgan foydalanuvchidan olinadi, frontend uni yubormaydi.
        # 🟢 'cost_price' qo'shildi: diler mahsulot qo'shayotganda tan narxini ham kiritadi.
        # 🟢 'description' qo'shildi: diler mahsulot haqida batafsil ma'lumot (tavsif) kiritishi uchun.
        fields = ['name', 'sku', 'price', 'cost_price', 'stock', 'category', 'image', 'description']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
        }

class BundleComponentSerializer(serializers.ModelSerializer):
    """🟢 YANGI: Savat ichidagi bitta mahsulot qatorini chiqaradi (nom, rasm, narx, soni)."""
    product_id = serializers.IntegerField(source='component.id', read_only=True)
    name = serializers.CharField(source='component.name', read_only=True)
    image = serializers.ImageField(source='component.image', read_only=True)
    price = serializers.DecimalField(source='component.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BundleItem
        fields = ['id', 'product_id', 'name', 'image', 'price', 'quantity']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    # 🟢 Landing sahifada "Barcha mahsulotlar" ro'yxatida qaysi dilerga
    # tegishli ekanini ko'rsatish uchun.
    dealer_company_name = serializers.CharField(source='dealer.dealer_profile.company_name', read_only=True, default=None)

    # 🟢 YANGI: Tan narxi va birlik foydasi — BU MAYDONLAR FAQAT MAHSULOT EGASI
    # BO'LGAN DILERGA CHIQARILADI. Magazinchi (client) yoki boshqa dilerlar uchun
    # bu maydonlar har doim `null` bo'lib qaytadi — ular hech qachon tan narxini ko'rmaydi.
    cost_price = serializers.SerializerMethodField()
    profit_per_unit = serializers.SerializerMethodField()

    # 🟢 YANGI: Savat (to'plam) bo'lsa, uning tarkibidagi mahsulotlar ro'yxati.
    components = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # 🟢 'dealer' qo'shildi: frontend buyurtma berayotganda mahsulot
        # qaysi dilerga tegishli ekanligini shu maydondan biladi.
        fields = [
            'id', 'name', 'sku', 'price', 'stock', 'category', 'category_name', 'brand_name',
            'image', 'dealer', 'dealer_company_name', 'cost_price', 'profit_per_unit',
            'is_bundle', 'components',
            # 🟢 'description' qo'shildi: mahsulot "Batafsil" (detail) sahifasida
            # to'liq tavsifni ko'rsatish uchun.
            'description',
        ]

    def _is_owner_dealer(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return bool(
            user and user.is_authenticated
            and getattr(user, 'role', None) == 'DEALER'
            and obj.dealer_id == user.id
        )

    def get_cost_price(self, obj):
        if self._is_owner_dealer(obj):
            return obj.cost_price
        return None

    def get_profit_per_unit(self, obj):
        if self._is_owner_dealer(obj):
            return obj.price - obj.cost_price
        return None

    def get_components(self, obj):
        if not obj.is_bundle:
            return []
        items = obj.bundle_components.select_related('component')
        return BundleComponentSerializer(items, many=True, context=self.context).data