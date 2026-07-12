from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin / Ta\'sischi Admin'),
        ('MANAGER', 'Ta\'sischi Menejer'),
        ('DEALER', 'Diler (Sotuvchi/Yetkazib beruvchi)'),
        ('CLIENT', 'Magazinchi (Mijoz / Client)'),
        ('COURIER', 'Kuryer (Yetkazib beruvchi)'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    phone_number = models.CharField(max_length=15, unique=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.phone_number} - {self.get_role_display()}"
    
    
class DealerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dealer_profile')
    company_name = models.CharField(max_length=255, verbose_name="Firma / Korxona nomi")

    def __str__(self):
        return self.company_name    
    
    
class ClientProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    store_name = models.CharField(max_length=255, verbose_name="Do'kon nomi")
    address = models.TextField(verbose_name="Yetkazib berish manzili")    

    def __str__(self):
        return self.store_name
    
    
class CreditLimit(models.Model):

    dealer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_limits', verbose_name="Diler")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dealer_limits', verbose_name="Magazinchi (Mijoz)")
    
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Ajratilgan Qarz Limiti")
    
    current_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Joriy Qarzdorlik")

    class Meta:
        # Bir diler muayyan bir magazinchiga faqat bitta limit ajrata oladi, takrorlanishi mumkin emas
        unique_together = ('dealer', 'client')

    def __str__(self):
        return f"{self.dealer.dealer_profile.company_name} -> {self.client.client_profile.store_name}: Limit {self.limit_amount}"   
    
    
class CourierProfile(models.Model):

    TRANSPORT_CHOICES = (
        ('CAR', 'Mashina'),
        ('MOTO', 'Motoroller / Skuter'),
        ('BIKE', 'Velosiped'),
        ('FOOT', 'Piyoda'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courier_profile')
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_CHOICES, default='CAR', verbose_name="Transport turi")
    
    # Kuryer hozir buyurtma olishga tayyormi yoki yo'qmi (Band/Bo'sh)
    is_available = models.BooleanField(default=True, verbose_name="Hozir bo'sh (Ishga tayyor)")

    def __str__(self):
        return f"Kuryer: {self.user.phone_number} ({self.get_transport_type_display()})"