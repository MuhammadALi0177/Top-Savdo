# Generated manually (venv Windows uchun mo'ljallangan bo'lgani sababli makemigrations shu yerda ishlatilmadi)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Tan narxi (faqat diler ko'radi)"),
        ),
    ]