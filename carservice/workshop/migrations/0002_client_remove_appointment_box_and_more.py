# Generated by Django 5.1.4 on 2024-12-08 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя клиента')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='Телефон')),
                ('discount', models.PositiveIntegerField(default=0, verbose_name='Скидка (%)')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='box',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='mechanic',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='service',
        ),
        migrations.AlterModelOptions(
            name='box',
            options={'verbose_name': 'Бокс', 'verbose_name_plural': 'Боксы'},
        ),
        migrations.AlterModelOptions(
            name='mechanic',
            options={'verbose_name': 'Мастер', 'verbose_name_plural': 'Мастера'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['name'], 'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.RemoveField(
            model_name='box',
            name='name',
        ),
        migrations.AddField(
            model_name='box',
            name='available_spots',
            field=models.PositiveIntegerField(default=2, verbose_name='Доступные места'),
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.TextField(default=1, verbose_name='Описание услуги'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='duration',
            field=models.PositiveIntegerField(default=60, verbose_name='Длительность (мин.)'),
        ),
        migrations.AlterField(
            model_name='box',
            name='number',
            field=models.PositiveIntegerField(verbose_name='Номер бокса'),
        ),
        migrations.AlterField(
            model_name='mechanic',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя мастера'),
        ),
        migrations.AlterField(
            model_name='mechanic',
            name='specialty',
            field=models.CharField(max_length=100, verbose_name='Специализация'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название услуги'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='CarRepairBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_time', models.DateTimeField(verbose_name='Время записи')),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='workshop.box', verbose_name='Бокс')),
                ('mechanic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='workshop.mechanic', verbose_name='Мастер')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='workshop.service', verbose_name='Услуга')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='workshop.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Запись на ремонт',
                'verbose_name_plural': 'Записи на ремонт',
                'ordering': ['booking_time'],
            },
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]
