# Generated by Django 5.0.6 on 2024-07-10 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_alter_channel_logo_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='logo_url',
        ),
    ]
