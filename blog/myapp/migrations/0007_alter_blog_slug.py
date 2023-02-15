# Generated by Django 4.1.1 on 2023-02-14 05:04

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0006_alter_blog_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False, populate_from="<django.db.models.fields.CharField>"
            ),
        ),
    ]
