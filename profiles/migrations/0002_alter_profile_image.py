# Generated by Django 3.2.4 on 2024-09-09 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../defaultprofile_tffswb', upload_to='images/'),
        ),
    ]
