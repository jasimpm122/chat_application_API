# Generated by Django 5.0.2 on 2024-02-19 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note_taking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='modified_at',
            field=models.DateField(auto_now=True),
        ),
    ]
