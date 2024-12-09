# Generated by Django 5.1.4 on 2024-12-08 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "user_auth",
            "0002_alter_doctorprofile_city_alter_doctorprofile_degree_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="doctorprofile",
            old_name="degree",
            new_name="other_speciality",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="designation",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="hospital_clinic",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="institute",
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="areas_of_interest",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="category",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="experiences",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="qualifications",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="doctorprofile",
            name="speciality",
            field=models.CharField(default="Dermatologist", max_length=100),
        ),
    ]
