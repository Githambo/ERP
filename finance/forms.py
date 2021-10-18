from django.forms import inlineformset_factory, modelformset_factory

from corecode.models import AcademicSession, AcademicTerm, StudentClass
from .models import Invoice, InvoiceItem, Receipt,Expense
from django import forms
InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=['description', 'amount'], extra=1, can_delete=True)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice, Receipt, fields=('amount_paid', 'date_paid', 'comment'), extra=0, can_delete=True
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)


		
class ExpenseForm(forms.ModelForm):
	class Meta:
		model=Expense
		fields=("__all__")
		widgets={			
			'date_incurred':forms.DateInput(attrs={'type':'date'}),

		}
