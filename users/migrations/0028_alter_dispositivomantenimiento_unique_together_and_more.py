# Generated by Django 5.2.1 on 2025-06-20 12:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_backup_mantenimiento_reporte_asignaciondispositivo_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dispositivomantenimiento',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='dispositivomantenimiento',
            name='dispositivo',
        ),
        migrations.RemoveField(
            model_name='dispositivomantenimiento',
            name='mantenimiento',
        ),
        migrations.RemoveField(
            model_name='backup',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='mantenimiento',
            name='dispositivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mantenimientos', to='users.dispositivoinventario', verbose_name='Dispositivo'),
        ),
        migrations.AlterField(
            model_name='dispositivoinventario',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dispositivos_asignados', to=settings.AUTH_USER_MODEL, verbose_name='Usuario asignado'),
        ),
        migrations.DeleteModel(
            name='AsignacionDispositivo',
        ),
        migrations.DeleteModel(
            name='DispositivoMantenimiento',
        ),
    ]
