# Generated by Django 4.0.4 on 2022-05-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='user', max_length=32, verbose_name='first name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unknown')], default='U', max_length=1, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='user', max_length=32, verbose_name='last name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='123456789', max_length=25, verbose_name='phone number'),
            preserve_default=False,
        ),
    ]
