# Generated by Django 2.2.3 on 2019-08-15 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legalfiles', '0006_auto_20190815_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='txts',
        ),
        migrations.AddField(
            model_name='txt',
            name='users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
