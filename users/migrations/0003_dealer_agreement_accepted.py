# Generated by Django 5.0.3 on 2024-03-26 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_admin_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='agreement_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
