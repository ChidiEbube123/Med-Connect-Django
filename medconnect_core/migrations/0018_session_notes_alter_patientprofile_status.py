# Generated by Django 5.1 on 2024-10-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medconnect_core', '0017_alter_appointment_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='status',
            field=models.CharField(blank=True, choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin'), ('Nurse', 'Nurse')], default='Nurse', max_length=100, null=True),
        ),
    ]
