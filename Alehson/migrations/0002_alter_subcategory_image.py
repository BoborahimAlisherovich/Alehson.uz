# Generated by Django 5.1.6 on 2025-03-06 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alehson', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(default=1, upload_to='Images/subcategories/'),
            preserve_default=False,
        ),
    ]
