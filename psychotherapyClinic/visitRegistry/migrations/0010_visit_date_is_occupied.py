# Generated by Django 4.2.7 on 2023-11-28 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitRegistry', '0009_rename_confirmed_patient_visit_booked_by_patient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit_date',
            name='is_occupied',
            field=models.BooleanField(default=False),
        ),
    ]