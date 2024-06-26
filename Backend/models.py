# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiStockelement(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField()
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_stockelement'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Cuenta(models.Model):
    usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    carnet_identidad = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='carnet_identidad')

    class Meta:
        managed = False
        db_table = 'cuenta'


class DetalleOrdenCompra(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_orden_compra = models.ForeignKey('OrdenCompra', models.DO_NOTHING, db_column='id_orden_compra')
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detalle_orden_compra'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empleado(models.Model):
    carnet_identidad = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=255)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    id_jefe = models.ForeignKey('self', models.DO_NOTHING, db_column='id_jefe', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleado'


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    cantidad_stock = models.IntegerField()
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'


class OrdenCompra(models.Model):
    fecha_realizada = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'orden_compra'


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=100)
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario', blank=True, null=True)
    stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'producto'


class Reporte(models.Model):
    fecha_reporte = models.DateField()
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado')

    class Meta:
        managed = False
        db_table = 'reporte'


class ReporteInventario(models.Model):
    id = models.OneToOneField(Reporte, models.DO_NOTHING, db_column='id', primary_key=True)
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    cantidad_stock = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'reporte_inventario'


class ReporteVenta(models.Model):
    id = models.OneToOneField(Reporte, models.DO_NOTHING, db_column='id', primary_key=True)
    fecha_hora_entrega = models.DateTimeField()
    id_orden_compra = models.ForeignKey(OrdenCompra, models.DO_NOTHING, db_column='id_orden_compra')
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'reporte_venta'
