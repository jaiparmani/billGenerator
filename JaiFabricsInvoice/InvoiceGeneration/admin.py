from django.contrib import admin
from InvoiceGeneration.models import CustomerModel, SaleModel
from InvoiceGeneration.models import PurchaseModel, SellerModel, Transaction
# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(PurchaseModel)
admin.site.register(SaleModel)
admin.site.register(SellerModel)
admin.site.register(Transaction)


