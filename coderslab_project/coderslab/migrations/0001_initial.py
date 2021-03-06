# Generated by Django 3.1.4 on 2021-01-03 11:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PipeOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('size', models.FloatField(choices=[(25.4, 'DN25'), (50.8, 'DN50'), (76.2, 'DN75'), (101.6, 'DN100')], max_length=6)),
                ('wall_thk', models.FloatField(choices=[(0.9, '0.9 mm'), (1.6, '1.6 mm'), (2.0, '2 mm'), (3.2, '3.2 mm')], max_length=6)),
                ('material', models.CharField(choices=[('SS-304', 'SS-316'), ('SS-304', 'SS-304')], max_length=6)),
                ('length', models.IntegerField(validators=[django.core.validators.MaxValueValidator(6000), django.core.validators.MinValueValidator(50)])),
                ('quantity', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1)])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('size', models.FloatField()),
                ('angle', models.FloatField(validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(0)])),
                ('pipe_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderslab.pipeorder')),
            ],
        ),
    ]
