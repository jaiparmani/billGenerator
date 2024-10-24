from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from django.core.paginator import Paginator
from django.db.models.functions import Cast

from django.db.models import IntegerField


# Create your views here.

global HSN_CODE
HSN_CODE=''
global no
no = 1
global GSTPERCENTAGE
GSTPERCENTAGE=''
global dict
dict = {}

#CHANGE BILL NO HERE
global fromBillNo
fromBillNo='100'
#PURCHASE
global srPurchase
srPurchase = 1
global fromDatePurchase
fromDatePurchase='2020-10-10'


global Date
Date=''
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
global custEmail
custEmail =""
global HSN_CODE_TAX
HSN_CODE_TAX = {}
HSN_CODE_TAX['5911'] = 12
HSN_CODE_TAX["5407"] = 5
HSN_CODE_TAX["540710"] = 5
HSN_CODE_TAX["5903"] = 12
HSN_CODE_TAX["5402"] = 12

subtotal, tax, total = 1, 1, 1

from InvoiceGeneration.forms import AddPurchaseForm
from InvoiceGeneration.forms import AddCustomerForm
from InvoiceGeneration.models import SellerModel


def AddPurchase(request):
    # pass
    if request.method == "POST":
        form = AddPurchaseForm(request.POST)
        if form.is_valid():
            # form.save()
            try:
                IGST = 0
                CGST = 0
                SGST = 0
                subtotal = float(round(float(form.cleaned_data['quantity'])*float(form.cleaned_data['pricePerUnit']),2)+float(form.cleaned_data['otherCharges']))
                gstChoices = ['CGST+SGST(6%+6%)', 'IGST(12%)', 'CGST+SGST(2.5%+2.5%)', 'IGST(5%)', 'CGST+SGST(9%+9%)']
                gstType2=form.cleaned_data['gstType2']
                if(gstType2 == gstChoices[0]):
                    IGST = 0
                    CGST = subtotal*6/100
                    SGST = subtotal*6/100

                elif(gstType2 == gstChoices[1]):
                    IGST = subtotal*12/100
                    CGST = 0
                    SGST = 0

                elif(gstType2 == gstChoices[2]):
                    IGST = 0
                    CGST = subtotal*2.5/100
                    SGST = subtotal*2.5/100

                elif(gstType2 == gstChoices[3]):
                    IGST = subtotal*5/100
                    CGST = 0
                    SGST = 0
                elif(gstType2 == gstChoices[4]):
                    IGST = 0
                    CGST = subtotal*9/100
                    SGST = subtotal*9/100
                IGST = round(IGST,2)
                CGST = round(CGST,2)
                SGST = round(SGST,2)
                total = subtotal+ IGST + CGST + SGST
                total = round(total)
                sellerGST = SellerModel.objects.values('sellerGST').filter(sellerName=str(form.cleaned_data['sellerName']).split(":")[0])
                GSTType = SellerModel.objects.values('GSTType').filter(sellerName=str(form.cleaned_data['sellerName']).split(":")[0])
                # sellerGST = SellerModel.objects.values('sellerGST').filter(custName=form.cleaned_data['sellerName'])

                # obj = PurchaseModel(invoiceNumber=form.cleaned_data['invoiceNumber'], invoicedate=form.cleaned_data['invoiceDate'], sellerName=form.cleaned_data['sellerName'],
                # sellerGST=sellerGST, itemName=form.cleaned_data['itemName'], HSN=form.cleaned_data['HSN'],
                # quantity=form.cleaned_data['quantity'], pricePerUnit=form.cleaned_data['pricePerUnit'], subTotal=form.cleaned_data['subTotal'], otherCharges=form.cleaned_data['otherCharges'], gstType=GSTType,
                # gstType2=form.cleaned_data['gstType2'], IGST=form.cleaned_data['IGST'], CGST=form.cleaned_data['CGST'],
                # SGST=form.cleaned_data['SGST'], totalAmount=form.cleaned_data['totalAmount'])

                obj = PurchaseModel(invoiceNumber=form.cleaned_data['invoiceNumber'], invoicedate=form.cleaned_data['invoiceDate'], sellerName=str(form.cleaned_data['sellerName']).split(":")[0],
                sellerGST=sellerGST, itemName=form.cleaned_data['itemName'], HSN=form.cleaned_data['HSN'],
                quantity=form.cleaned_data['quantity'], pricePerUnit=form.cleaned_data['pricePerUnit'], subTotal=subtotal,
                otherCharges=form.cleaned_data['otherCharges'], gstType=GSTType,
                gstType2=form.cleaned_data['gstType2'], IGST=IGST, CGST=CGST,
                SGST=SGST, totalAmount= total)
                obj.save()
            except Exception as e:
                return HttpResponse(str(e)+str([x for x in sellerGST]) + str(len(sellerGST)) + str(form.cleaned_data['sellerName'])  )
                return HttpResponse(str([x for x in sellerGST]) + str(len(sellerGST)) + str(form.cleaned_data['sellerName']))
            return redirect('AddPurchase')

    else:
        form = AddPurchaseForm()
    return render(request, 'AddPurchase.html', {'form': form})

def AddCustomer(request):
    if request.method == "POST":
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AddCustomer')


    else:
        form = AddCustomerForm()
    return render(request, 'AddCustomer.html', {'form': form})


from InvoiceGeneration.forms import AddSellerForm
def AddSeller(request):
    if request.method == "POST":
        form = AddSellerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AddSeller')


    else:
        form = AddSellerForm()
    return render(request, 'AddSeller.html', {'form': form})

global isDuplicate
isDuplicate = 0
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
    global Date
    global custAddress1
    global custAddress2
    global TransportName
    global LR_NO
    from num2words import num2words
    global GSTPERCENTAGE
    totalFigureNo = float(total)

    totalFigure=num2words(totalFigureNo, to = 'currency', lang='en', currency ='INR'  )
    return render(request, 'finalBill.html',{'TransportName': TransportName, 'lrno':LR_NO, 'GSTType':GSTType,'invoiceNumber':invoiceNumber,'finalList' : finalList,
    'subtotal':subtotal ,'total':total, 'tax':tax, 'customerName':custDetails[1],'custGST':custDetails[0], 'totalFigure':totalFigure, 'invoiceDate': Date,'choice': transportDetails[0],
    'custAddress1':custAddress1,'custAddress2':custAddress2, 'choiceInfo':transportDetails[1], 'HSN_CODE':HSN_CODE, 'GSTPERCENTAGE':GSTPERCENTAGE})
    from num2words import num2words
class BasePage(TemplateView):
    template_name = "base.html"
from InvoiceGeneration.models import SaleModel
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
    global Date
    global GSTPERCENTAGE
    global HSN_CODE_TAX
    for i in range(0, int(len(dict)/3)):
        # print(i)
        itemList.append(dict['Item_{}'.format(i+1)])
        QuantityList.append(dict['Quantity of {}'.format(i+1)])
        PriceList.append(dict['Price Of {}'.format(i+1)])
        print(dict['Item_{}'.format(i+1)])
        finalList.append([itemList[i], QuantityList[i], PriceList[i], round(float(QuantityList[i])*float(PriceList[i]),2)])
    subtotal = 0
    global HSN_CODE
    global GSTPERCENTAGE
    GSTPERCENTAGE=''
    for i in range(len(finalList)):
        subtotal+=finalList[i][3]
    subtotal = round(subtotal, 2)

    # NEW CODzE TO FIT IN HSN_CODE_TAX dict
    GSTPERCENTAGE = HSN_CODE_TAX[str(HSN_CODE)]
    tax = round(subtotal*1.0/100*GSTPERCENTAGE, 2)
    if(not GSTType == "IGST"):
        GSTPERCENTAGE /= 2
    GSTPERCENTAGE = int(GSTPERCENTAGE) if GSTPERCENTAGE %  1 == 0 else float(GSTPERCENTAGE)


    # return HttpResponse(GSTType, GSTPERCENTAGE)
    """
    if(int(HSN_CODE)==5407):
        if(GSTType=="IGST"):
            GSTPERCENTAGE=5
        else:
            GSTPERCENTAGE=2.5
    else:
        if(GSTType=="IGST"):
            GSTPERCENTAGE=12
        else:
            GSTPERCENTAGE=6
            """
        # tax = round(subtotal*1.0/100*12, 2)
                # gstType='CGST+SGST'
    total = subtotal + tax

    total = round(total)
    global isDuplicate
    global TransportName
    # isDuplicate = False
    global LR_NO

    if(isDuplicate == '0'):
        try:


            obj = SaleModel(invoiceNumber = invoiceNumber,invoiceDate = Date, custName = custDetails[1], custGST = custDetails[0],
                itemName = itemList[0], quantity = QuantityList[0], pricePerUnit = PriceList[0], subtotal = subtotal,
                gstType = GSTType , CGST = round(float(tax/2), 2), SGST = round(float(tax/2),2),    total =total,
                transportName=TransportName, transportGSTOrVehicleNumber=transportDetails[1], LR_NO = LR_NO,
                HSN_CODE=HSN_CODE)
            obj.save()

            """
            if(GSTType == 'IGST'):
                obj = SaleModel(invoiceNumber = invoiceNumber,invoiceDate = Date, custName = custDetails[1], custGST = custDetails[0],
                itemName = itemList[0], quantity = QuantityList[0], pricePerUnit = PriceList[0], subtotal = subtotal,
                gstType = GSTType , IGST = tax,    total =total, transportName=TransportName, transportGSTOrVehicleNumber=transportDetails[1], LR_NO = LR_NO)
                obj.save()
            elif(int(HSN_CODE)==5407):
                # GSTPERCENTAGE=2.5
                obj = SaleModel(invoiceNumber = invoiceNumber,invoiceDate = Date, custName = custDetails[1], custGST = custDetails[0],
                itemName = itemList[0], quantity = QuantityList[0], pricePerUnit = PriceList[0], subtotal = subtotal,
                gstType = GSTType , CGST = round(float(tax/2), 2), SGST = round(float(tax/2),2),    total =total,  transportName=TransportName, transportGSTOrVehicleNumber=transportDetails[1], LR_NO = LR_NO)
                obj.save()
            else:
                tax = round(subtotal*1.0/100*12, 2)
                # gstType='CGST+SGST'
                GSTPERCENTAGE=6
                obj = SaleModel(invoiceNumber = invoiceNumber,invoiceDate = Date, custName = custDetails[1], custGST = custDetails[0],
                itemName = itemList[0], quantity = QuantityList[0], pricePerUnit = PriceList[0], subtotal = subtotal,
                gstType = GSTType , CGST = round(float(tax/2), 2), SGST = round(float(tax/2),2),    total =total,
                transportName=TransportName, transportGSTOrVehicleNumber=transportDetails[1], LR_NO = LR_NO,
                HSN_CODE=HSN_CODE)
                obj.save()
                """
        except Exception as e:
            return HttpResponse(e)


    from num2words import num2words
    totalFigureNumber = float(total)
    totalFigure=num2words(totalFigureNumber, to = 'currency', lang='en', currency ='INR'  )
    # custAddress1, custAddress2 = 1,1
    return render(request, 'bill.html',{'TransportName': TransportName, 'lrno':LR_NO, 'GSTType':GSTType,'invoiceNumber':invoiceNumber,'finalList' : finalList,
    'subtotal':subtotal ,'total':total, 'tax':tax, 'customerName':custDetails[1],'custGST':custDetails[0], 'totalFigure':totalFigure, 'invoiceDate': Date,'choice': transportDetails[0],
    'custAddress1':custAddress1,'custAddress2':custAddress2, 'choiceInfo':transportDetails[1], 'HSN_CODE':HSN_CODE, 'GSTPERCENTAGE':GSTPERCENTAGE})
    print(finalList)
# class GenerateBill(DetailView):
    # template_name = "bill.html"
    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # return context

import datetime
class saleTotal(ListView):
    model = SaleModel

    template_name = 'saleTotal.html'
    context_object_name = 'saleList'
    today = datetime.datetime.today()
    paginate_by = 10  # Number of items per page


    # if today.month == 1:
    #     one_month_ago = today.replace(year=today.year - 1, month=12)
    # else:
    #     extra_days = 0
    #     while True:
    #         try:
    #             one_month_ago = today.replace(month=today.month - 1, day=today.day - extra_days)
    #             break
    #         except ValueError:
    #             extra_days += 1


    queryset = SaleModel.objects.exclude(invoiceNumber__lt=fromBillNo).annotate(invoiceNumber_int=Cast('invoiceNumber', IntegerField())).order_by('-invoiceNumber_int')
from InvoiceGeneration.models import PurchaseModel
class purchaseTotal(ListView):
    # pass

    template_name = 'purchaseTotal.html'
    context_object_name = 'purchaseList'
    today = datetime.datetime.today()
    global srPurchase
    queryset = PurchaseModel.objects.all().order_by('-invoicedate')


from InvoiceGeneration.forms import saleDetailsForm
def saleDetailForm(request):
    if request.method == "POST":
        form = saleDetailsForm(request.POST)
        if form.is_valid():
            global fromBillNo
            fromBillNo = int(form.cleaned_data['BillNo'])
            # if(form.cleaned_data['pin']==1803):
            # return HttpResponse(fromBillNo)
            return redirect('saleTotal')

        else:
            return render(request, 'saleDetailForm.html', {'form':form})

            # return render(request, 'securityCheck.html', {'SecurityForm':form})

    else:
        form = saleDetailsForm()

        return render(request, 'saleDetailForm.html', {'form':form})



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

from django.http import HttpResponse
from InvoiceGeneration.models import CustomerModel
from InvoiceGeneration.forms import CustForm
def CustomerAndNumberOfItems(request):
    if request.method == "POST":
        form = CustForm(request.POST)
        if form.is_valid():
            global Date
            Date = form.cleaned_data['invoiceDate']
            global no
            global invoiceNumber
            global  isDuplicate
            isDuplicate = form.cleaned_data['isDuplicate']
            # return HttpResponse(isDuplicate)
            invoiceNumber =  form.cleaned_data['invoiceNumber']
            custName =  form.cleaned_data['custName']
            # return HttpResponse("HI")
            custName = str(custName).split(':')
            custGST = custName[1]
            custName = custName[0]
            global HSN_CODE
            HSN_CODE = int(form.cleaned_data['HSN_CODE'])
            # return HttpResponse(custGST)
            global GSTType
            try:
                GSTType = CustomerModel.objects.values('gstType').filter(custName=custName)
                # return HttpResponse(GSTType[0]['gstType'], 'hi')
            except Exception as e:
                return HttpResponse(e, 'hi')
            # GSTType = form.cleaned_data['GST_Type']
            GSTType = GSTType[0]['gstType']
            global custAddress1
            global custAddress2
            global custEmail
            try:
                custAddress1 = CustomerModel.objects.values('address1').filter(custName=custName)
                custAddress2 =  CustomerModel.objects.values('address2').filter(custName=custName)
                custEmail =  CustomerModel.objects.values('email_id').filter(custName=custName)
                # return HttpResponse(GSTType, 'hi')
            except Exception as e:
                return HttpResponse(e, 'hi')
            # custAddress1 = form.cleaned_data['custAddress1']
            # custAddress2 = form.cleaned_data['custAddress2']
            custAddress1 = custAddress1[0]['address1']
            custAddress2 = custAddress2[0]['address2']
            # for i in custAddress1:
                # return HttpResponse(i)
            # return HttpResponse(custAddress1, custGST)
            global TransportName
            global LR_NO
            TransportName =  form.cleaned_data['TransportName']
            LR_NO =  form.cleaned_data['LR_NO']

            no =  form.cleaned_data['noOfItems']
            if(LR_NO == ''):
                LR_NO = '          ';
            # custGST =  form.cleaned_data['custGST']
            # form.cleaned_data
            global custDetails
            # custName =  form.cleaned_data['custName']
            custDetails = [custGST, custName]
            global transportDetails
            transportDetails = [ form.cleaned_data['SELECTYOURCHOICE'], form.cleaned_data['GSTorVehicleNumber']]
            print(transportDetails)
            if(transportDetails[1] == ''):
                transportDetails[1] =  '                 ';
            if(transportDetails[0]=='1'):
                transportDetails[0]='GST'
            else:
                transportDetails[0]='Vehicle Number'

            print(  form.cleaned_data['noOfItems'])
            # return render(request, 'CustomerNItems.html', {'CustForm' : CustForm})
            return redirect("BillInfo")
        else: #form is not  validity
            return HttpResponse("Enter the form properly.")
        # global custDetails
        # custDetails = CustForm
        # return form['noOfItems']

    else:
        customerForm = CustForm
        return render(request, 'CustomerNItems.html', {'CustForm' : CustForm})


def giveNo():
    print("Called from form! Returned=", no)
    return no


# Return Month wise and Partyy wise
from InvoiceGeneration.forms import salePartyWiseForm
def salePartyWise(request):
    if request.method=="POST":
        form = salePartyWiseForm(request.POST)
        if form.is_valid():
            custName = str(form.cleaned_data['custName']).split(":")[0]
            bills=SaleModel.objects.all().filter(custGST=str(form.cleaned_data['custName']).split(":")[1]).order_by("-invoiceNumber")
            # return HttpResponse(bills)
            return render(request, "saleTotal.html", {"saleList":bills, "custName": custName })

    else:
        form=salePartyWiseForm
        return render(request, 'salePartyChoice.html',{'form':form})





from InvoiceGeneration.forms import purchasePartyWiseForm
def purchasePartyWise(request):
    if request.method=="POST":
        form = purchasePartyWiseForm(request.POST)
        if form.is_valid():
            # return HttpResponse(form.cleaned_data['sellerName'])
            bills=PurchaseModel.objects.all().filter(sellerName=str(str(form.cleaned_data['sellerName']).split(":")[0])).order_by("-invoicedate")
            # return HttpResponse(form.cleaned_data['sellerName'].split(":")[0])
            return render(request, "purchasePartyWiseList.html", {"purchaseList":bills})

    else:
        form=purchasePartyWiseForm
        return render(request, 'purchasePartyWise.html',{'form':form})
















# Generate Letter
from InvoiceGeneration.forms import letterForm
def generateLetter(request):
    if request.method=="POST":
        form = letterForm(request.POST)
        if form.is_valid():
            custName=str(form.cleaned_data['custName'])
            letterDate=str(form.cleaned_data['letterDate'])

            letterBody=str(form.cleaned_data['letterBody'])
            return render(request, 'letterPad.html', {'letterDate':letterDate,'custName':custName, 'letterBody':letterBody, })
    else:
        form=letterForm

        return render(request, 'letterFormPage.html',{'form':form})


# import xlsxwriter

# def getExcelSale(request):
#     sales = SaleModel.objects.all()

#     workbook = xlsxwriter.Workbook('sales.xlsx')
#     worksheet = workbook.add_worksheet()
#     salesList = [['Number'],['Date'],['Customer'],['GST'],['item'],['Quantity']]
#     for i in sales:
#         salesList[0].append(i.invoiceNumber)
#         salesList[1].append(i.invoiceDate)
#         salesList[2].append(i.CustName)
#         salesList[3].append(i.CustGST)
#         salesList[4].append(i.itemName)
#         salesList[5].append(i.Quantity)





#     workbook = xlsxwriter.Workbook('arrays.xlsx')
#     worksheet = workbook.add_worksheet()






#     row = 0

#     for col, data in enumerate(salesList):
#         worksheet.write_column(row, col, data)

#     workbook.close()







#     row = 0

#     for col, data in enumerate(salesList):
#         worksheet.write_column(row, col, data)

#     workbook.close()



from InvoiceGeneration.forms import TransactionForm
from InvoiceGeneration.models import Transaction


def addTransactions(request):

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            partyType=str(form.cleaned_data['partyType'])
            if(partyType == "Sale"):
                party = str(form.cleaned_data['party']).split(":")[1]

                party = CustomerModel.objects.get(custGST = party)
            else:
                party = str(form.cleaned_data['party2']).split(":")[1]
                party = SellerModel.objects.get(sellerGST = party)

            crdr = str(form.cleaned_data['crdr'])
            transactionDate = str(form.cleaned_data['transactionDate'])
            ref = str(form.cleaned_data['ref'])

            amount = str(form.cleaned_data['amount'])
            # saving it into the database


            obj = Transaction(partyGST = party, partyType = partyType, transactionDate = transactionDate, ref = ref, crdr = crdr, amount = amount)
            obj.save()
            # from django.https import HttpResponse
            return redirect('addTransactions')

            return HttpResponse({party, partyType})
            return render(request, 'letterPad.html', {'letterDate':letterDate,'custName':custName, 'letterBody':letterBody, })
    else:
        form=TransactionForm

        return render(request, 'transactionForm.html',{'form':form})







from InvoiceGeneration.forms import GetTransactionsForm


def getTransactions(request):

    if request.method == "POST":


        form = GetTransactionsForm(request.POST)

        if(form.is_valid()):


            partyType = str(form.cleaned_data['partyType'])
            fromDate = form.cleaned_data['fromDate']
            toDate = form.cleaned_data['toDate']
            if(fromDate == toDate):
                fromDate = toDate = None
            # return HttpResponse(fromDate)
            if(partyType == 'Sale'):
                 partyGST = str(form.cleaned_data['party'])#.split(":")[1]


            else:
                 partyGST = str(form.cleaned_data['party2'])#.split(":")[1]

            records = Transaction.objects.all().filter(partyType = partyType, partyGST = partyGST, transactionDate__gte=fromDate, transactionDate__lte=toDate).order_by('-transactionDate')
            rec = []
            for i in records:
                    bill = {}
                    bill['ref'] = i.ref
                    bill['transactionDate'] = i.transactionDate
                    bill['crdr'] = i.crdr
                    bill['amount'] = i.amount
                    rec.append(bill)
            #
            if(partyType == 'Sale'):
                #  partyGST = str(form.cleaned_data['party'])#.split(":")[1]
                # return HttpResponse(partyGST)
                bills=SaleModel.objects.all().filter(custGST=str(partyGST).split(":")[1], invoiceDate__gte=fromDate, invoiceDate__lte=toDate).order_by("-invoiceNumber")

                records2 = []
                for i in bills:
                    bill = {}
                    bill['ref'] = str(i.invoiceNumber) + " " + str(i.itemName)
                    bill['transactionDate'] = i.invoiceDate
                    bill['crdr'] = 'CR'
                    bill['amount'] = i.total



                    records2.append(bill)


                totalCredit = sum([int(x['amount'])  for x in records2])
                totalDebit = sum([int(x.amount)  for x in records])
            else:
                # partyGST = str(form.cleaned_data['party2'])#.split(":")[1]

                bills=PurchaseModel.objects.all().filter(sellerGST=str(str(partyGST).split(":")[1]), invoicedate__gte=fromDate, invoicedate__lte=toDate).order_by("-invoicedate")
                records2 = []
                for i in bills:
                    bill = {}
                    bill['ref'] = str(i.invoiceNumber) + " " + str(i.itemName)
                    bill['transactionDate'] = i.invoicedate
                    bill['crdr'] = 'Dr'
                    bill['amount'] = i.totalAmount



                    records2.append(bill)

                totalDebit = sum([int(x['amount'])  for x in records2])
                totalCredit = sum([int(x.amount)  for x in records])
        records2 = records2 + rec
        records2.sort(reverse = True, key = lambda x:x['transactionDate'])

        return render(request, "transactions.html", {'party':partyGST, 'transactions':records2,'totalCredit':totalCredit, 'totalDebit':totalDebit   })


    else:
        form = GetTransactionsForm
        return render(request, "getTransactions.html", {'form':form})

from .forms import VerifyPin
def getActions(request, pk):
    saleOrPurchase="S"
    if request.method == "POST":
        form = VerifyPin(request.POST)
        if form.is_valid():
            givenPin = form['pin'].value()
            # return HttpResponse(givenPin, type(givenPin))
            if(int(givenPin) == 1803):
                # return redirect("/Actions/", saleOrPurchase = saleOrPurchase, pk = pk)
                return redirect("/Actions/type="+saleOrPurchase+"/"+str(pk))


    else:
        form = VerifyPin()

        return render(request, "getActions.html",{"form":form})



from django.views.generic.edit import UpdateView, DeleteView

# Relative import of GeeksModel
# from .models import GeeksModel

class SaleUpdateView(UpdateView):
    # specify the model you want to use
    model = SaleModel

    # specify the fields
    fields = '__all__'


    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"


class SaleDeleteView(DeleteView):
    # specify the model you want to use
    model = SaleModel

    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"
    template_name = "confirm_delete.html"


def Actions(request, pk, saleOrPurchase):
    if saleOrPurchase == "S":

        bill = SaleModel.objects.get(id = pk)
    else:
        bill = PurchaseModel.objects.get(pk=pk)
    return render(request, "Actions.html", {'bill':bill, 'saleOrPurchase':saleOrPurchase})



def getSaleBill(request, pk):
    global custAddress1
    global custAddress
    global TransportName
    global LR_NO
    global GSTType

    global invoiceNumber
    global finalList
    global subtotal
    global total
    global custDetails
    global Date
    global transportDetails
    global HSN_Code
    global totalFigureNo
    global GSTPERCENTAGE
    global tax
    bill = SaleModel.objects.get(id = pk)
    custName = bill.custName
    try:
                custAddress1 = CustomerModel.objects.values('address1').filter(custName=custName)
                custAddress2 =  CustomerModel.objects.values('address2').filter(custName=custName)
                custEmail =  CustomerModel.objects.values('email_id').filter(custName=custName)
                # return HttpResponse(GSTType, 'hi')
    except Exception as e:
        return HttpResponse(e, 'hi')
            # custAddress1 = form.cleaned_data['custAddress1']
            # custAddress2 = form.cleaned_data['custAddress2']
    custAddress1 = custAddress1[0]['address1']
    custAddress2 = custAddress2[0]['address2']
    # for i in custAddress1:
                # return HttpResponse(i)
            # return HttpResponse(custAddress1, custGST)
    TransportName = bill.transportName
    LR_NO = bill.LR_NO
    GSTType = bill.gstType
    invoiceNumber = bill.invoiceNumber
    finalList = [[bill.itemName, bill.quantity, bill.pricePerUnit, bill.subtotal]]
    subtotal = bill.subtotal
    total = bill.total
    custDetails = [bill.custGST, custName]
    Date = bill.invoiceDate
    transportDetails = [ "GST/Vehicle No.",bill.transportGSTOrVehicleNumber]
    HSN_CODE = bill.HSN_CODE

    totalFigureNo = float(total)
    from num2words import num2words
    totalFigure=num2words(totalFigureNo, to = 'currency', lang='en', currency ='INR'  )

    GSTPERCENTAGE = HSN_CODE_TAX[str(HSN_CODE)]
    tax = round(float(subtotal)*1.0/100*GSTPERCENTAGE, 2)
    if(not GSTType == "IGST"):
        GSTPERCENTAGE /= 2
    GSTPERCENTAGE = int(GSTPERCENTAGE) if GSTPERCENTAGE %  1 == 0 else float(GSTPERCENTAGE)

    return render(request, 'bill.html',{'TransportName': TransportName, 'lrno':LR_NO, 'GSTType':GSTType,'invoiceNumber':invoiceNumber,'finalList' : finalList,
    'subtotal':subtotal ,'total':total, 'tax':tax, 'customerName':custDetails[1],'custGST':custDetails[0], 'totalFigure':totalFigure, 'invoiceDate': Date,'choice': transportDetails[0],
    'custAddress1':custAddress1,'custAddress2':custAddress2, 'choiceInfo':transportDetails[1], 'HSN_CODE':HSN_CODE, 'GSTPERCENTAGE':GSTPERCENTAGE})











