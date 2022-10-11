# Generated by Django 4.0.6 on 2022-07-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='city',
            field=models.CharField(choices=[(29, 'Ha Noi'), (90, 'Ha Nam')], default='Choose', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.IntegerField(),
        ),
    ]