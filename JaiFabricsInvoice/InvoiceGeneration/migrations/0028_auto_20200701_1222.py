# Generated by Django 3.0.6 on 2020-07-01 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0027_salemodel_invoicedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salemodel',
            name='transportName',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
    ]