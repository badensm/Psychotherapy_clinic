# Generated by Django 4.2.7 on 2023-11-26 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitRegistry', '0007_alter_visit_date_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='is_confirmed',
            new_name='confirmed_patient',
        ),
        migrations.AddField(
            model_name='visit',
            name='confirmed_therapist',
            field=models.BooleanField(default=False),
        ),
    ]
