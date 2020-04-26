# Generated by Django 3.0.5 on 2020-04-26 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0004_user_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='confirmation_number',
            field=models.TextField(max_length=8, validators=[django.core.validators.RegexValidator('[0-9]{8}')]),
        ),
    ]
