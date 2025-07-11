# Generated by Django 5.1.5 on 2025-04-23 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webpanel", "0015_remove_server_query_protocol_game_query_protocol"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="default_query_port_key",
            field=models.CharField(
                blank=True,
                help_text="Default key (e.g., '27015/udp' or '27910') used for status queries within the Server's port mappings.",
                max_length=20,
                null=True,
            ),
        ),
    ]
