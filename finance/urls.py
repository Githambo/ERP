from django.urls import path

from .views import download_expense_report, download_finance_report, ExpenseList,ExpenseCreate,InvoiceCreateView, InvoiceListView, InvoiceDeleteView, InvoiceDetailView,InvoiceUpdateView,ReceiptCreateView, ReceiptUpdateView, bulk_invoice
app_name='finance'
urlpatterns = [
    path('list/', InvoiceListView.as_view(), name='invoice-list'),
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('<int:pk>/detail/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('receipt/create', ReceiptCreateView.as_view(), name='receipt-create'),
    path('receipt/<int:pk>/update/', ReceiptUpdateView.as_view(), name='receipt-update'),

    path('bulk-invoice/',  bulk_invoice, name='bulk-invoice'),
    path('expenses',ExpenseList.as_view(),name="expense-list"),
	path('expense_add',ExpenseCreate.as_view(),name="expenses-create"),
    path('report_download',download_finance_report,name='finance-report'),
    path('expense_download',download_expense_report,name='expense-report'),
]
