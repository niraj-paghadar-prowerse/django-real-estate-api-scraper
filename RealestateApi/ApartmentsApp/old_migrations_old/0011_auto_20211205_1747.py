# Generated by Django 3.2.9 on 2021-12-05 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ApartmentsApp', '0010_auto_20211205_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartmentstatus',
            old_name='ApartmentID',
            new_name='Apartment',
        ),
        migrations.RenameField(
            model_name='projectavailability',
            old_name='ProjectID',
            new_name='Project',
        ),
    ]
