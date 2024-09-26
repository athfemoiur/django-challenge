# Generated by Django 4.2.2 on 2024-09-26 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0003_rename_reserver_by_seatassignment_reserved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatassignment',
            name='reserved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reserved_seats', to=settings.AUTH_USER_MODEL),
        ),
    ]
