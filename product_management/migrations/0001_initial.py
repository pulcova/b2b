# Generated by Django 5.0.3 on 2024-03-31 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('hex_code', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DesignNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design_no', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PI', 'Pending Invoice'), ('PP', 'Pending Payment'), ('PD', 'Paid')], default='PI', max_length=2)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.dealer')),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.retailer')),
                ('sales_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_address', models.TextField()),
                ('customer_id', models.CharField(max_length=255)),
                ('gst_number', models.CharField(max_length=15)),
                ('waybill_number', models.CharField(max_length=255)),
                ('gst_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('courier_name', models.CharField(max_length=255)),
                ('payment_status', models.CharField(choices=[('P', 'Pending'), ('PD', 'Paid'), ('O', 'Overdue')], default='P', max_length=2)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('images', models.ImageField(upload_to='media/product_images/')),
                ('msrp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wholesale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_colors', models.ManyToManyField(to='product_management.color')),
                ('design_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.designnumber')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.producttype')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('order_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.color')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.size')),
            ],
        ),
        migrations.CreateModel(
            name='SizeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('sizes', models.ManyToManyField(to='product_management.size')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='default_size_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_management.sizegroup'),
        ),
    ]