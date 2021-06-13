# Generated by Django 3.2.4 on 2021-06-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210606_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compileinfo',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='contestproblem',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='custominput',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='loginlog',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='online',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='password',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='problems',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='reply',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='runtimeinfo',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='sim',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='solution',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='sourcecode',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='loginlog',
            name='login_way',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='登录方法'),
        ),
        migrations.AlterModelTable(
            name='compileinfo',
            table='compile_info',
        ),
        migrations.AlterModelTable(
            name='contest',
            table='contest',
        ),
        migrations.AlterModelTable(
            name='contestproblem',
            table='contest_problem',
        ),
        migrations.AlterModelTable(
            name='custominput',
            table='custom_input',
        ),
        migrations.AlterModelTable(
            name='loginlog',
            table='login_log',
        ),
        migrations.AlterModelTable(
            name='news',
            table='news',
        ),
        migrations.AlterModelTable(
            name='online',
            table='online',
        ),
        migrations.AlterModelTable(
            name='password',
            table='password',
        ),
        migrations.AlterModelTable(
            name='problems',
            table='problems',
        ),
        migrations.AlterModelTable(
            name='reply',
            table='reply',
        ),
        migrations.AlterModelTable(
            name='runtimeinfo',
            table='runtime_info',
        ),
        migrations.AlterModelTable(
            name='sim',
            table='sim',
        ),
        migrations.AlterModelTable(
            name='solution',
            table='solution',
        ),
        migrations.AlterModelTable(
            name='sourcecode',
            table='source_code',
        ),
        migrations.AlterModelTable(
            name='team',
            table='team',
        ),
        migrations.AlterModelTable(
            name='topic',
            table='topic',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]