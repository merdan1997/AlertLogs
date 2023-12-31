# Generated by Django 4.0.5 on 2023-10-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filterlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=150)),
                ('severity', models.CharField(max_length=50)),
                ('facility', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=70)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('role', models.CharField(max_length=350)),
                ('is_know', models.BooleanField(default=False)),
                ('text_message', models.CharField(blank=True, default=None, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hostnames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=150)),
                ('ipaddress', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('severity_in', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=100)),
                ('index_number', models.CharField(blank=True, max_length=10, null=True)),
                ('split_character', models.CharField(max_length=10)),
                ('start_message', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('severity_out', models.CharField(max_length=10)),
                ('own_text', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]
