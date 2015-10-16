# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('date_time_begin', models.DateTimeField(db_index=True)),
                ('date_time_end', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('url', models.URLField()),
                ('description', models.TextField(null=True, blank=True)),
                ('published', models.BooleanField(default=False, db_index=True)),
                ('canceled', models.BooleanField(default=False)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('street', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('historized_since', models.DateTimeField(db_index=True, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'images', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('name', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=500)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TweetedEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', models.CharField(max_length=500)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=1, choices=[(b'S', 'Short Term'), (b'L', 'Long Term')])),
                ('event', models.ForeignKey(to='techism.Event')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='tags',
            field=models.ManyToManyField(to='techism.OrganizationTag'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, to='techism.Location', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(blank=True, to='techism.Organization', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(to='techism.EventTag'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
