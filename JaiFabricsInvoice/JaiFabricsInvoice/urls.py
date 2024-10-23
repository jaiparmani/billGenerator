"""JaiFabricsInvoice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from InvoiceGeneration import views
from django.views.i18n import JavaScriptCatalog

from django.urls import path

urlpatterns = [
  path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'saleDetailForm', views.saleDetailForm, name = 'saleDetailForm'),
    # url(r'saleTotal', views.saleTotal.as_view(), name = 'saleTotal'),
    url(r'saleTotal', views.saleTotal.as_view(), name = 'saleTotal'),
    
    url(r'purchaseTotal', views.purchaseTotal.as_view(), name = 'purchaseTotal'),
    url(r'AddSeller', views.AddSeller, name = 'AddSeller'),

url(r'AddPurchace', views.AddPurchase, name = 'AddPurchase'),
url(r'AddCustomer', views.AddCustomer, name = 'AddCustomer'),

url(r'SecurityForm', views.SecurityForm, name = 'SecurityForm'),
    url(r'finalBill', views.FinalBill, name="finalBill"),
    url(r"^$", views.BasePage.as_view(), name="BasePage"),
    url("form/", views.BillInfo, name = "BillInfo"),
    path('admin/', admin.site.urls),
    url("details/", views.CustomerAndNumberOfItems, name = "Form"),
    url("GenerateBill", views.GenerateBill, name="GenerateBill"),
    url("salePartyWise", views.salePartyWise, name="salePartyWise"),
    url("generateLetter", views.generateLetter, name="generateLetter"),

#   url("getExcelSales", views.getExcelSale, name="getSale"),
    url("purchasePartyWise", views.purchasePartyWise, name="purchasePartyWise"),

    url("addTransaction", views.addTransactions, name="addTransactions"),
    url("getTransactions", views.getTransactions, name="getTransactions"),

    path('getActions/<str:pk>/', views.getActions, name="getActions"),
    path('Actions/type=<str:saleOrPurchase>/<str:pk>', views.Actions, name="Actions"),
    path("Actions/", views.Actions),
    path("updateBill/<str:pk>/", views.SaleUpdateView.as_view(), name="updateBill"),
        path("deleteBill/<str:pk>/", views.SaleDeleteView.as_view(), name="deleteBill"),
 path("getSaleBill/<str:pk>/", views.getSaleBill, name="getBill"),

    # url("updateSale", views.getTransactions, name="getTransactions"),

]
