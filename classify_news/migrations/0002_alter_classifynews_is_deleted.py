

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifynews',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
