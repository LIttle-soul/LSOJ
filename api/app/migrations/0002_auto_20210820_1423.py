# Generated by Django 3.2.6 on 2021-08-20 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balloon',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userpassword', verbose_name='用户账号'),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_user',
            field=models.ManyToManyField(through='app.ClassUser', to='app.UserPassword', verbose_name='班级用户'),
        ),
        migrations.AlterField(
            model_name='classuser',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userpassword', verbose_name='用户账号'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_user',
            field=models.ManyToManyField(blank=True, through='app.ContestUser', to='app.UserPassword', verbose_name='竞赛用户'),
        ),
        migrations.AlterField(
            model_name='contestuser',
            name='contest_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.userpassword', verbose_name='竞赛用户'),
        ),
        migrations.AlterField(
            model_name='limitlogin',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userpassword', verbose_name='用户账号'),
        ),
        migrations.AlterField(
            model_name='loginlog',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.userpassword', verbose_name='登陆用户'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userpassword', verbose_name='用户账号'),
        ),
    ]
