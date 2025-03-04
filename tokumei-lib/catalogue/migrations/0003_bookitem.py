# Generated by Django 3.0 on 2020-10-10 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0002_auto_20201009_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(max_length=10, unique=True)),
                ('location', models.CharField(choices=[('1/F Collection', '1/F Collection'), ('2/F Collection', '2/F Collection'), ('3/F Collection', '3/F Collection'), ('1/F Reference Section', '1/F Reference Section')], max_length=25)),
                ('callno', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('available', 'available'), ('checked-out', 'checked-out'), ('on holdshelf', 'on holdshelf'), ('lib use only', 'lib use only'), ('in purchase', 'in purchase'), ('in process', 'in process'), ('library display', 'library display'), ('lost', 'lost'), ('withdrawn', 'withdrawn')], max_length=25)),
                ('duedate', models.DateField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('current_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_in_use', to=settings.AUTH_USER_MODEL)),
                ('previous_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_previous_use', to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Booktitle')),
            ],
        ),
    ]
