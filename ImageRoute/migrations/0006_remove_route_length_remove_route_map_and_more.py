# Generated by Django 5.2 on 2025-04-29 20:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageRoute', '0005_alter_route_owner_backgroundimage_image_delete_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='length',
        ),
        migrations.RemoveField(
            model_name='route',
            name='map',
        ),
        migrations.RemoveField(
            model_name='route',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='route',
            name='route_name',
        ),
        migrations.AddField(
            model_name='route',
            name='background',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ImageRoute.backgroundimage'),
        ),
        migrations.AddField(
            model_name='route',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='route',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RoutePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='ImageRoute.route')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.DeleteModel(
            name='RoutePoints',
        ),
    ]
