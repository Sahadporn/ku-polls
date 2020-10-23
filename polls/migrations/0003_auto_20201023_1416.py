# Generated by Django 3.1.2 on 2020-10-23 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20201023_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='vote',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='vote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.vote'),
        ),
        migrations.AddField(
            model_name='vote',
            name='selected_choice_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
