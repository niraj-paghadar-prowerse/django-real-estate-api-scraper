# Generated by Django 3.2.9 on 2021-12-05 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApartmentsApp', '0004_auto_20211205_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='ProjectAvailableApartments',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjectTotalApartments',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]