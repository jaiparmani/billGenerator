# Generated by Django 3.0.6 on 2020-06-25 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0012_auto_20200625_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salemodel',
            name='invoiceNumber',
            field=models.CharField(max_length=20),
        ),
    ]