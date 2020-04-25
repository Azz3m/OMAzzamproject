# Generated by Django 2.2.2 on 2020-04-23 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commentsclassifier', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='langclassifier',
            old_name='ar_en_list',
            new_name='ar_en_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='arabic_with_others_list',
            new_name='arabic_with_others_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_ar_en_list',
            new_name='emoji_ar_en_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_arabic_with_others_list',
            new_name='emoji_arabic_with_others_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_comment_list',
            new_name='emoji_comment_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_english_with_others_list',
            new_name='emoji_english_with_others_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_exceptions_list',
            new_name='emoji_exceptions_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_mixed_lang_list',
            new_name='emoji_mixed_lang_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_other_language_list',
            new_name='emoji_other_language_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_pure_arabic_list',
            new_name='emoji_pure_arabic_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_pure_english_list',
            new_name='emoji_pure_english_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='emoji_useless_comment_list',
            new_name='emoji_useless_comment_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='english_with_others_list',
            new_name='english_with_others_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='exceptions_list',
            new_name='exceptions_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='mixed_lang_list',
            new_name='mixed_lang_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='other_language_list',
            new_name='other_language_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='pure_arabic_list',
            new_name='pure_arabic_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='pure_emoji_list',
            new_name='pure_emoji_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='pure_english_list',
            new_name='pure_english_dic',
        ),
        migrations.RenameField(
            model_name='langclassifier',
            old_name='useless_comment_list',
            new_name='useless_comment_dic',
        ),
    ]
