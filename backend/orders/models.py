from django.db import models
from django.contrib.auth import get_user_model
# Yangi yaratilgan products ilovasidan tayyor mukammal Product modelini chaqiramiz:
from products.models import Product 

User = get_user_model()

class Order(models.Model):
    """
    Asosiy Buyurtma jadvali (Savdo shartnomasi boshi).
    """
    STATUS_CHOICES = (
        ('PENDING', 'Kutilmoqda (Magazinchi buyurtma berdi)'),
        ('ACCEPTED', 'Tasdiqlandi (Diler qadoqlayapti)'),
        ('COURIER_REQUESTED', 'Kuryerga so\'rov yuborildi'),
        ('SHIPPED', 'Yo\'lda (Kuryer yukni oldi)'),
        ('DELIVERED', 'Yetkazib berildi (Yopildi)'),
        ('CANCELED', 'Bekor qilindi'),
    )
    
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='client_orders', limit_choices_to={'role': 'CLIENT'})
    dealer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='dealer_orders', limit_choices_to={'role': 'DEALER'})
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='courier_orders', limit_choices_to={'role': 'COURIER'})

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Buyurtma holati")
    
    # Moliyaviy qism (Aniq so'mda hisoblanadi, foizlardan butkul voz kechildi)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Umumiy summa")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Magazinchi to'lagan summa")
    debt_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Nasiya (Qarz) summa")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Django saqlash (save) funksiyasini kengaytiramiz: Qarzni avtomatik matematik hisoblash uchun
    def save(self, *args, **kwargs):
        # Qarz summasi = Umumiy summadan to'langan summani ayirganimizga teng
        self.debt_amount = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)

    def __str__(self):
        # Ba'zi foydalanuvchilarda profil yaratilmagan bo'lsa xato bermasligi uchun xavfsiz format:
        store = getattr(self.client, 'client_profile', None)
        store_name = store.store_name if store else "Noma'lum do'kon"
        return f"Buyurtma #{self.id} - {store_name} (Qarz: {self.debt_amount} so'm)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # 🟢 ESKI orders ichidagi Product emas, yangi products.Product modeliga ulandiki:
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(verbose_name="Soni")
    price_at_order = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Buyurtma paytidagi narxi")
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"