# Generated by Django 5.0.6 on 2024-07-08 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('scraped_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapednews',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='scrapednews',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='accounts.user'),
        ),
    ]