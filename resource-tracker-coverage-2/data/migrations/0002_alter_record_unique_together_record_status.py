# Generated by Django 4.2.5 on 2024-06-07 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='record',
            unique_together={('psm', 'region', 'domain', 'location')},
        ),
        migrations.AddField(
            model_name='record',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
