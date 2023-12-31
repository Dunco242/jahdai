# Generated by Django 4.2.5 on 2023-09-28 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('first_aid', 'First Aid'), ('cpr', 'CPR'), ('6m_criminal_record', '6m Criminal Record'), ('1yr_criminal_record', '1yr Criminal Record')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_date', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('overdue', 'Overdue'), ('credit', 'Credit'), ('payment_plan', 'Payment Plan')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent1_f_name', models.CharField(max_length=50)),
                ('parent1_l_name', models.CharField(max_length=50)),
                ('parent2_f_name', models.CharField(blank=True, max_length=50, null=True)),
                ('parent2_l_name', models.CharField(blank=True, max_length=50, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('allergies', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('current', 'Current Student'), ('past', 'Past Student'), ('sick', 'Sick Student')], max_length=10)),
                ('student_fee', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_fee_relation', to='student_management.fee')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('role', models.CharField(max_length=50)),
                ('certs', models.ManyToManyField(blank=True, to='student_management.certification')),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management.student')),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management.student')),
            ],
        ),
        migrations.AddField(
            model_name='fee',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fee_relation', to='student_management.student'),
        ),
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergens', models.TextField()),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student_management.student')),
            ],
        ),
    ]
