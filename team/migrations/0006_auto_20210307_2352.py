# Generated by Django 3.1.7 on 2021-03-07 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_auto_20210307_2350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='dribble',
            new_name='dribbble',
        ),
    ]
