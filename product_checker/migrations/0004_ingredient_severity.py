# Generated by Django 3.2.20 on 2023-11-16 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_checker', '0003_ingredient_country_banned_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='severity',
            field=models.IntegerField(default=0),
        ),
    ]
