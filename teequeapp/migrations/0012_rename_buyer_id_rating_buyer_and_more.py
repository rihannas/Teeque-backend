# Generated by Django 4.2.15 on 2024-09-03 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teequeapp', '0011_rename_order_id_orderitem_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='buyer_id',
            new_name='buyer',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='service_id',
            new_name='service',
        ),
    ]