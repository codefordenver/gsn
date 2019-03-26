# Generated by Django 2.1.5 on 2019-03-26 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gsndb', '0002_auto_20190221_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='behavior',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gsndb.Course'),
        ),
        migrations.AddField(
            model_name='behavior',
            name='period',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='period',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='referral',
            name='reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='avg_daily_attendance',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsndb.Program'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='program',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='gsndb.Program'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='behavior',
            name='program',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='gsndb.Program'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grade',
            name='program',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='gsndb.Program'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='referral',
            name='program',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='gsndb.Program'),
            preserve_default=False,
        ),
    ]