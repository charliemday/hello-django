# Generated by Django 3.0.9 on 2022-07-24 11:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_teaminvite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminvite',
            name='token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]