# Generated by Django 3.1.7 on 2021-03-07 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='priority',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
