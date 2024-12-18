# Generated by Django 5.0.2 on 2024-10-23 11:08

import Installation.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Dealer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallatonModels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('MILLER_TRANSPORTER_ID', models.CharField(blank=True, max_length=15)),
                ('MILLER_NAME', models.CharField(blank=True, max_length=200)),
                ('district', models.CharField(blank=True, max_length=200)),
                ('MillerContactNo', models.CharField(blank=True, max_length=15)),
                ('Entity_id', models.CharField(blank=True, max_length=15)),
                ('GPS_IMEI_NO', models.CharField(blank=True, max_length=20)),
                ('SIM_NO', models.CharField(blank=True, max_length=15)),
                ('Device_Name', models.CharField(blank=True, max_length=150)),
                ('NewRenewal', models.CharField(blank=True, max_length=8)),
                ('OTR', models.CharField(blank=True, max_length=5)),
                ('vehicle1', models.CharField(blank=True, max_length=300)),
                ('vehicle2', models.CharField(blank=True, max_length=300)),
                ('vehicle3', models.CharField(blank=True, max_length=300)),
                ('InstallationDate', models.DateField(blank=True, null=True)),
                ('Employee_Name', models.CharField(blank=True, max_length=100)),
                ('Device_Fault', models.CharField(blank=True, max_length=200)),
                ('Fault_Reason', models.CharField(blank=True, max_length=300)),
                ('Replace_DeviceIMEI_NO', models.CharField(blank=True, max_length=20)),
                ('Remark1', models.CharField(blank=True, max_length=350)),
                ('Remark2', models.CharField(blank=True, max_length=350)),
                ('Remark3', models.CharField(blank=True, max_length=350)),
                ('Installation_letterHead', models.FileField(blank=True, default='', null=True, upload_to='installation_letterheads/', validators=[Installation.models.validate_file_extension])),
                ('Dealer_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dealer.dealersmodel')),
            ],
            options={
                'verbose_name': 'Installation Model',
                'verbose_name_plural': 'Installation Models',
            },
        ),
    ]
