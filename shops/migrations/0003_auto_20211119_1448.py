# Generated by Django 3.2.9 on 2021-11-19 11:48

from django.db import migrations, models
import django.db.models.deletion
import shops.models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_shopprofilemodel_cover_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addonmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='optiongroupmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='optionmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productgroupmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productgroupmodel',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_groups', to='shops.shopprofilemodel'),
        ),
        migrations.AlterField(
            model_name='productgroupmodel',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productreviewmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='relyon',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shopaddressmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='closes_at',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='cover_photo',
            field=models.ImageField(null=True, upload_to=shops.models.shop_photo_upload),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='currency',
            field=models.CharField(choices=[('$', 'Dollar'), ('€', 'Euro'), ('egp', 'Egyptian Pound')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='delivery_fee',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='opens_at',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='phone_number',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to=shops.models.shop_photo_upload),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='shop_type',
            field=models.CharField(choices=[('F', 'Food'), ('G', 'Groceries'), ('P', 'Pharmacy')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='shopprofilemodel',
            name='time_to_prepare',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shopreviewmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shoptagsmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shoptagsmodel',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='shops.shopprofilemodel'),
        ),
        migrations.AlterField(
            model_name='shoptagsmodel',
            name='tag',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
