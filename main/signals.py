import os
import csv
from io import StringIO
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .models import Student, BulkStudentUpload

@receiver(post_save, sender=BulkStudentUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
  if created:
    opened = StringIO(instance.csv_file.read().decode())
    reading = csv.DictReader(opened, delimiter=',')
    students = []
    for row in reading:
      if 'reg_number' in row and row['reg_number']:
        asset_des = row['reg_number']
        tag = row['first_name'] if 'first_name' in row and row['first_name'] else ''
        voucher_number = row['second_name'] if 'second_name' in row and row['second_name'] else ''
        sn = row['surname'] if 'surname' in row and row['surname'] else ''
        
        lcn = row['gender'] if 'gender' in row and row['gender'] else ''
        #ctg = row['category'] if 'category' in row and row['category'] else ''
        #dis = row['date_in_service'] if 'date_in_service' in row and row['date_in_service'] else ''
       
        check = Student.objects.filter(reg_number=asset_des).exists()
        if not check:
          students.append(
            Student(
                reg_number=asset_des,
                first_name=tag,
               
                second_name=voucher_number,
                surname=sn,
                gender=lcn,
                #category=ctg,
                #date_in_service=dis,
                
            )
          )

    Student.objects.bulk_create(students)
    instance.csv_file.close()
    instance.delete()


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(post_delete, sender=BulkStudentUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
  if instance.csv_file:
    _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Student)
def delete_passport_on_delete(sender, instance, *args, **kwargs):

  if instance.passport:

    _delete_file(instance.passport.path)
