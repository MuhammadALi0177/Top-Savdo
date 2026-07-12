from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="Rasm")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Brend nomi")
    logo = models.ImageField(upload_to='brands/', null=True, blank=True, verbose_name="Logotip")

    class Meta:
        verbose_name = "Brend"
        verbose_name_plural = "Brendlar"

    def __str__(self):
        return self.name


class Product(models.Model):
    # 🟢 YANGI: Mahsulot qaysi dilerga tegishli ekanligini bildiruvchi maydon.
    # Bu maydon yo'qligi sababli buyurtma berishda "dealer" aniqlanmay, 400 xato chiqayotgan edi.
    dealer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'role': 'DEALER'},
        null=True, blank=True,
        verbose_name="Diler (Mahsulot egasi)"
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Kategoriya")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Brend")
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Artikul / SKU")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price = models.DecimalField(max_length=10, decimal_places=2, max_digits=10, verbose_name="Narxi")
    # 🟢 YANGI: Tan narxi (sotib olish/ishlab chiqarish narxi). Faqat diler o'zi ko'radi,
    # magazinchi (client) tomonga hech qachon chiqarilmaydi (serializerda maxsus yashiriladi).
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name="Tan narxi (faqat diler ko'radi)"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Ombordagi qoldiq")
    # 🟢 Rasm maydoni qo'shildi
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Mahsulot rasmi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    # 🟢 YANGI: Bu qator ushbu Product yozuvi diler tomonidan boshqa mahsulotlardan
    # yig'ilgan "Savat" (to'plam) ekanligini bildiradi. Savat ham oddiy mahsulot
    # kabi katalogga, buyurtmaga va statistikaga tushadi — alohida tizim shart emas.
    is_bundle = models.BooleanField(default=False, verbose_name="Savat (to'plam) mahsulotmi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return self.name


class BundleItem(models.Model):
    """
    🟢 YANGI: "Savat" (to'plam) mahsulot ichidagi tarkibiy qismlar.
    Har bir savat — bir nechta oddiy mahsulotdan (component) va ularning
    sonidan (quantity) tashkil topadi. `bundle` — is_bundle=True bo'lgan Product,
    `component` — dilerning o'zining oddiy (is_bundle=False) mahsuloti.
    """
    bundle = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='bundle_components',
        verbose_name="Savat"
    )
    component = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='used_in_bundles',
        verbose_name="Tarkibidagi mahsulot"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")

    class Meta:
        verbose_name = "Savat tarkibi"
        verbose_name_plural = "Savat tarkiblari"
        unique_together = ('bundle', 'component')

    def __str__(self):
        return f"{self.bundle.name} <- {self.component.name} x {self.quantity}"