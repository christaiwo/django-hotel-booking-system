# Generated by Django 4.0.4 on 2022-11-10 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(max_length=100, null=True, unique=True)),
                ('check_in', models.DateField(max_length=100, null=True)),
                ('check_out', models.DateField(max_length=100, null=True)),
                ('amount', models.CharField(max_length=100, null=True)),
                ('guest', models.CharField(max_length=10, null=True)),
                ('room', models.CharField(max_length=10, null=True)),
                ('status', models.IntegerField(default=0, null=True)),
                ('date', models.DateTimeField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'booking',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='category/')),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('phone_no', models.CharField(max_length=15, null=True)),
                ('message', models.TextField(max_length=500, null=True)),
                ('date', models.DateTimeField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'contact',
            },
        ),
        migrations.CreateModel(
            name='hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('price', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='hotel/')),
                ('status', models.IntegerField(default=1, null=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.category')),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(editable=False, max_length=100, unique=True)),
                ('issue', models.CharField(max_length=100, null=True)),
                ('priority', models.CharField(max_length=100, null=True)),
                ('message', models.TextField(max_length=1000, null=True)),
                ('date', models.DateTimeField(max_length=100, null=True)),
                ('status', models.IntegerField(default=1, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='ticket_reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=1000, null=True)),
                ('date', models.DateTimeField(max_length=100, null=True)),
                ('ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ticket')),
            ],
            options={
                'db_table': 'ticket_reply',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.CharField(default=0, max_length=100, null=True)),
                ('phone_no', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('user_type', models.IntegerField(default=0, null=True)),
                ('status', models.IntegerField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='hotel_gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='hotel/')),
                ('hotel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.hotel')),
            ],
            options={
                'db_table': 'hotel_gallery',
            },
        ),
        migrations.CreateModel(
            name='canceled_booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(max_length=200, null=True)),
                ('date', models.DateTimeField(max_length=100, null=True)),
                ('status', models.IntegerField(default=0)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.booking')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'canceled_booking',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.hotel'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]