# Generated by Django 2.2.2 on 2020-04-23 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Videoinformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_at', models.TextField()),
                ('video_ID', models.TextField()),
                ('video_title', models.TextField()),
                ('channel_ID', models.TextField()),
                ('channel_title', models.TextField()),
                ('tags', models.TextField()),
                ('video_desciption', models.TextField()),
                ('statics_view_counts', models.IntegerField()),
                ('statics_like_counts', models.IntegerField()),
                ('statics_dislike_counts', models.IntegerField()),
                ('statics_comments_counts', models.IntegerField()),
                ('video_category_ID', models.IntegerField()),
                ('video_category', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usersearcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_object_id', models.IntegerField()),
                ('comment_object_id', models.IntegerField()),
                ('video_ID', models.TextField()),
                ('video_title', models.TextField()),
                ('watching_url', models.TextField()),
                ('key_api', models.TextField()),
                ('content_url_api', models.TextField()),
                ('comments_url_api', models.TextField()),
                ('searching_date_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videoInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comments.Videoinformation')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_object_id', models.IntegerField()),
                ('key_api', models.CharField(max_length=255)),
                ('video_id', models.TextField()),
                ('authorDisplayName', models.TextField()),
                ('authorProfileImageUrl', models.TextField()),
                ('authorChannelUrl', models.TextField()),
                ('textDisplay', models.TextField()),
                ('publishedAt', models.TextField()),
                ('updatedAt', models.TextField()),
                ('numberOfComments', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videoInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comments.Videoinformation')),
            ],
        ),
    ]
