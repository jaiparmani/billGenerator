from django.db import models
import django
# Create your models here.


class CustomerModel(models.Model):
    custName = models.CharField(max_length = 40)
    custGST = models.CharField(max_length = 15)
    address1 = models.CharField(max_length = 50)
    address2 = models.CharField(max_length = 70)
    gstType = models.CharField(max_length =10)
    email_id = models.EmailField(max_length=254, default="ashokparmani@gmail.com")
    def __str__(self):
        return '{0}:{1}'.format(self.custName ,self.custGST)

class PurchaseModel(models.Model):
    invoicedate = models.DateField(blank=True)
    sellerName = models.CharField(max_length = 40, default='')
    sellerGST = models.CharField(max_length = 15, default='')
    invoiceNumber = models.CharField(max_length = 15, default='')

    itemName = models.CharField(max_length = 25, default='')
    HSN = models.CharField(max_length= 5, default = '')
    quantity = models.CharField(max_length = 15, default='')
    pricePerUnit = models.CharField(max_length = 8, default='')
    otherCharges = models.CharField(max_length = 10, default='')
    subTotal = models.CharField(max_length = 10, default='')
    gstType = models.CharField(max_length = 10, default='')
    gstType2 = models.CharField(max_length = 20, default='')
    # GST = models.CharField(max_length = 8, default='')
    IGST = models.CharField(max_length = 10, default = '0')
    CGST = models.CharField(max_length = 10, default = '0')
    SGST = models.CharField(max_length = 10, default = '0')

    totalAmount = models.CharField(max_length = 10)
    def __str__(self):
        return self.sellerName+"  "+str(self.invoiceNumber)

import datetime
class SaleModel(models.Model):
    invoiceNumber = models.CharField(max_length = 15)
    invoiceDate = models.DateField(blank=True, null=True)
    # invoiceDate1 = models.DateField(default=SaleModel.objects.invoiceDate)
    custName = models.CharField(max_length = 40)
    custGST = models.CharField(max_length = 15)
    itemName = models.CharField(max_length = 20)
    HSN_CODE = models.CharField(max_length=10, default=5407)
    quantity = models.CharField(max_length = 10)
    pricePerUnit = models.CharField(max_length = 5)
    subtotal = models.CharField(max_length = 10)
    gstType =   models.CharField(max_length = 10)

    IGST = models.CharField(max_length = 10, default = '0')
    CGST = models.CharField(max_length = 10, default = '0')
    SGST = models.CharField(max_length = 10, default = '0')
    total =models.CharField(max_length = 10)
    transportName = models.CharField(max_length = 25, default='-', blank=True, null=True)
    transportGSTOrVehicleNumber = models.CharField(max_length = 15, default='-', blank=True, null=True)
    LR_NO = models.CharField(max_length = 10, default='-', blank=True, null=True)

    def __str__(self):
        return str(self.invoiceNumber)


class SellerModel(models.Model):
    sellerName = models.CharField(max_length = 40)
    sellerGST = models.CharField(max_length = 15)
    GSTType = models.CharField(max_length = 10, default = '')
    def __str__(self):
        return self.sellerName + ":" +self.sellerGST



class Transaction(models.Model):

    partyGST = models.CharField(max_length = 15, default='')
    partyType = models.CharField(max_length = 10)
    transactionDate = models.DateField(blank=True, null=True)
    ref = models.CharField(max_length = 100)
    crdr = models.CharField(max_length = 2)
    amount = models.IntegerField()





