

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifyNews',
            fields=[
                ('news_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='news.news')),
                ('score', models.IntegerField()),
                ('reason', models.CharField(verbose_name=500)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_deleted', models.BooleanField(null=True)),
            ],
        ),
    ]
