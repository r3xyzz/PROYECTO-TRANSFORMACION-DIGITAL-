# Generated by Django 5.0.7 on 2024-11-02 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('seccion', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cargo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CSVFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('archivo', models.FileField(upload_to='csvs/')),
                ('subido_el', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReporteFrecuencias',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('evento', models.CharField(db_column='Evento', max_length=50)),
                ('tipo_recurso', models.CharField(db_column='TipoRecurso', max_length=100)),
                ('recursos', models.CharField(db_column='Recursos', max_length=50)),
                ('recursos2', models.CharField(db_column='Recursos2', max_length=100)),
                ('fecha_inicio', models.DateField(db_column='FechaInicio')),
                ('fecha_final', models.DateField(db_column='FechaFinal')),
                ('hora_inicio', models.TimeField(db_column='HoraInicio')),
                ('hora_fin', models.TimeField(db_column='HoraFin')),
                ('cantidad_horas', models.DecimalField(db_column='CtdHoras', decimal_places=2, max_digits=5)),
                ('denominacion_evento', models.CharField(db_column='DenominacionEvento', max_length=100)),
                ('fecha_final_extra', models.DateField(db_column='FechaFinalExtra')),
                ('fecha_inicio_extra', models.DateField(db_column='FechaInicioExtra')),
                ('evento_extra', models.CharField(db_column='EventoExtra', max_length=50)),
                ('recurso_id', models.CharField(db_column='RecursoID', max_length=50)),
                ('tipo_recurso_2', models.CharField(db_column='TipoRecurso2', max_length=50)),
                ('evento2', models.CharField(db_column='Evento2', max_length=50)),
                ('recursos3', models.CharField(db_column='Recursos3', max_length=50)),
                ('tipo_recurso_3', models.CharField(db_column='TipoRecurso3', max_length=50)),
                ('tipo_recurso_4', models.CharField(db_column='TipoRecurso4', max_length=50)),
            ],
            options={
                'db_table': 'reporte_frecuencias',
            },
        ),
        migrations.CreateModel(
            name='Reserva2',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('recursos', models.CharField(db_column='RECURSOS', max_length=100)),
                ('tipo_recurso', models.CharField(db_column='TIPO_RECURSO', max_length=100)),
                ('fecha_inicio', models.DateField(db_column='FECHA_INICIO')),
                ('fecha_final', models.DateField(db_column='FECHA_FINAL')),
                ('hora_inicio', models.TimeField(db_column='HORA_INICIO')),
                ('hora_fin', models.TimeField(db_column='HORA_FINAL')),
                ('correo', models.CharField(db_column='CORREO', max_length=100)),
                ('estado', models.IntegerField(db_column='ESTADO')),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sede', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRecinto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_recinto', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Recinto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_recinto', models.CharField(max_length=100)),
                ('capacidad', models.PositiveIntegerField()),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.categoria')),
                ('id_sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.sede')),
                ('id_tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.tiporecinto')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnombre', models.CharField(max_length=40)),
                ('snombre', models.CharField(max_length=40)),
                ('appaterno', models.CharField(max_length=40)),
                ('apmaterno', models.CharField(max_length=40)),
                ('correo', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=20)),
                ('id_cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hra_inicio', models.CharField(max_length=10)),
                ('hra_fin', models.CharField(max_length=10)),
                ('estado', models.CharField(max_length=30)),
                ('id_asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.asignatura')),
                ('id_recinto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.recinto')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdocente.usuario')),
            ],
        ),
    ]