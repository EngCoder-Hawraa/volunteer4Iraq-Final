# Generated by Django 3.1.2 on 2021-12-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iraq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='gender',
            field=models.CharField(max_length=255),
        ),
    ]
