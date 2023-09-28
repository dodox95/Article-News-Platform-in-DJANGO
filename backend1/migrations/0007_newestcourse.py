# Generated by Django 4.2.4 on 2023-09-19 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend1', '0006_editorial_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewestCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField()),
            ],
        ),
    ]