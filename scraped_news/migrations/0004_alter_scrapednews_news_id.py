# Generated by Django 5.0.6 on 2024-07-08 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        ('scraped_news', '0003_alter_scrapednews_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapednews',
            name='news_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='news.news'),
        ),
    ]
