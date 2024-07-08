# Generated by Django 5.0.6 on 2024-07-08 05:35

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
        migrations.RemoveField(
            model_name='classifynews',
            name='is_faked',
        ),
        migrations.RemoveField(
            model_name='classifynews',
            name='is_fishing',
        ),
        migrations.RemoveField(
            model_name='classifynews',
            name='is_saved',
        ),
        migrations.RemoveField(
            model_name='classifynews',
            name='user_id',
        ),
    ]
