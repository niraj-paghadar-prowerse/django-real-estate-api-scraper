# Generated by Django 3.2.9 on 2021-12-05 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ApartmentsApp', '0005_auto_20211205_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartments',
            name='Project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ApartmentsApp.projects'),
        ),
    ]
