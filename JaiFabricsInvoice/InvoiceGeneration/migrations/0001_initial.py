# Generated by Django 3.0.6 on 2020-06-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custName', models.CharField(max_length=20)),
                ('custGST', models.CharField(max_length=12)),
                ('address1', models.CharField(max_length=25)),
                ('address2', models.CharField(max_length=25)),
                ('gstType', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerName', models.CharField(max_length=20)),
                ('sellerGST', models.CharField(max_length=12)),
                ('invoiceNumber', models.CharField(max_length=15)),
                ('quantity', models.CharField(max_length=15)),
                ('pricePerUnit', models.CharField(max_length=8)),
                ('otherCharges', models.CharField(max_length=10)),
                ('subTotal', models.CharField(max_length=10)),
                ('gstType', models.CharField(max_length=10)),
                ('GST', models.CharField(max_length=8)),
                ('totalAmount', models.CharField(max_length=10)),
            ],
        ),
    ]
