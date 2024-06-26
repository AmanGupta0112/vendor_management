# Generated by Django 5.0.3 on 2024-04-28 16:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vm", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendor",
            name="average_response_time",
        ),
        migrations.RemoveField(
            model_name="vendor",
            name="fulfillment_rate",
        ),
        migrations.RemoveField(
            model_name="vendor",
            name="on_time_delivery_rate",
        ),
        migrations.RemoveField(
            model_name="vendor",
            name="quality_rating_avg",
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="delivery_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now
            ),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="order_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("completed", "Completed"),
                    ("acknowledged", "Acknowledged"),
                ],
                db_index=True,
                default="draft",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="HistoricalPerformance",
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
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("on_time_delivery_rate", models.FloatField(default=0)),
                ("quality_rating_avg", models.FloatField(default=0)),
                ("average_response_time", models.FloatField(default=0)),
                ("fulfillment_rate", models.FloatField(default=0)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vm.vendor"
                    ),
                ),
            ],
        ),
    ]
