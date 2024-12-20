# Generated by Django 4.1.7 on 2023-03-15 23:03

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fanfics', '0006_auto_20210503_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fanfic',
            name='genres',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('RO', 'Romance'), ('SU', 'Surnaturel'), ('ER', 'Erotique'), ('DR', 'Drame'), ('AM', 'Amitié'), ('AC', 'Action-Aventure'), ('SC', 'School-Fic'), ('MY', 'Mystère'), ('GE', 'Général'), ('DCED', "De cape et d'épée"), ('LE', 'Lemon'), ('HU', 'Humour'), ('OS', 'One-Shot'), ('SUS', 'Suspense'), ('TH', 'Thriller'), ('HO', 'Horreur'), ('HF', 'Heroic Fantasy'), ('TR', 'Tragédie'), ('CO', 'Cross-Over')], max_length=255),
        ),
        migrations.AlterField(
            model_name='fanfic',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
