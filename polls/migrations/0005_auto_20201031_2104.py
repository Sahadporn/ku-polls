# Generated by Django 3.1.2 on 2020-10-31 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0004_auto_20201031_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='value',
        ),
        migrations.AddField(
            model_name='question',
            name='vote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.vote'),
        ),
        migrations.AddField(
            model_name='vote',
            name='question_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
