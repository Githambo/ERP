# Generated by Django 3.1.4 on 2021-09-02 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_remove_student_sponsor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='photo',
            new_name='passport',
        ),
    ]
