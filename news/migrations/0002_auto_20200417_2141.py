# Generated by Django 3.0.5 on 2020-04-17 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspost',
            options={'permissions': [('post_without_moderation', 'Can post without moderation')]},
        ),
        migrations.AddField(
            model_name='newspost',
            name='accepted',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.NewsPost'),
        ),
    ]
