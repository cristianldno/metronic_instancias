from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class DATOS(models.Model):
    id_conv = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_doc = models.CharField(max_length=100)
    numero_doc = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    tipo_certificado = models.CharField(max_length=100)
    formato_entrega = models.CharField(max_length=100)
    vigencia = models.CharField(max_length=100)
    ocupacion = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    unidad_organizacional = models.CharField(max_length=100)
    token_andesid = models.CharField(max_length=100)
    universidad = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)
    titulo_profesional = models.CharField(max_length=100)
    matricula_profesional = models.CharField(max_length=100)
    
    radicado = models.CharField(max_length=50)
    
    
    
class SOLICITUD_CERT(models.Model):
    id = models.AutoField(primary_key=True)
    id_certificado = models.IntegerField()
    id_convenio = models.IntegerField()
    id_datos = models.IntegerField()
    nombre_cert = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)


    
class TIPO_CERT(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_cert = models.CharField(max_length=100)
    id_convenio = models.IntegerField()

class TipoCertificado(models.Model):
    nombre = models.CharField(max_length=100)

class OperacionCertificado(models.Model):
    nombre = models.CharField(max_length=100)

class OperacionFirmado(models.Model):
    nombre = models.CharField(max_length=100)

class OperacionOTP(models.Model):
    nombre = models.CharField(max_length=100)

class VigenciaCertificado(models.Model):
    duracion = models.CharField(max_length=100)


class FormatoEntrega(models.Model):
    nombre = models.CharField(max_length=100)
class CONVENIO(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    certificados_permi = models.CharField(max_length=100) 
    o_cert_permi = models.CharField(max_length=100)    
    o_firmado_permi = models.CharField(max_length=100)    
    o_otp_permi = models.CharField(max_length=100)    
    vigencias_permi = models.CharField(max_length=100)    
    formatos_entrega_permi = models.CharField(max_length=100)    
    url = models.CharField(max_length=100, null=True)
    color_primario = models.CharField(max_length=100)
    color_secundario = models.CharField(max_length=100)
    id_vigenica = models.IntegerField(null=True)
    id_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CONVENIO')
    
    
    usuario_convenio=models.CharField(max_length=100)

    imagen_banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    contraseña_convenio = models.TextField(blank=True, null=True)
    usuario_weservice = models.CharField(max_length=100, null=True)
    contraseña_webservice = models.CharField(max_length=100, null=True)
    
    tipos_certificado = models.ManyToManyField(TipoCertificado, related_name='convenios')
    operaciones_certificado = models.ManyToManyField(OperacionCertificado, related_name='convenios')
    operaciones_firmado = models.ManyToManyField(OperacionFirmado, related_name='convenios')
    operaciones_otp = models.ManyToManyField(OperacionOTP, related_name='convenios')
    vigencias_certificado = models.ManyToManyField(VigenciaCertificado, related_name='convenios')
    formatos_entrega = models.ManyToManyField(FormatoEntrega, related_name='convenios')
    
    certificados_seleccionados = models.ManyToManyField(TIPO_CERT, related_name='convenios')
    
    def save(self, *args, **kwargs):
        # Generar y guardar la URL automáticamente
        self.url = f'/instancia/{self.nombre.replace(" ", "_").lower()}/'
        super().save(*args, **kwargs)

    

class CONFI_CERTIFICADOS(models.Model):
    id_convenio = models.ForeignKey(CONVENIO, on_delete=models.CASCADE)  # Clave foránea
    tipo_certificado = models.CharField(max_length=255)
    vigencias = ArrayField(models.IntegerField())  # Puede almacenar listas de enteros
    formatos = ArrayField(models.CharField(max_length=255)) 
     

class FORMATO_ENTREGA(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_formato=models.CharField
    id_convenio = models.IntegerField()

    
 
    
class VIGENCIA(models.Model):
    id = models.AutoField(primary_key=True)
    id_cert = models.IntegerField()


