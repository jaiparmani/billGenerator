# Generated by Django 3.0.6 on 2020-07-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0035_auto_20200706_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermodel',
            name='email_id',
            field=models.EmailField(default='ashokparmani@gmail.com', max_length=254),
        ),
    ]
