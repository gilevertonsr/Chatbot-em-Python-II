# Generated by Django 2.2.5 on 2020-12-02 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('code_user', models.CharField(max_length=15)),
                ('active', models.IntegerField()),
                ('code_relation', models.CharField(max_length=15)),
                ('question', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
            ],
        ),
    ]
