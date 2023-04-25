# Generated by Django 3.2 on 2023-04-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('link', models.TextField()),
                ('imageURL', models.TextField()),
                ('price', models.IntegerField()),
                ('maker', models.TextField()),
                ('category1', models.TextField()),
                ('category2', models.TextField()),
            ],
        ),
    ]
