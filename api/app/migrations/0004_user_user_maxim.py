# Generated by Django 3.2.4 on 2021-07-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_user_user_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_maxim',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='用户座右铭'),
        ),
    ]