
from django import template
register = template.Library()

@register.filter
def div(value, div):
    return round((value / div), 2)


@register.filter
def giveOneMoreArgument(date, field):
    return [date, field]
from ..models import SaleModel, PurchaseModel
@register.filter
def checkDate(date, model):

    month, year = date.month, date.year
    if(model=="SaleModel"):
        j=SaleModel.objects.filter( invoiceDate__month=month , invoiceDate__year=year).order_by('-invoiceDate')[0]
        j=j.invoiceDate
    elif(model=="PurchaseModel"):
       j=PurchaseModel.objects.filter( invoicedate__month=month , invoicedate__year=year).order_by('-invoicedate')[0]
       j=j.invoicedate
    if(j == date):
         return False
    return True
from django.db.models import Sum

@register.filter
def giveSummary(date, model):

    month, year = date[0].month, date[0].year
    if(model=="SaleModel"):
        j=SaleModel.objects.filter( invoiceDate__month=month , invoiceDate__year=year).aggregate(Sum(date[1]))
    elif(model=="PurchaseModel"):
        j=PurchaseModel.objects.filter( invoicedate__month=month , invoicedate__year=year).aggregate(Sum(date[1]))
    else:
        j=PurchaseModel.objects.filter( invoicedate__month=month , invoicedate__year=year).aggregate(Sum(date[1]))
    return round(j[date[1]+"__sum"],2)