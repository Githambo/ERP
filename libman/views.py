from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import BookForm, StudentForm, EmployerForm, IssueForm, ReturnForm,EbookForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Books, Student, Employer, Issue, Return, Semester,Ebook
from django.views.generic import UpdateView, DeleteView,ListView
from django.db.models import Q


# Create your views here.
@login_required
def siteconfig_view(request):
  """ Site Config View """
  if request.method == 'POST' :
    form = SiteConfigForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Configurations successfully updated')
      return HttpResponseRedirect('site-config')
  else:
    form = SiteConfigForm(queryset=SiteConfig.objects.all())

  context = {"formset": form, "title": "Configuration"}
  return render(request, 'main/siteconfig.html', context)


def index(request):
    return render(request, 'libman/home.html')



class BookCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
  form_class = BookForm
  template_name = 'libman/mgt_form.html'
  success_url = reverse_lazy('view_books')
  success_message = 'Book successfully added'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Add new New book'
      return context

        

class BookUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Books
    form_class=BookForm
    
    success_message = "Record successfully updated."
    success_url = reverse_lazy('view_books')
    template_name='libman/book_update.html'

    
class StudentList(LoginRequiredMixin,ListView):
    model=Student

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('main:students-list')









class EbookCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
  form_class = EbookForm
  template_name = 'libman/mgt_form.html'
  success_url = reverse_lazy('view_ebook')
  success_message = 'e-Book successfully added'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Add new New e-book'
      return context











def view_books(request):
    books = Books.objects.order_by('department')
    query = request.GET.get('q')
    if query:
        books = Books.objects.filter(Q(book_name__icontains=query) | Q(author_name__icontains=query) | Q(book_detail__icontains=query) | Q(department__icontains=query))
    else:
        books = Books.objects.order_by('department')
    return render(request, 'libman/view_book.html', {'books': books})

class EbookList(ListView):
    model=Ebook

def view_student(request):
    students = Student.objects.order_by('batch')
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(Q(Fname__icontains=query) | Q(Lname__icontains=query) | Q(phone__icontains=query) | Q(depart__icontains=query) | Q(student_id__icontains=query))
    else:
        students = Student.objects.order_by('batch')
    return render(request, 'libman/view_student.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        s_form = StudentForm(request.POST)
        if s_form.is_valid():
            s_form.save(commit=True)
            return redirect('add_student')
    else:
        s_form = StudentForm()
    return render(request, 'libman/add_student.html', {'s_form': s_form})


def view_employer(request):
    employer = Employer.objects.order_by('timer')
    query = request.GET.get('q')
    if query:
        employer = Employer.objects.filter(Q(Fname__icontains=query) | Q(Lname__icontains=query) | Q(phone__icontains=query) | Q(timer__icontains=query) | Q(emp_id__icontains=query))
    else:
        employer = Employer.objects.order_by('timer')
    return render(request, 'libman/view_employer.html', {'employer': employer})



def add_employer(request):
    if request.method == 'POST':
        e_form = EmployerForm(request.POST)
        if e_form.is_valid():
            e_form.save(commit=True)
            return redirect('add_employer')
    else:
        e_form = EmployerForm()
    return render(request, 'libman/add_employer.html', {'e_form': e_form})

def view_issue(request):
    issue = Issue.objects.order_by('borrower_name', 'issue_date')
    return render(request, 'libman/view_issue.html', {'issue': issue})


def new_issue(request):
    if request.method == 'POST':
        i_form = IssueForm(request.POST)
        if i_form.is_valid():
            name = i_form.cleaned_data['borrower_id']
            book = i_form.cleaned_data['isbn']
            i_form.save(commit=True)
            books = Books.objects.get(isbn_no=book)
            semest = Student.objects.get(student_id=name).semester
            departm = Student.objects.get(student_id=name).depart
            Books.Claimbook(books)
            return redirect('new_issue')
    else:
        i_form = IssueForm()
    semest = None
    departm = None
    sem_book = Semester.objects.filter(sem=semest, depart=departm)
    return render(request, 'libman/new_issue.html', {'i_form': i_form, 'sem_book': sem_book})



def return_book(request):
    if request.method == 'POST':
        r_form = ReturnForm(request.POST)
        if r_form.is_valid():
            r_form.save(commit=True)
            book = r_form.cleaned_data['isbn_no']
            books = Books.objects.get(isbn_no=book)
            b_id = r_form.cleaned_data['borrower_id']
            Books.Addbook(books)
            Issue.objects.filter(borrower_id=b_id, isbn=book).delete()
            return redirect('return_book')
    else:
        r_form = ReturnForm()
    return render(request, 'libman/return_book.html', {'r_form': r_form})

def redir(request):
    return redirect('home')

'''
@login_required(login_url='/login/')
class ViewUpdatePost(UpdateView):
    model = Books
    template_name = 'libman/update_book.html'
    fields = ['book_name', 'author_name', 'book_detail', 'no_of_books']

    def get_object(self, queryset=None):
        isbn_no = self.args['isbn_no']
        return self.model.objects.get(isbn_no=isbn_no)

    def form_valid(self, form):
        form.save()
        return redirect('view_book')
'''
