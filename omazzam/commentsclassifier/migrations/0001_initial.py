# Generated by Django 2.2 on 2020-10-27 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Langclassifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_ObjectID', models.IntegerField()),
                ('comment_objID', models.IntegerField()),
                ('emoji_comment_dic', models.TextField()),
                ('pure_emoji_dic', models.TextField()),
                ('emoji_pure_arabic_dic', models.TextField()),
                ('emoji_pure_english_dic', models.TextField()),
                ('emoji_mixed_lang_dic', models.TextField()),
                ('emoji_arabic_with_others_dic', models.TextField()),
                ('emoji_english_with_others_dic', models.TextField()),
                ('emoji_ar_en_dic', models.TextField()),
                ('emoji_exceptions_dic', models.TextField()),
                ('emoji_other_language_dic', models.TextField()),
                ('emoji_useless_comment_dic', models.TextField()),
                ('pure_arabic_dic', models.TextField()),
                ('pure_english_dic', models.TextField()),
                ('mixed_lang_dic', models.TextField()),
                ('exceptions_dic', models.TextField()),
                ('other_language_dic', models.TextField()),
                ('useless_comment_dic', models.TextField()),
                ('arabic_with_others_dic', models.TextField()),
                ('english_with_others_dic', models.TextField()),
                ('ar_en_dic', models.TextField()),
                ('comment_object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comments.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video_Object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comments.Videoinformation')),
            ],
        ),
        migrations.CreateModel(
            name='Commentclassifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_ObjectID', models.IntegerField()),
                ('comment_objID', models.IntegerField()),
                ('langcommentsclassifier_objID', models.IntegerField()),
                ('emoji_comment_dic', models.TextField()),
                ('pure_emoji_dic', models.TextField()),
                ('emoji_pure_arabic_dic', models.TextField()),
                ('emoji_pure_english_dic', models.TextField()),
                ('emoji_mixed_lang_dic', models.TextField()),
                ('emoji_arabic_with_others_dic', models.TextField()),
                ('emoji_english_with_others_dic', models.TextField()),
                ('emoji_ar_en_dic', models.TextField()),
                ('emoji_exceptions_dic', models.TextField()),
                ('emoji_other_language_dic', models.TextField()),
                ('emoji_useless_comment_dic', models.TextField()),
                ('pure_arabic_dic', models.TextField()),
                ('pure_english_dic', models.TextField()),
                ('mixed_lang_dic', models.TextField()),
                ('exceptions_dic', models.TextField()),
                ('other_language_dic', models.TextField()),
                ('useless_comment_dic', models.TextField()),
                ('arabic_with_others_dic', models.TextField()),
                ('english_with_others_dic', models.TextField()),
                ('ar_en_dic', models.TextField()),
                ('comment_object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comments.Comment')),
                ('langcommentsclassifier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='commentsclassifier.Langclassifier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video_Object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comments.Videoinformation')),
            ],
        ),
    ]
