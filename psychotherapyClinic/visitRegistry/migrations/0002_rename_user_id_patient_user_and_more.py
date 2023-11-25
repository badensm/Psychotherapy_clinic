# Generated by Django 4.2.7 on 2023-11-25 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitRegistry', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='therapist',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='visits',
            old_name='patient_id',
            new_name='patient',
        ),
        migrations.RenameField(
            model_name='visits',
            old_name='therapist_id',
            new_name='therapist',
        ),
        migrations.RenameField(
            model_name='visits',
            old_name='visit_date_id',
            new_name='visit_date',
        ),
    ]