# Generated by Django 5.2.1 on 2025-05-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agritech_app', '0003_profile_accepte_contact_profile_telephone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
