# Generated by Django 5.1.1 on 2024-11-01 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Sent Back', 'Sent Back')], default='Pending', max_length=20),
        ),
    ]
