import json
from django.shortcuts import render
from django.db.models import ProtectedError
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from django.utils import timezone
from .models import Category, Brand, Product, BundleItem
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CategorySerializer, BrandSerializer, ProductCreateSerializer, ProductListSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Hamma uchun ruxsat berish (yaratish, o'chirish, tahrirlash)
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    
    # 🟢 BU QATOR MUAMMONI HAL QILADI:
    # Django fayllarni (multipart) qabul qilishi uchun bu parserlar kerak.
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductListSerializer 

    def get_queryset(self):
        user = self.request.user
        # 🟢 Diler faqat o'z mahsulotlarini ko'radi (Mening mahsulotlarim bo'limi uchun).
        # Boshqa rollar (admin, magazinchi) hammasini ko'radi.
        if user.is_authenticated and getattr(user, 'role', None) == 'DEALER':
            qs = Product.objects.filter(dealer=user)
        else:
            qs = Product.objects.all()

        # 🟢 YANGI: ?is_bundle=true/false parametri orqali "Mening Omborim" (oddiy
        # mahsulotlar) va "Savat yaratish" (to'plamlar) bo'limlarini ajratib olamiz.
        is_bundle_param = self.request.query_params.get('is_bundle')
        if is_bundle_param is not None:
            wants_bundle = is_bundle_param.lower() in ('1', 'true', 'yes')
            qs = qs.filter(is_bundle=wants_bundle)

        # 🟢 MUAMMONI TUZATADI: "o'chirilgan" (aslida buyurtmalarda ishlatilgani
        # uchun faqat is_active=False qilingan) mahsulotlar dilerning "Mening
        # mahsulotlarim" ro'yxatida ko'rinishda davom etardi — go'yo o'chirish
        # ishlamagandek tuyulardi. Endi standart holatda ular ro'yxatdan
        # yashiriladi. Kerak bo'lsa ?include_inactive=true bilan ko'rish mumkin.
        include_inactive = self.request.query_params.get('include_inactive')
        if include_inactive is None or include_inactive.lower() not in ('1', 'true', 'yes'):
            qs = qs.filter(is_active=True)
        return qs

    def destroy(self, request, *args, **kwargs):
        # 🟢 MUAMMONI TUZATADI: agar mahsulot (yoki savat) avval biror
        # buyurtmada ishlatilgan bo'lsa, OrderItem.product `on_delete=PROTECT`
        # bo'lgani uchun Django uni o'chirishga yo'l qo'ymaydi va ProtectedError
        # tashlaydi. DRF buni avtomatik ushlamagani sababli frontendga 500
        # (Internal Server Error) qaytib, "DELETE .../products/15/ 500" xatosi
        # chiqayotgan edi. Endi bu holatni ushlab, tushunarli 400 xato va
        # o'chirish o'rniga mahsulotni faolsizlantirish (soft-delete) imkonini
        # beramiz — buyurtma tarixi buzilmaydi.
        instance = self.get_object()
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            instance.is_active = False
            instance.save(update_fields=['is_active'])
            return Response(
                {
                    "message": (
                        "Bu mahsulot avval buyurtmalarda ishlatilgan, shuning uchun "
                        "uni butunlay o'chirib bo'lmaydi. U katalogdan yashirildi "
                        "(faolsizlantirildi)."
                    )
                },
                status=status.HTTP_200_OK,
            )

    def perform_create(self, serializer):
        # 🟢 MUAMMONI TUZATADI: yangi mahsulot yaratilganda uni so'rov yuborgan
        # dilerga avtomatik bog'laymiz. Aynan shu maydon yo'qligi sabab
        # buyurtma berishda "dealer" aniqlanmay, 400 xato chiqayotgan edi.
        user = self.request.user
        if user.is_authenticated and getattr(user, 'role', None) == 'DEALER':
            serializer.save(dealer=user)
        else:
            # Fallback: agar boshqa rol (masalan admin) mahsulot qo'shsa,
            # bazadagi birinchi dilerga bog'lab qo'yamiz — bo'sh qolib ketmasin.
            from django.contrib.auth import get_user_model
            User = get_user_model()
            fallback_dealer = User.objects.filter(role='DEALER').first()
            serializer.save(dealer=fallback_dealer)

    # 🟢 YANGI: "Savat yaratish" — diler o'zining bir nechta mahsulotini bitta
    # to'plam (savat) qilib birlashtiradi, unga alohida nom, rasm va narx qo'yadi.
    # Yaratilgan savat oddiy Product sifatida saqlanadi (is_bundle=True), shu sababli
    # u avtomatik ravishda katalogga, buyurtma tizimiga va statistikaga qo'shiladi —
    # magazinchiga xuddi oddiy mahsulot kabi ko'rinadi va sotiladi.
    @action(detail=False, methods=['post'], url_path='create_bundle')
    def create_bundle(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'DEALER':
            return Response({"message": "Faqat dilerlar savat yarata oladi!"}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        price = request.data.get('price')
        stock = request.data.get('stock')
        image = request.data.get('image')
        description = request.data.get('description', '')
        items_raw = request.data.get('items')

        if not name or price is None or stock is None or not items_raw:
            return Response(
                {"message": "Savat nomi, narxi, soni va tarkibi to'ldirilishi shart!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            items = json.loads(items_raw)
        except (TypeError, ValueError):
            return Response({"message": "Savat tarkibi noto'g'ri formatda yuborildi!"}, status=status.HTTP_400_BAD_REQUEST)

        if not items:
            return Response({"message": "Savatga kamida bitta mahsulot qo'shing!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            price = float(price)
            stock = int(stock)
            if price < 0 or stock < 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({"message": "Narx va son musbat son bo'lishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

        # 🟢 Faqat dilerning o'ziga tegishli, savat bo'lmagan mahsulotlar tanlanishi mumkin.
        own_products = {
            p.id: p for p in Product.objects.filter(dealer=user, is_bundle=False)
        }

        validated_items = []
        cost_price_total = 0
        for it in items:
            try:
                product_id = int(it.get('product_id'))
                quantity = int(it.get('quantity'))
            except (TypeError, ValueError, AttributeError):
                return Response({"message": "Savat tarkibida noto'g'ri mahsulot ma'lumoti bor!"}, status=status.HTTP_400_BAD_REQUEST)

            product = own_products.get(product_id)
            if product is None or quantity <= 0:
                return Response(
                    {"message": "Savat tarkibida faqat sizga tegishli mahsulotlar va musbat son bo'lishi kerak!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cost_price_total += float(product.cost_price) * quantity
            validated_items.append((product, quantity))

        # 🟢 Savatlar uchun alohida umumiy kategoriya (dealer kategoriya tanlashi shart emas).
        savat_category, _ = Category.objects.get_or_create(
            slug='savatlar-toplamlar',
            defaults={'name': "Savatlar / To'plamlar"},
        )

        bundle = Product.objects.create(
            dealer=user,
            category=savat_category,
            name=name,
            sku=f"SAVAT-{user.id}-{int(timezone.now().timestamp())}",
            price=price,
            cost_price=cost_price_total,
            stock=stock,
            image=image if image else None,
            description=description or "",
            is_bundle=True,
        )

        BundleItem.objects.bulk_create([
            BundleItem(bundle=bundle, component=product, quantity=quantity)
            for product, quantity in validated_items
        ])

        serializer = ProductListSerializer(bundle, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    # 🟢 Ro'yxatdan o'tmagan mehmonlar ham (Landing sahifada) katalogni ko'ra olishi uchun ochiq.
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand', 'dealer', 'dealer__dealer_profile')
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    # Filtrlash va Qidiruv sozlamalari
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'dealer'] # /api/catalog/?dealer=3
    search_fields = ['name', 'sku', 'description'] # /api/catalog/?search=cola
    ordering_fields = ['price', 'created_at'] # /api/catalog/?ordering=-price