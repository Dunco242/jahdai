# Generated by Django 4.2.5 on 2023-10-02 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fee_relation', to='student_management.student'),
        ),
    ]
