# Generated by Django 5.1.1 on 2024-10-31 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_tweet_likes_alter_follow_followed_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created_at'], name='core_commen_created_97080c_idx'),
        ),
    ]