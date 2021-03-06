# Generated by Django 3.1.6 on 2021-03-06 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20210306_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.event'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='role',
            field=models.CharField(choices=[('Convenor', 'Convenor'), ('Co_Convenor1', 'Co_Convenor1'), ('Co_Convenor2', 'Co_Convenor2'), ('Member1', 'Member1'), ('Member2', 'Member2')], max_length=15),
        ),
    ]
