# Generated by Django 4.2.7 on 2023-11-25 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitRegistry', '0002_rename_user_id_patient_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit_date',
            name='day',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
