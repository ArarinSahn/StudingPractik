from django.db import models

class Application(models.Model):
    id_aplic = models.AutoField(primary_key=True)
    id_con_event = models.ForeignKey('DateConductEvent', models.DO_NOTHING, db_column='id_con_event')
    quantity_sit = models.IntegerField()
    id_pay = models.ForeignKey('PayMethod', models.DO_NOTHING, db_column='id_pay')
    id_ststus = models.ForeignKey('Status', models.DO_NOTHING, db_column='id_ststus')
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')
    review = models.TextField(blank=True, null=True)
    date_create = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Application'
        unique_together = (('id_user', 'id_con_event'),)


class DateConductEvent(models.Model):
    id_con_event = models.AutoField(primary_key=True)
    id_event = models.ForeignKey('Event', models.DO_NOTHING, db_column='id_event')
    date_con = models.DateTimeField()
    max_member = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Date_conduct_event'


class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'Event'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey('Roles', models.DO_NOTHING, db_column='id_rol')
    fio = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Users'
        unique_together = (('email', 'login'),)


class PayMethod(models.Model):
    id_pay = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pay_method'


class Roles(models.Model):
    id_rol = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'roles'


class Status(models.Model):
    id_status = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status'
# Create your models here.
