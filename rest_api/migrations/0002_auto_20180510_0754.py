# Generated by Django 2.0.4 on 2018-05-10 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, unique=True)),
                ('country_code', models.CharField(default=None, max_length=50, unique=True)),
                ('currency_code', models.CharField(default=None, max_length=50, unique=True)),
                ('created_at', models.DateField(default=None)),
                ('updated_at', models.DateField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Tariffs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum', models.IntegerField(default=0)),
                ('maximum', models.IntegerField(default=0)),
                ('tariff_type', models.CharField(default=None, max_length=50, unique=True)),
                ('amount', models.IntegerField(default=0)),
                ('created_at', models.DateField(default=None)),
                ('updated_at', models.DateField(default=None)),
            ],
        ),
        migrations.AddField(
            model_name='customers',
            name='country_code',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='forex',
            name='buying',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='forex',
            name='destination',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='forex',
            name='selling',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transactions',
            name='currency',
            field=models.CharField(default=None, max_length=55),
        ),
        migrations.AddField(
            model_name='transactions',
            name='transaction_ref',
            field=models.CharField(default=None, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='usd_amount',
            field=models.IntegerField(default=0),
        ),
    ]
