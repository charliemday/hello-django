# Generated by Django 3.0.9 on 2022-07-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
