# Generated by Django 4.2.11 on 2024-06-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipify', '0006_dishimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishimage',
            name='image',
            field=models.URLField(),
        ),
    ]
