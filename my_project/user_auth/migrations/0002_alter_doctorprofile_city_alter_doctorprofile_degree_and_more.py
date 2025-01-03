# Generated by Django 5.1.4 on 2024-12-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctorprofile",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="degree",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="designation",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="end_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="fee",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="hospital_clinic",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="hospital_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="institute",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="online_consultation_fee",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="online_days",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="online_end_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="online_start_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="phone_no",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="practice_days",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="review_address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="start_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
