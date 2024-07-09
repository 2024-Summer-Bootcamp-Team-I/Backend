

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('news_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('category', models.CharField(max_length=20)),
                ('published_date', models.DateField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='news', to='channels.channel')),
            ],
        ),
    ]
