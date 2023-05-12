# Generated by Django 4.0.2 on 2022-12-27 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('author', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('contact_info', models.CharField(blank=True, max_length=20, null=True)),
                ('datePost', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/')),
                ('repuPost', models.BooleanField(default=False)),
                ('fbPost', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-datePost',),
            },
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='posts/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
