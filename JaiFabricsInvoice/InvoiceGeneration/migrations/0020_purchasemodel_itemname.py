# Generated by Django 3.0.6 on 2020-06-27 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0019_sellermodel_gsttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasemodel',
            name='itemName',
            field=models.CharField(default='', max_length=25),
        ),
    ]
