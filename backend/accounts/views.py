from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.db.models import Count, Q as models_Q
from .models import DealerProfile, ClientProfile, CourierProfile
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny # 🟢 Import qo'shildi

User = get_user_model()

# =========================================================================
# Serializer
# =========================================================================
class UserAdminSerializer(ModelSerializer):
    company_name = serializers.CharField(source='dealer_profile.company_name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'role', 'date_joined', 'is_active', 'company_name']

# =========================================================================
# Admin List View
# =========================================================================
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return Response(
            {"error": "Sizda bu sahifani ko'rish uchun huquq yo'q!"}, 
            status=status.HTTP_403_FORBIDDEN
        )

# =========================================================================
# 🟢 Public Dealer List: Landing sahifada, ro'yxatdan o'tmagan mehmonlar
# ham dilerlar ro'yxatini va ularning mahsulot sonini ko'rishi uchun.
# =========================================================================
class PublicDealerSerializer(ModelSerializer):
    company_name = serializers.CharField(source='dealer_profile.company_name', read_only=True, default=None)
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        # 🟢 'date_joined' qo'shildi: Landing sahifada diler "qachon beri ishlayapti"
        # (masalan, "8 oydan beri faoliyatda") degan ma'lumotni ko'rsatish uchun.
        fields = ['id', 'company_name', 'phone_number', 'products_count', 'date_joined']


class PublicDealerListView(generics.ListAPIView):
    """ Hammaga ochiq: faol dilerlar ro'yxati (login talab qilinmaydi). """
    serializer_class = PublicDealerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            User.objects.filter(role='DEALER', is_active=True, dealer_profile__isnull=False)
            .select_related('dealer_profile')
            .annotate(products_count=Count('products', filter=models_Q(products__is_active=True)))
            .order_by('dealer_profile__company_name')
        )


# 🟢 Bitta dilerning batafsil (detail) sahifasi uchun: hammaga ochiq.
class PublicDealerDetailView(generics.RetrieveAPIView):
    """ Hammaga ochiq: bitta dilerning batafsil ma'lumoti (login talab qilinmaydi). """
    serializer_class = PublicDealerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            User.objects.filter(role='DEALER', is_active=True, dealer_profile__isnull=False)
            .select_related('dealer_profile')
            .annotate(products_count=Count('products', filter=models_Q(products__is_active=True)))
        )


# =========================================================================
# Login View
# =========================================================================
class CustomAuthToken(APIView):
    permission_classes = [AllowAny] # Login ham hammaga ochiq bo'lishi kerak

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response({"error": "Telefon raqam va parol kiritilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                user_role = user.role
                if user.is_superuser or user.is_staff:
                    user_role = 'ADMIN'
                elif not user_role:
                    user_role = 'CLIENT'

                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'role': user_role 
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Telefon raqam yoki parol xato!"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Telefon raqam yoki parol xato!"}, status=status.HTTP_400_BAD_REQUEST)

# =========================================================================
# 🟢 Signup View (TO'G'IRLANGAN)
# =========================================================================
class SignupView(APIView):
    permission_classes = [AllowAny] # 🟢 BU QATOR MUAMMONI HAL QILADI

    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = data.get('phone_number')
        password = data.get('password')
        role = data.get('role')

        if not phone_number or not password or not role:
            return Response({"error": "Barcha maydonlarni to'ldirish shart!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Bu telefon raqami allaqachon ro'yxatdan o'tgan!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=phone_number,
                phone_number=phone_number,
                password=password,
                role=role
            )

            if role == 'DEALER':
                company_name = data.get('company_name', 'Noma\'lum Firma')
                DealerProfile.objects.create(user=user, company_name=company_name)
            elif role == 'CLIENT':
                store_name = data.get('store_name', 'Noma\'lum Do\'kon')
                address = data.get('address', 'Kiritilmagan')
                ClientProfile.objects.create(user=user, store_name=store_name, address=address)
            elif role == 'COURIER':
                transport_type = data.get('transport_type', 'CAR')
                valid_transport = dict(CourierProfile.TRANSPORT_CHOICES)
                if transport_type not in valid_transport:
                    transport_type = 'CAR'
                CourierProfile.objects.create(user=user, transport_type=transport_type)

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
                'token': token.key,
                'user_id': user.pk,
                'role': user.role
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================================
# 🟢 Kuryer profili: o'zining holatini (bo'sh/band) va transport turini
# ko'rish hamda "Ishga tayyorman / Bandman" holatini almashtirish uchun.
# =========================================================================
class CourierMeView(APIView):
    """ Kuryerning o'z profilini ko'rishi (GET) va holatini yangilashi (PATCH) """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'COURIER':
            return Response({"error": "Faqat kuryerlar uchun!"}, status=status.HTTP_403_FORBIDDEN)

        profile, _ = CourierProfile.objects.get_or_create(user=request.user)
        return Response({
            "id": request.user.id,
            "phone_number": request.user.phone_number,
            "transport_type": profile.transport_type,
            "transport_type_display": profile.get_transport_type_display(),
            "is_available": profile.is_available,
        })

    def patch(self, request):
        if request.user.role != 'COURIER':
            return Response({"error": "Faqat kuryerlar uchun!"}, status=status.HTTP_403_FORBIDDEN)

        profile, _ = CourierProfile.objects.get_or_create(user=request.user)

        def to_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.strip().lower() in ('true', '1', 'yes')
            return bool(val)

        if 'is_available' in request.data:
            profile.is_available = to_bool(request.data.get('is_available'))
        if 'transport_type' in request.data:
            valid_transport = dict(CourierProfile.TRANSPORT_CHOICES)
            new_transport = request.data.get('transport_type')
            if new_transport in valid_transport:
                profile.transport_type = new_transport

        profile.save()
        return Response({
            "message": "Holat muvaffaqiyatli yangilandi!",
            "is_available": profile.is_available,
            "transport_type": profile.transport_type,
        })