# Generated by Django 4.2.11 on 2024-03-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_blogpost_accommodation_alter_blogpost_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
