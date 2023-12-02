# Generated by Django 4.2.7 on 2023-12-02 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitRegistry', '0011_rename_is_occupied_visit_date_is_reserved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='visit_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
