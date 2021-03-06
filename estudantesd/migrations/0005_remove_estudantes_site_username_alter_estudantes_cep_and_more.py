# Generated by Django 4.0.4 on 2022-05-14 21:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudantesd', '0004_estudantes_sol_feita_alter_estudantes_cep_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudantes',
            name='site_username',
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='CEP',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='Email',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='Nome',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='RA',
            field=models.CharField(default=None, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='cod_curso',
            field=models.IntegerField(default=None, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='cor',
            field=models.IntegerField(default=None, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='escola',
            field=models.IntegerField(default=None, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='motivacao',
            field=models.IntegerField(default=None, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='renda',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='estudantes',
            name='sexo',
            field=models.IntegerField(default=None, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)]),
        ),
    ]
