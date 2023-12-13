# Generated by Django 5.0 on 2023-12-13 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=120)),
                ('born_date', models.DateField()),
                ('born_location', models.CharField(max_length=200)),
                ('description', models.CharField()),
            ],
            options={
                'db_table': 'authors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tags',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField()),
                ('author', models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.CASCADE, to='quotes_app.authors')),
                ('tags', models.ManyToManyField(related_name='quotes', to='quotes_app.tags')),
            ],
            options={
                'db_table': 'quotes',
                'managed': True,
            },
        ),
    ]
