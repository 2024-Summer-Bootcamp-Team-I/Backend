# Generated by Django 5.0.6 on 2024-07-05 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classify_news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classifynews',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='classifynews',
            old_name='delete_at',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='classifynews',
            old_name='update_at',
            new_name='updated_at',
        ),
    ]
