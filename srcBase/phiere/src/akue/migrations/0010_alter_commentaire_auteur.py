# Generated by Django 4.1.7 on 2023-04-05 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('akue', '0009_remove_article_titre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
