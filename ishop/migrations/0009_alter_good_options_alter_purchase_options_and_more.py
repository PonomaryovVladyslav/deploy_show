# Generated by Django 4.0.5 on 2022-06-22 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ishop', '0008_rename_quantity_good_in_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='good',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['-datetime']},
        ),
        migrations.RemoveField(
            model_name='refund',
            name='quantity',
        ),
    ]