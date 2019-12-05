# Generated by Django 2.2.4 on 2019-12-03 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import users.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("organisations", "0001_initial"),
        ("auth", "0011_update_proxy_permissions"),
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseUser",
            fields=[
                ("first_name", models.CharField(blank=True, max_length=30, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("email", models.EmailField(blank=True, default=None, max_length=254)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False,},
            managers=[("objects", users.models.CustomUserManager()),],
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                ("id", models.CharField(editable=False, max_length=30, primary_key=True, serialize=False)),
                ("name", models.CharField(default="permission - FIX", max_length=80)),
                (
                    "type",
                    models.CharField(
                        choices=[("exporter", "Exporter"), ("internal", "Internal")], default="internal", max_length=30
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, default=None, max_length=30, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("exporter", "Exporter"), ("internal", "Internal")], default="internal", max_length=30
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="organisations.Organisation"
                    ),
                ),
                ("permissions", models.ManyToManyField(related_name="roles", to="users.Permission")),
            ],
        ),
        migrations.CreateModel(
            name="ExporterUser",
            fields=[
                (
                    "baseuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False,},
            bases=("users.baseuser",),
            managers=[("objects", users.models.CustomUserManager()),],
        ),
        migrations.CreateModel(
            name="UserOrganisationRelationship",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Deactivated", "Deactivated")], default="Active", max_length=20
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organisations.Organisation"),
                ),
                (
                    "role",
                    models.ForeignKey(
                        default=uuid.UUID("00000000-0000-0000-0000-000000000004"),
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="exporter_role",
                        to="users.Role",
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.ExporterUser")),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="GovUser",
            fields=[
                (
                    "baseuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Deactivated", "Deactivated")], default="Active", max_length=20
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        default=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="role",
                        to="users.Role",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="team", to="teams.Team"
                    ),
                ),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False,},
            bases=("users.baseuser",),
            managers=[("objects", users.models.CustomUserManager()),],
        ),
    ]
