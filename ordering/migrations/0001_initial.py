# Generated by Django 3.2.7 on 2021-09-07 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cappuccino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='قیمت')),
                ('size', models.CharField(choices=[('small', 'کوچک'), ('medium', 'متوسط'), ('large', 'بزرگ')], max_length=20, verbose_name='اندازه')),
            ],
            options={
                'verbose_name': 'کاپوچینو',
                'verbose_name_plural': 'کاپوچینو ها',
            },
        ),
        migrations.CreateModel(
            name='Chocolate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='قیمت')),
                ('size', models.CharField(choices=[('small', 'کوچک'), ('medium', 'متوسط'), ('large', 'بزرگ')], max_length=20, verbose_name='اندازه')),
            ],
            options={
                'verbose_name': 'شکلات',
                'verbose_name_plural': 'شکلات ها',
            },
        ),
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='قیمت')),
                ('kind', models.CharField(choices=[('chocolate_chip', 'شکلاتی'), ('ginger', 'زنجبیلی')], max_length=20, verbose_name='نوع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Espresso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='قیمت')),
                ('shots', models.CharField(choices=[('single', 'یکی'), ('double', 'دوتا'), ('triple', 'سه تا')], max_length=20, verbose_name='شات')),
            ],
            options={
                'verbose_name': 'اسپرسو',
                'verbose_name_plural': 'اسپرسو ها',
            },
        ),
        migrations.CreateModel(
            name='GenericMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Latte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='قیمت')),
                ('milk', models.CharField(choices=[('skim', 'کم'), ('semi', 'متوسط'), ('whole', 'کامل')], max_length=20, verbose_name='شیر')),
            ],
            options={
                'verbose_name': 'لاته',
                'verbose_name_plural': 'لاته ها',
            },
        ),
        migrations.CreateModel(
            name='Tea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(verbose_name='قیمت')),
            ],
            options={
                'verbose_name': 'چای',
                'verbose_name_plural': 'چای ها',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'در انتظار'), ('preparation', 'آماده سازی'), ('ready', 'آماده شده'), ('delivered', 'تحویل داده شده')], default='waiting', max_length=20, verbose_name='وضعیت')),
                ('consume_location', models.CharField(choices=[('take_away', 'بیرون بر'), ('in_shop', 'در محدوده')], default='in_shop', max_length=20, verbose_name='محل سرو')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering.genericmenuitem')),
            ],
        ),
    ]