# Generated by Django 4.2.8 on 2023-12-31 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0002_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventslot',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='eventApp.event'),
        ),
    ]