from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import widgets
from django.urls import reverse_lazy
from django.http import HttpResponse
import csv


from main.models import Student
from .models import Invoice, InvoiceItem, Receipt,Expense
from .forms import InvoiceItemFormset, InvoiceReceiptFormSet, Invoices,ExpenseForm

class InvoiceListView(LoginRequiredMixin, ListView):
  model = Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = '__all__'
    success_url = '/finance/list'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = InvoiceItemFormset(
                self.request.POST, prefix='invoiceitem_set')
        else:
            context['items'] = InvoiceItemFormset(prefix='invoiceitem_set')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['items']
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['receipts'] = Receipt.objects.filter(invoice=self.object)
        context['items'] = InvoiceItem.objects.filter(invoice=self.object)
        return context


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ['student', 'session', 'term',
              'class_for', 'balance_from_previous_term']

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
          context['receipts'] = InvoiceReceiptFormSet(
              self.request.POST, instance=self.object)
          context['items'] = InvoiceItemFormset(
              self.request.POST, instance=self.object)
        else:
          context['receipts'] = InvoiceReceiptFormSet(instance=self.object)
          context['items'] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self, form):
      context = self.get_context_data()
      formset = context['receipts']
      itemsformset = context['items']
      if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
        form.save()
        formset.save()
        itemsformset.save()
      return super().form_valid(form)



class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice-list')


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipt
    fields = ['amount_paid', 'date_paid', 'comment']
    success_url = reverse_lazy('invoice-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        obj.invoice = invoice
        obj.save()
        return redirect('finance:invoice-list')

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        context['invoice'] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ['amount_paid', 'date_paid', 'comment']
    success_url = reverse_lazy('invoice-list')


class ReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy('invoice-list')

@login_required
def bulk_invoice(request):
    return render(request, 'finance/bulk_invoice.html')


class ExpenseList(ListView):
    model=Expense


class ExpenseCreate(CreateView):
    form_class=ExpenseForm
    template_name='finance/expense_create.html'

    def form_valid(self,request):
        if self.request.method=='POST':
            form=ExpenseForm(self.request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("expense added ")
            return render(request,self.template_name,{'form':form})
        else:
            form=ExpenseForm()


def download_finance_report(request):  
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename="finance_report.csv"'
    report=Invoice.objects.all()
    writer=csv.writer(response)
    writer.writerow(['STUDENT','ACADEMIC_YEAR','TERM','TOTAL_PAYABLE','TOTAL PAID',' BALANCE'])

    for rows in report:
        writer.writerow([rows.student,rows.year,rows.month,rows.total_amount_payable() ,rows.total_amount_paid(),rows.balance()])

    return response


def download_expense_report(request):  
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename="expense_report.csv"'
    report=Expense.objects.all()
    writer=csv.writer(response)
    writer.writerow(['CATEGORY','AMOUNT','DATE'])

    for rows in report:
        writer.writerow([rows.category,rows.amount,rows.date_incurred])

    return response