# Generated by Django 5.0.6 on 2024-07-15 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.URLField(null=True),
        ),
    ]