# Generated by Django 2.2.4 on 2021-04-26 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('stocks', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=70)),
                ('company_cap', models.IntegerField(default=0)),
                ('current_price', models.IntegerField(default=0)),
                ('r_o_a', models.IntegerField(default=0)),
                ('p_e', models.IntegerField(default=0)),
                ('efficiency_level', models.IntegerField(default=0)),
                ('date_update', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=16)),
                ('capital', models.CharField(max_length=50)),
                ('avatar', models.ImageField(upload_to='')),
            ],
        ),
    ]
