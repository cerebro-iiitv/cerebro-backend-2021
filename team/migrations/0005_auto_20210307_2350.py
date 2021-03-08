# Generated by Django 3.1.7 on 2021-03-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_auto_20210306_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='priority',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='role',
            field=models.CharField(choices=[('Student Convenor', 'Student Convenor'), ('Technical Lead', 'Technical Lead'), ('Convenor', 'Convenor'), ('Head', 'Head'), ('Co-Head', 'Co-Head'), ('Member', 'Member')], max_length=100),
        ),
    ]
