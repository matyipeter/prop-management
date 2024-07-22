# Generated by Django 5.0.6 on 2024-07-22 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messaging", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={"ordering": ("timestamp",)},
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.CharField(max_length=255, unique=True)),
                ("client", models.CharField(max_length=255)),
                ("url", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "Waiting"),
                            ("active", "Active"),
                            ("closed", "Closed"),
                        ],
                        default="waiting",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "messages",
                    models.ManyToManyField(
                        blank=True, related_name="rooms", to="messaging.message"
                    ),
                ),
            ],
            options={
                "ordering": ("created_at",),
            },
        ),
    ]