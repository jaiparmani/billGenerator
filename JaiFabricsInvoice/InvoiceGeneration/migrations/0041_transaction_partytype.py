# Generated by Django 3.0.6 on 2021-09-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0040_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='partyType',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]
