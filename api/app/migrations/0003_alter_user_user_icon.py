# Generated by Django 3.2.4 on 2021-07-04 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210703_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_icon',
            field=models.ImageField(blank=True, null=True, upload_to='user_icon', verbose_name='用户头像'),
        ),
    ]
