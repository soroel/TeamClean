# Generated by Django 5.1.1 on 2024-11-26 15:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('Producer', 'Producer'), ('Recycler', 'Recycler')], max_length=10)),
                ('organization_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WasteListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waste_type', models.CharField(choices=[('Plastic', 'Plastic'), ('Organic', 'Organic'), ('Cardboard', 'Cardboard'), ('E-Waste', 'E-Waste')], max_length=50)),
                ('description', models.TextField()),
                ('quantity', models.FloatField(help_text='Quantity in kilograms or units')),
                ('location', models.CharField(max_length=200)),
                ('availability_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_producer', to='wasteToResource.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(auto_now_add=True)),
                ('recycler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_recycler', to='wasteToResource.profile')),
                ('waste_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wasteToResource.wastelisting')),
            ],
        ),
    ]
