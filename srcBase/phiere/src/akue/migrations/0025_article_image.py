# Generated by Django 4.1.7 on 2023-04-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akue', '0024_commentaireoffre_offre_likeoffre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='akue/static/akue/img/publication_images/'),
        ),
    ]
