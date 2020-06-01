from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
# Create your views here.

global no
no = 1

global dict
dict = {}

global itemList
global QuantityList
global PriceList
global finalList
itemList = []
QuantityList=[]
PriceList=[]
finalList = []
global custDetails
custDetails = []

global transportDetails
transportDetails = []

global invoiceNumber
invoiceNumber = 1

global GSTType
GSTType = ''
global custAddress1
global custAddress2
custAddress1 = ''
custAddress2 = ''



global TransportName
global LR_NO
TransportName=''
LR_NO=''
global subtotal
global total
global tax

subtotal, tax, total = 1, 1, 1
def FinalBill(request):
    # template_name = "finalBill.html"
    global subtotal
    global total
    global tax
    global itemList
    global QuantityList
    global PriceList
    global finalList
    global invoiceNumber
    global GSTType
    global custAddress1
    global custAddress2
    global TransportName
    global LR_NO
    from num2words import num2words
    totalFigure=num2words(total, to = 'currency', lang='en', currency ='INR'  )
    return render(request, 'finalBill.html',{'TransportName': TransportName, 'lrno':LR_NO, 'GSTType':GSTType,'invoiceNumber':invoiceNumber,'finalList' : finalList,
    'subtotal':subtotal ,'total':total, 'tax':tax, 'customerName':custDetails[1],'custGST':custDetails[0], 'totalFigure':totalFigure, 'invoiceDate':'31/12/200','choice': transportDetails[0],'custAddress1':custAddress1,'custAddress2':custAddress2, 'choiceInfo':transportDetails[1]})
from num2words import num2words
class BasePage(TemplateView):
    template_name = "base.html"
def GenerateBill(request):
    print(dict, "From generate")
    global itemList
    global QuantityList
    global PriceList
    global finalList
    itemList = []
    QuantityList=[]
    PriceList=[]
    finalList = []
    global subtotal
    global total
    global tax
    global GSTType
    global custAddress1
    global custAddress2

    for i in range(0, int(len(dict)/3)):
        # print(i)
        itemList.append(dict['Item_{}'.format(i+1)])
        QuantityList.append(dict['Quantity of {}'.format(i+1)])
        PriceList.append(dict['Price Of {}'.format(i+1)])
        print(dict['Item_{}'.format(i+1)])
        finalList.append([itemList[i], QuantityList[i], PriceList[i], float(QuantityList[i])*float(PriceList[i])])
        subtotal = 0
    for i in range(len(finalList)):
        subtotal+=finalList[i][3]
    tax = round(subtotal*1.0/100*5, 2)
    total = subtotal + tax

    global TransportName
    global LR_NO
    from num2words import num2words
    totalFigure=num2words(total, to = 'currency', lang='en', currency ='INR'  )
    # custAddress1, custAddress2 = 1,1
    return render(request, 'bill.html',{'TransportName': TransportName, 'lrno':LR_NO, 'GSTType':GSTType,'invoiceNumber':invoiceNumber,'finalList' : finalList,
    'subtotal':subtotal ,'total':total, 'tax':tax, 'customerName':custDetails[1],'custGST':custDetails[0], 'totalFigure':totalFigure, 'invoiceDate':'31/12/200','choice': transportDetails[0],'custAddress1':custAddress1,'custAddress2':custAddress2, 'choiceInfo':transportDetails[1]})
    print(finalList)
# class GenerateBill(DetailView):
    # template_name = "bill.html"
    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # return context





from InvoiceGeneration.forms import SecurityCheck
def SecurityForm(request):
    if request.method == "POST":
        form = SecurityCheck(request.POST)
        if form.is_valid():
            if(form.cleaned_data['pin']==1803):
                    return redirect('Form')
            else:
                return render(request, 'securityCheck.html', {'SecurityForm':form})

        else:
            return render(request, 'securityCheck.html', {'SecurityForm':form})

    else:
        form = SecurityCheck()

        return render(request, 'securityCheck.html', {'SecurityForm':form})
from InvoiceGeneration.forms import BillInfoForm
def BillInfo(request):
    if request.method == "POST":
        form = BillInfoForm(request.POST)
        if form.is_valid():
            print("HI")
            # form.cleaned_data
            print(form.cleaned_data)
            global dict
            dict = form.cleaned_data
            # return render(request, 'CustomerNItems.html', {'CustForm' : CustForm})
            return redirect("GenerateBill")
    else:

    # template_name = "forms.html"
    # if request.method == "POST":
    #     if CustForm.is_valid():
    #         custDetails = CustForm.save()

    # print(custDetails.noOfItems)
        form = BillInfoForm()
        return render(request, "forms.html", {"form":form})

#Gives the number of items in the bill

# class Inputs:
    # def numberOfInputs(inp = 1):
            # return inp




from django.shortcuts import  redirect


from InvoiceGeneration.forms import CustForm
def CustomerAndNumberOfItems(request):
    if request.method == "POST":
        form = CustForm(request.POST)
        if form.is_valid():
            global no
            global invoiceNumber
            invoiceNumber =  form.cleaned_data['invoiceNumber']
            global GSTType
            GSTType = form.cleaned_data['GST_Type']
            global custAddress1
            global custAddress2
            custAddress1 = form.cleaned_data['custAddress1']
            custAddress2 = form.cleaned_data['custAddress2']
            global TransportName
            global LR_NO
            TransportName =  form.cleaned_data['TransportName']
            LR_NO =  form.cleaned_data['LR_NO']
            no =  form.cleaned_data['noOfItems']
            custGST =  form.cleaned_data['custGST']
            # form.cleaned_data
            global custDetails
            custName =  form.cleaned_data['custName']
            custDetails = [custGST, custName]
            global transportDetails
            transportDetails = [ form.cleaned_data['SELECTYOURCHOICE'], form.cleaned_data['GSTorVehicleNumber']]
            print(transportDetails)
            if(transportDetails[0]=='1'):
                transportDetails[0]='GST'
            else:
                transportDetails[0]='Vechicle Number'

            print(  form.cleaned_data['noOfItems'])
            # return render(request, 'CustomerNItems.html', {'CustForm' : CustForm})
            return redirect("BillInfo")
        else: #form is not  validity
            return redirect("ErrorPage")
        # global custDetails
        # custDetails = CustForm
        # return form['noOfItems']

    else:
        customerForm = CustForm
        return render(request, 'CustomerNItems.html', {'CustForm' : CustForm})


def giveNo():
    print("Called from form! Returned=", no)
    return no
