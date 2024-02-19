# Generated by Django 5.0.2 on 2024-02-19 11:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note_taking_app', '0003_note_shared_users_alter_note_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='modified_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
