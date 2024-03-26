# Generated by Django 5.0.3 on 2024-03-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_purchase_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='product',
        ),
        migrations.AddField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]