from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomAuthToken, SignupView, AdminUserListView, AdminUserDeleteView, CourierMeView, PublicDealerListView, PublicDealerDetailView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/login/', CustomAuthToken.as_view(), name='api_token_auth'), 
    path('api/v1/signup/', SignupView.as_view(), name='api_signup'),
    
    path('api/v1/admin/users/', AdminUserListView.as_view(), name='admin_users_list'),
    path('api/v1/admin/users/<int:pk>/', AdminUserDeleteView.as_view(), name='admin_users_delete'),

    # 🟢 Landing sahifa uchun: hech kim login qilmasdan dilerlar ro'yxatini ko'ra oladi
    path('api/v1/public/dealers/', PublicDealerListView.as_view(), name='public_dealers_list'),

    # 🟢 Bitta dilerning "Batafsil" (detail) sahifasi uchun: hammaga ochiq
    path('api/v1/public/dealers/<int:pk>/', PublicDealerDetailView.as_view(), name='public_dealer_detail'),

    # 🟢 Kuryerning o'z profili (holat: bo'sh/band, transport turi)
    path('api/v1/courier/me/', CourierMeView.as_view(), name='courier_me'),
    
    path('api/v1/', include('orders.urls')),
    
    # 🟢 BU YERNI O'ZGARTIRDIK: endi u ham v1 prefiksi ostida ishlaydi!
    path('api/v1/', include('products.urls')),

] 

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]