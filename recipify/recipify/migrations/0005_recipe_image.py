# Generated by Django 4.2.11 on 2024-06-21 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipify', '0004_recipe_nutrients_absent_recipe_nutrients_present'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipify.foodimage'),
        ),
    ]
