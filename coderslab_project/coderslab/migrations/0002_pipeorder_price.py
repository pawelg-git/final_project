# Generated by Django 3.1.4 on 2021-01-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderslab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeorder',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
