# Generated by Django 2.2.16 on 2020-12-05 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0024_auto_20201204_0309'),
        ('users', '0014_auto_20200907_1234'),
        ('documents', '0001_initial'),
        ('applications', '0040_goodonapplication_firearm_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodOnApplicationDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_document', to='applications.BaseApplication')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_on_application_document', to='goods.Good')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.ExporterUser')),
            ],
            options={
                'abstract': False,
            },
            bases=('documents.document',),
        ),
    ]
