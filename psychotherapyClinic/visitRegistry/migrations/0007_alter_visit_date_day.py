# Generated by Django 4.2.7 on 2023-11-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitRegistry', '0006_alter_visit_date_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit_date',
            name='day',
            field=models.CharField(max_length=12),
        ),
    ]
