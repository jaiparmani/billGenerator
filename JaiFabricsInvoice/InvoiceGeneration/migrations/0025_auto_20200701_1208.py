# Generated by Django 3.0.6 on 2020-07-01 12:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0024_auto_20200701_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salemodel',
            name='invoiceDate',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=40, null=True),
        ),
    ]
