# Generated by Django 5.1 on 2024-12-01 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("assistants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
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
                (
                    "title",
                    models.CharField(
                        db_index=True, help_text="Chat title", max_length=128
                    ),
                ),
                (
                    "is_pinned",
                    models.BooleanField(
                        default=False, help_text="Designates if the chat is pinned"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Date created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Last update"),
                ),
                (
                    "assistant",
                    models.ForeignKey(
                        help_text="Assistant (Chat LLM)",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chats",
                        to="assistants.assistant",
                    ),
                ),
            ],
        ),
    ]
