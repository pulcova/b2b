# Generated by Django 5.0.3 on 2024-03-29 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_color_color_code_size_sort_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='sort_order',
        ),
    ]
