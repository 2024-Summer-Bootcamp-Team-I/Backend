# Generated by Django 4.2.14 on 2024-07-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_news_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='summarize',
            field=models.TextField(default=None),
        ),
    ]