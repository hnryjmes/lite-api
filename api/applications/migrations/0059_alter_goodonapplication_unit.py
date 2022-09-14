# Generated by Django 3.2.15 on 2022-09-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0058_standardapplication_is_mod_security_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goodonapplication",
            name="unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NAR", "Items"),
                    ("TON", "Tonnes"),
                    ("KGM", "Kilograms"),
                    ("GRM", "Grams"),
                    ("MIM", "Milligrams"),
                    ("MCM", "Micrograms"),
                    ("MTR", "Metres"),
                    ("MTK", "Square metres"),
                    ("MTQ", "Cubic metres"),
                    ("LTR", "Litres"),
                    ("MIR", "Millilitres"),
                ],
                default=None,
                max_length=50,
                null=True,
            ),
        ),
    ]
