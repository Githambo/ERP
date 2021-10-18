from django.db import models
from django.core.validators import MaxValueValidator, validate_email, ValidationError
import datetime

# Create your models here.
#book table
class Books(models.Model):
    DEPARTMENT = (
        ('COM', 'Computer'),
        ('ELX', 'Electronics'),
        ('CIV', 'Civil'),
        ('BBS', 'Business'),
        ('MSC', 'Miscellaneous'),
    )
    isbn_no = models.CharField(max_length=20, blank=True)
    barcode = models.CharField(max_length=20, unique=True)
    book_id = models.CharField(max_length=20)
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    no_of_books = models.IntegerField()
    book_detail = models.TextField(default='text')
    department = models.CharField(max_length=3, choices=DEPARTMENT)
    publisher = models.CharField(max_length=100)
    rack_no = models.CharField(max_length=3)

    def Claimbook(self):
        if self.no_of_books>1:
            self.no_of_books=self.no_of_books-1
            self.save()
        else:
            print("not enough books to Claim")

    def Addbook(self):
        self.no_of_books=self.no_of_books+1
        self.save()


    def __str__(self):
        return self.book_name

#borrower table
class BORROWER(models.Model):
    Fname = models.CharField(max_length=200)
    Lname = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    phone = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)

    def __str__(self):
        return self.Fname+" "+self.Lname

class Student(BORROWER):
    now = datetime.datetime.now()
    BATCH = [(str(a), str(a)) for a in range(now.year-4, now.year+1)]
    DEPART = (
        ('BEC', 'B. Computer Engineering'),
        ('BIT', 'B. Information Technology'),
        ('BCA', 'B. Computer Application'),
        ('ELX', 'B. Electronics Engineering'),
        ('CIV', 'B. Civil Engineering'),
        ('BBS', 'B. Business Studies'),
        ('MCA', 'M. Computer Application'),
        ('PGD', 'PG. Computer Applications'),
        ('MCJ', 'M. Mass Communication and Journalism'),
    )
    student_id = models.CharField(max_length=20, unique=True)
    batch = models.CharField(max_length=4, choices = BATCH)
    depart = models.CharField(max_length=3, choices = DEPART)
    semester = models.CharField(max_length=1)

    def __str__(self):
        return self.Fname+" "+self.Lname

class Employer(BORROWER):
    TIMER = (
        ('FT', 'Full Timer'),
        ('PT', 'Part Timer'),
    )
    emp_id = models.CharField(max_length=20, unique=True)
    timer = models.CharField(max_length=2, choices = TIMER)

    def __str__(self):
        return self.Fname+" "+self.Lname
class Ebook(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=300)
    document=models.FileField(null=True,upload_to='media/documents/%Y/%m/%d/')
    image=models.ImageField(null=True,upload_to='Cover_images')

    def _str__(self):
        return self.title

class Issue(models.Model):
    borrower_id = models.CharField(max_length=20)
    borrower_name = models.CharField(max_length=100)
    book_name = models.CharField(max_length = 200)
    book_id = models.CharField(max_length=20)
    issue_date = models.DateField(default=datetime.date.today)
    issue_id = models.CharField(max_length=20)
    isbn = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.book_name

class Return(models.Model):
    return_id = models.CharField(max_length=20)
    return_date = models.DateField(default=datetime.date.today)
    borrower_id = models.CharField(max_length=20)
    borrower_name = models.CharField(max_length = 100)
    book_id = models.CharField(max_length=20)
    book_name= models.CharField(max_length=200)
    isbn_no = models.CharField(max_length=20)

    def __str__(self):
        return self.book_name

class Semester(models.Model):
    SEM = (
        ('1', 'first'),
        ('2', 'second'),
        ('3', 'third'),
        ('4', 'fourth'),
        ('5', 'fifth'),
        ('6', 'sixth'),
        ('7', 'seventh'),
        ('8', 'eighth')
    )
    DEPART = (
        ('BEC', 'B. Computer Engineering'),
        ('BIT', 'B. Information Technology'),
        ('BCA', 'B. Computer Application'),
        ('ELX', 'B. Electronics Engineering'),
        ('CIV', 'B. Civil Engineering'),
        ('BBS', 'B. Business Studies'),
        ('MCA', 'M. Computer Application'),
        ('PGD', 'PG. Computer Applications'),
        ('MCJ', 'M. Mass Communication and Journalism'),
    )
    sem = models.CharField(max_length=1)
    depart = models.CharField(max_length=3)
    subject = models.CharField(max_length=30)

    def __str__(self):
        return depart + ' ' + sem
