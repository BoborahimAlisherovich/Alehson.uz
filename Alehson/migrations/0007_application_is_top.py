# Generated by Django 5.1.6 on 2025-03-10 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alehson', '0006_application_view_count_news_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_top',
            field=models.BooleanField(default=False),
        ),
    ]
