# Generated by Django 2.2.4 on 2019-09-18 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0002_auto_20190628_1252'),
        ('goodstype', '0002_goodstype_flags'),
        ('parties', '0001_initial'),
        ('goods', '0001_initial'),
        ('users', '0007_delete_govuserrevisionmeta'),
        ('denial_reasons', '0001_initial'),
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advice',
            name='consignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consignee', to='parties.Consignee'),
        ),
        migrations.AddField(
            model_name='advice',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='countries.Country'),
        ),
        migrations.AddField(
            model_name='advice',
            name='denial_reasons',
            field=models.ManyToManyField(to='denial_reasons.DenialReason'),
        ),
        migrations.AddField(
            model_name='advice',
            name='end_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parties.EndUser'),
        ),
        migrations.AddField(
            model_name='advice',
            name='good',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.Good'),
        ),
        migrations.AddField(
            model_name='advice',
            name='goods_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goodstype.GoodsType'),
        ),
        migrations.AddField(
            model_name='advice',
            name='third_party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='third_party', to='parties.ThirdParty'),
        ),
        migrations.AddField(
            model_name='advice',
            name='ultimate_end_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ultimate_end_user', to='parties.UltimateEndUser'),
        ),
        migrations.AddField(
            model_name='advice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.GovUser'),
        ),
        migrations.AddField(
            model_name='caseactivity',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case'),
        ),
    ]
