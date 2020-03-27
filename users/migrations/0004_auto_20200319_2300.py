# Generated by Django 2.2.11 on 2020-03-19 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_auto_20200311_1124"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userorganisationrelationship", options={"default_related_name": "relationship"},
        ),
        migrations.AlterField(
            model_name="userorganisationrelationship",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relationship",
                to="organisations.Organisation",
            ),
        ),
        migrations.AlterField(
            model_name="userorganisationrelationship",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="relationship", to="users.ExporterUser"
            ),
        ),
    ]
