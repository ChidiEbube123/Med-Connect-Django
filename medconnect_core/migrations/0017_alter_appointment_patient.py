# Generated by Django 5.1 on 2024-10-07 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medconnect_core', '0016_alter_patientprofile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(limit_choices_to={'is_staff': False}, null=True, on_delete=django.db.models.deletion.CASCADE, to='medconnect_core.patientprofile'),
        ),
    ]
