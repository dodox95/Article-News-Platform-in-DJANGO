# Generated by Django 4.2.4 on 2023-09-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend1', '0004_remove_news_position_news_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='main_article_position',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Main'), (2, 'Side 1'), (3, 'Side 2')], null=True, unique=True),
        ),
    ]