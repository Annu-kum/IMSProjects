# Generated by Django 5.0.2 on 2024-08-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reactivation', '0002_alter_reactivationmodels_dealer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactivationmodels',
            name='Entity_id',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
