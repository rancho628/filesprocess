# Generated by Django 2.2.4 on 2019-08-31 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legalfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]