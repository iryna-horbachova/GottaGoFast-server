# Generated by Django 4.0.4 on 2022-05-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='category',
            field=models.CharField(choices=[('E', 'Econom'), ('N', 'Normal'), ('C', 'Comfort')], default='N', max_length=2, verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='type',
            field=models.CharField(choices=[('P', 'Passenger'), ('T', 'Truck'), ('M', 'Minivan')], max_length=2, verbose_name='type'),
        ),
    ]
