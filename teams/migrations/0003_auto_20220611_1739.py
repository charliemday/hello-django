# Generated by Django 3.0.9 on 2022-06-11 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_team_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
