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
           self.fields[price] = forms.IntegerField(required=False)
           quantity = "Quantity of %s" %(i+1)
           self.fields[quantity] = forms.CharField(required=False)


           try:
               field_name = 'Item_%s' % (i + 1,)
               self.initial[field_name] = ''
           except IndexError:
               self.initial[field_name] = ''
       # create an extra blank field
       # self.fields[field_name] = forms.CharField(required=False)






class CustForm(forms.Form):
    invoiceNumber = forms.IntegerField(required = True)
    custGST = forms.CharField(max_length =  20)
    custName = forms.CharField(max_length =  256)
    custAddress1 = forms.CharField(max_length = 100)
    custAddress2 = forms.CharField(max_length = 100)

    noOfItems = forms.IntegerField()
    GST_Type=forms.ChoiceField(widget=forms.RadioSelect, choices=[('CGST+SGST','CGST+SGST'), ('IGST', 'IGST')])
    CHOICES = [('1','GST'), ('2','Vehicle Number')]
    SELECTYOURCHOICE=forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    GSTorVehicleNumber=forms.CharField(max_length =  20)
    TransportName = forms.CharField(max_length = 50)
    LR_NO = forms.IntegerField()


class SecurityCheck(forms.Form):
    pin = forms.IntegerField()
