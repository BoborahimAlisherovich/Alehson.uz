# Generated by Django 5.1.6 on 2025-03-07 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alehson', '0003_remove_application_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
