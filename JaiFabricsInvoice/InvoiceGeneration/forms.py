from django import forms
import InvoiceGeneration
# from InvoiceGeneration.views import Inputs
class BillInfoForm(forms.Form):

    name = forms.TextInput()
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       fields = InvoiceGeneration.views.giveNo()
       # for i in range(fields):
           # self.fields['my_field_%i' % i] = forms.CharField(max_length=100)
       # interests = ProfileInterest.objects.filter(
           # profile=self.instance
       # )
       input = InvoiceGeneration.views.giveNo()
       interests = input
       print(interests)
       for i in range((interests)):
           field_name = 'Item_%s' % (i+1,)
           self.fields[field_name] = forms.CharField(required=False)
           price = 'Price Of %s' %(i+1)
           self.fields[price] = forms.CharField(required=False)
           quantity = "Quantity of %s" %(i+1)
           self.fields[quantity] = forms.CharField(required=False)


           try:
               field_name = 'Item_%s' % (i + 1,)
               self.initial[field_name] = ''
           except IndexError:
               self.initial[field_name] = ''
       # create an extra blank field
       # self.fields[field_name] = forms.CharField(required=False)



from InvoiceGeneration.models import CustomerModel, PurchaseModel, Transaction

class AddCustomerForm(forms.ModelForm):
    class Meta():

        model = CustomerModel
        exclude = []
        CHOICES=[('CGST+SGST','CGST+SGST'), ('IGST', 'IGST')]
        widgets = {
            'gstType': forms.RadioSelect(choices = CHOICES)
        }


from InvoiceGeneration.models import SellerModel
class AddSellerForm(forms.ModelForm):
    # custName = forms.ModelChoiceField(label="Customer Name",queryset=SellerModel.objects.all(),widget=forms.Select)

    class Meta():
        model = SellerModel
        exclude = []
        CHOICES=[('CGST+SGST','CGST+SGST'), ('IGST', 'IGST')]
        widgets = {
            'GSTType': forms.RadioSelect(choices = CHOICES)
            # 'sellerName':
        }

import datetime

from django.contrib.admin.widgets import AdminDateWidget
class TransactionForm(forms.Form):


    party = forms.ModelChoiceField(required = False, label = "Sale", queryset = CustomerModel.objects.all() , widget = forms.Select)
    party2 = forms.ModelChoiceField(required = False, label = "Purchase",  queryset =SellerModel.objects.all(), widget = forms.Select)
    partyType = forms.ChoiceField(widget = forms.Select, choices = [('Sale','Sale'),('Purchase', 'Purchase')])
    crdr = forms.ChoiceField(widget = forms.RadioSelect, choices =[('CR','CR'), ('DR','DR')])
    transactionDate = forms.DateField(label="Transaction Date(YYYY-MM-DD)", required = True, widget=AdminDateWidget, initial=datetime.date.today())

    amount = forms.CharField(label = "Enter amount")
    ref = forms.CharField(label = "Enter ref")




class CustForm(forms.Form):
    isDuplicate = forms.ChoiceField(label="Is it a duplicate Bill?",widget = forms.RadioSelect, choices = [('1','YES'), ('0','NO')])
    invoiceNumber = forms.CharField(label="Inovice Number",required = True)
    invoiceDate = forms.DateField(label="Inovice Date(YYYY-MM-DD)", required = True, widget=AdminDateWidget, initial=datetime.date.today())
    # custList = list(CustomerModel.objects.all())
    # for i in CustomerModel.objects.all():
        # custList.append(i)
    # custName = forms.CharField()
    custName = forms.ModelChoiceField(label="Customer Name",queryset=CustomerModel.objects.all(),widget=forms.Select)
    HSN_CODE = forms.ChoiceField(label="HSN CODE", widget=forms.RadioSelect, choices=[('5407','5407'),('540710','540710'),('5903','5903'),('5402','5402'),('5911','5911'),])

    noOfItems = forms.IntegerField(label="Enter number of items:")
    # GST_Type=forms.ChoiceField(widget=forms.RadioSelect, choices=[('CGST+SGST','CGST+SGST'), ('IGST', 'IGST')])
    CHOICES = [('1','GST'), ('2','Vehicle Number')]
    SELECTYOURCHOICE=forms.ChoiceField(label="TRANSPORT",widget=forms.RadioSelect, choices=CHOICES)

    GSTorVehicleNumber=forms.CharField(label="Enter GST or vechicle number of transport:",max_length =  20, required = False)
    TransportName = forms.CharField(label="Enter Transport Name:",max_length = 50, required = False)
    LR_NO = forms.CharField(label="Enter LR no.:",required = False)




class saleDetailsForm(forms.Form):
    BillNo=forms.IntegerField(label="BillNo")
# class AddPurchaseForm(forms.ModelForm):
#     class Meta():
#         model = PurchaseModel
#         exclude = []
#         CHOICES=[('CGST+SGST','CGST+SGST'), ('IGST', 'IGST')]

#         widgets = {
#             'gstType': forms.RadioSelect(choices = CHOICES)
#
        # }
# from django.contrib.admin.widgets import AdminDateWidget


# from django.forms.extras.widgets import SelectDateWidget
class AddPurchaseForm(forms.Form):
    invoiceDate = forms.DateField(widget=AdminDateWidget, initial=datetime.date.today())
    sellerName = forms.ModelChoiceField(label="Seller Name",queryset=SellerModel.objects.all(),widget=forms.Select)

    # sellerName = forms.CharField(max_length = 40)
    # sellerGST = forms.CharField(max_length = 15)
    invoiceNumber = forms.CharField(max_length = 15)
    itemName = forms.CharField(max_length = 25)
    HSN = forms.ChoiceField(label="HSN Code", widget = forms.RadioSelect, choices = [('5407', '5407'), ('5402', '5402'), ('9988', '9988'),('8471','8471(Computer)')])
    quantity = forms.CharField(max_length = 15)
    pricePerUnit = forms.CharField(max_length = 8)
    otherCharges = forms.CharField(max_length = 10)
    # subTotal = forms.CharField(max_length = 10)
    # gstType = forms.CharField(max_length = 10)
    gstType2 = forms.ChoiceField(label="Select GST Type", widget = forms.RadioSelect, choices = [('CGST+SGST(6%+6%)','CGST+SGST(6%+6%)'),('IGST(12%)', 'IGST(12%)'), ('CGST+SGST(2.5%+2.5%)','CGST+SGST(2.5%+2.5%)'),('IGST(5%)', 'IGST(5%)'),('CGST+SGST(9%+9%)','CGST+SGST(9%+9%)')])
    # GST = models.CharField(max_length = 8)
    # IGST = forms.CharField(max_length = 10)
    # CGST = forms.CharField(max_length = 10)
    # SGST = forms.CharField(max_length = 10)

    # totalAmount = forms.CharField(max_length = 10)


class SecurityCheck(forms.Form):
    pin = forms.IntegerField()



class salePartyWiseForm(forms.Form):

     custName = forms.ModelChoiceField(label="Customer Name",queryset=CustomerModel.objects.all(),widget=forms.Select)

class purchasePartyWiseForm(forms.Form):
    sellerName = forms.ModelChoiceField(label="Seller Name",queryset=SellerModel.objects.all(),widget=forms.Select)


class letterForm(forms.Form):
    letterDate = forms.DateField(widget=AdminDateWidget, initial=datetime.date.today())
    custName = forms.CharField(max_length=100)
    letterBody=forms.CharField(max_length=1000, widget=forms.Textarea(attrs={"rows":5, "cols":20}))



class GetTransactionsForm(forms.Form):
    party = forms.ModelChoiceField(required = False, label = "Sale", queryset = CustomerModel.objects.all() , widget = forms.Select)
    party2 = forms.ModelChoiceField(required = False, label = "Purchase",  queryset =SellerModel.objects.all(), widget = forms.Select)

    partyType = forms.ChoiceField(widget = forms.Select, choices = [('Sale','Sale'),('Purchase', 'Purchase')])

    fromDate = forms.DateField(widget=AdminDateWidget, initial=datetime.date.today())
    toDate = forms.DateField(widget=AdminDateWidget, initial=datetime.date.today())


class VerifyPin(forms.Form):
    pin = forms.IntegerField(label = "Enter pin")

