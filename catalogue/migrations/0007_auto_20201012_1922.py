# Generated by Django 3.0 on 2020-10-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_bookitem_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookitem',
            name='message',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
