# Generated by Django 3.0.5 on 2020-04-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0012_auto_20200426_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(auto_created=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='message_id',
            field=models.IntegerField(auto_created=True, default=None, null=True),
        ),
    ]
