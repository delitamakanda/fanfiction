# Generated by Django 2.0.2 on 2018-08-23 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20180819_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='logic_value',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]