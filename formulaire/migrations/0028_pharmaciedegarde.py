# Generated by Django 4.1.10 on 2023-09-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulaire', '0027_alter_formulaire_utilisateurr_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='PharmacieDeGarde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Plage', models.CharField(max_length=100)),
                ('Pharmacie', models.CharField(max_length=200)),
                ('Téléphone1', models.CharField(max_length=20)),
                ('Téléphone2', models.CharField(max_length=20)),
                ('Téléphone3', models.CharField(max_length=20)),
                ('Localisation', models.CharField(max_length=200)),
            ],
        ),
    ]