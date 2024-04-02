# Generated by Django 5.0.3 on 2024-04-02 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PI', 'Pending Invoice'), ('PP', 'Pending Payment'), ('PD', 'Paid')], default='PP', max_length=2),
        ),
    ]
