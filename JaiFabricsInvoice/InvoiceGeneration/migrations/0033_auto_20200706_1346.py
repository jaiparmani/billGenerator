# Generated by Django 3.0.6 on 2020-07-06 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0032_auto_20200706_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salemodel',
            old_name='transportGST',
            new_name='transportGSTOrVehicleNumber',
        ),
        migrations.RenameField(
            model_name='salemodel',
            old_name='transportNameOrVehicleNo',
            new_name='transportName',
        ),
    ]
