# Generated by Django 5.1.1 on 2024-10-25 19:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_comment_options_alter_follow_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='like',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Follow', 'verbose_name_plural': 'Follows'},
        ),
        migrations.RemoveIndex(
            model_name='follow',
            name='core_follow_followe_db4ef4_idx',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', through='core.Follow', to=settings.AUTH_USER_MODEL, verbose_name='Seguindo'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_relations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_relations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]