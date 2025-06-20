# Generated by Django 5.2 on 2025-04-29 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageRoute', '0003_map_alter_route_owner_route_map'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Map',
            new_name='BackgroundImage',
        ),
        migrations.CreateModel(
            name='RoutePoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='ImageRoute.route')),
            ],
        ),
    ]
