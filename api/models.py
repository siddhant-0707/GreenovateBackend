# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Emissionrecord(models.Model):
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    subsubfactor = models.ForeignKey('Subsubfactor', models.DO_NOTHING)
    input_value = models.FloatField()
    record_year = models.IntegerField()
    net_emission = models.FloatField()

    class Meta:
        managed = False
        db_table = 'emissionrecord'


class Factor(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'factor'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'organization'


class Subfactor(models.Model):
    name = models.CharField(max_length=255)
    factor = models.ForeignKey(Factor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subfactor'


class Subsubfactor(models.Model):
    name = models.CharField(max_length=255)
    sub_factor = models.ForeignKey(Subfactor, models.DO_NOTHING)
    emission_factor = models.FloatField()
    description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subsubfactor'

class Tips(models.Model):
    factor = models.ForeignKey(Factor, models.DO_NOTHING)
    tip = models.CharField(max_length=255)
    desc_1 = models.TextField(blank=True, null=True)
    desc_2 = models.TextField(blank=True, null=True)
    desc_3 = models.TextField(blank=True, null=True)
    desc_4 = models.TextField(blank=True, null=True)
    potential_reduction_percentage = models.FloatField()
