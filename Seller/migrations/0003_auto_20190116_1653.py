# Generated by Django 2.1.5 on 2019-01-16 08:53

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0002_auto_20190114_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
