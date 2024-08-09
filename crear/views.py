import logging
from django.shortcuts import render

# Create your views here.from http import client
from django.shortcuts import render, redirect
import psycopg2
from suds.client import Client
from django.contrib.auth import authenticate, login
from django.contrib import messages
from dashboards.models import CONFI_CERTIFICADOS, CONVENIO, DATOS
from django.contrib.auth.hashers import make_password
from zeep import Client
import base64
import hashlib
import datetime
import random
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import json
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.template import TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.http import JsonResponse
from django.utils.encoding import force_str
from django.views.decorators.csrf import csrf_exempt
import requests
from requests import Session
import xml.etree.ElementTree as ET
import base64
from zeep import Client, Transport
from zeep.exceptions import TransportError, XMLSyntaxError
from zeep.wsse.username import UsernameToken
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
import hashlib
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
import io
import base64
import zipfile
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.urls import reverse




def login_instancia(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        try:
            convenio = CONVENIO.objects.get(usuario=usuario, contraseña=contraseña)
            return redirect('plantilla_convenio')
        except CONVENIO.DoesNotExist:
             return render(request, 'login_instancia.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login_instancia.html')


def plantilla_convenio(request, id):
    convenio = get_object_or_404(CONVENIO, id=id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})


def detalle_convenio(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})


@never_cache
@login_required
def home(request):
    convenios = CONVENIO.objects.all()
    return render(request, 'home.html', {'convenios': convenios})

def imagen_banner(request):
    convenios = CONVENIO.objects.all()  # Obtén todos los convenios de la base de datos
    return render(request, 'plantilla_convenio.html', {'convenios': convenios})




def plantilla_dinamica(request, nombre):
    mapeo_tipos_certificado = {
    "10": "Facturación Electrónica - Persona Jurídica",
    "11": "Facturación Electrónica - Persona Natural",
    "6": "Comunidad Académica",
    "9": "Pertenencia Empresa",
    "7": "Profesional Titulado",
    "8": "Representante Legal",
    "12": "Función Pública",
    "13": "Persona Jurídica",
    "14": "Función Pública para SIIF Nación",
    "5": "Persona Natural",
    "15": "Persona Natural Para Actividad Comercial(Rut)"
}

    mapeo_certificados_formularios = {
        "10": 'form_fe_pj',
        "11": 'form_fe_pn',
        "6": 'form_com_acad',
        "9": 'form_pert_emp',
        "7": 'form_prof_titu',
        "8": 'form_rep_leg',
        "12": 'form_func_pub',
        "13": 'form_pers_jur',
        "14": 'form_siif_nac',
        "5": 'form_pers_nat',
        "15": 'form_pers_nat_rut'
    }



    mapeo_operacion_cert = {
        "1" : 'consultar',
        "2" : 'revocar',
        "3" : 'cambiar_pin',
        "4" : 'reposicion'

    }

    mapeo_operaciones_firmado = {
        "1" : 'firmar_doc',
        "2" : 'verificar_firma'
    }

    mapeo_operaciones_otp = {
        "1" : 'cambiar_tiempo',
        "2" : 'firmar_otp',
        "3" : 'invalidar'

    }





    convenio = get_object_or_404(CONVENIO, nombre=nombre)
    confi_certificados = CONFI_CERTIFICADOS.objects.filter(id_convenio=convenio.id)

    certificados_con_nombre_y_formulario = [
        {
            'tipo_certificado': mapeo_tipos_certificado.get(str(cert.tipo_certificado), 'Tipo desconocido'),
            'formulario': mapeo_certificados_formularios.get(str(cert.tipo_certificado), '#'),  # Default to '#'
            'detalles_certificado': cert,
        }
        for cert in confi_certificados
    ]

    for cert in confi_certificados:

        print("Tipo de Certificado:", cert.tipo_certificado)

        print("---")

    print("color: ", convenio.color_primario)
    print("Nombre del convenio:", convenio.nombre)
    print("Color primario del convenio:", convenio.color_primario)




    numeros_operacion_cert = convenio.o_cert_permi.split(',') if convenio.o_cert_permi else []
    operaciones_certificado = [mapeo_operacion_cert.get(numero) for numero in numeros_operacion_cert]


    numeros_operaciones_firmado = convenio.o_firmado_permi.split(',') if convenio.o_firmado_permi else []
    operaciones_firmado = [mapeo_operaciones_firmado.get(numero) for numero in numeros_operaciones_firmado]


    numeros_operaciones_otp = convenio.o_otp_permi.split(',') if convenio.o_otp_permi else []
    operaciones_otp = [mapeo_operaciones_otp.get(numero) for numero in numeros_operaciones_otp]

    return render(request, 'plantilla_convenio.html', {
        'convenio': convenio,
        'certificados_con_nombre_y_formulario': certificados_con_nombre_y_formulario,
        'operaciones_certificado': operaciones_certificado,
        'operaciones_firmado': operaciones_firmado,
        'operaciones_otp': operaciones_otp

    })



def formulario_dinamico(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    print("Nombre del convenio for:", convenio.nombre)
    print("Color primario del convenio for:", convenio.color_primario)
    #return render(request, 'form-pers-nat.html', {'convenio': convenio})
    return render(request, 'form-pers-nat.html', {
        'convenio_id': convenio.id,
        'convenio_nombre': convenio.nombre,
    })


def verificar_convenio(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    if convenio.contraseña_convenio:
        return redirect('login_instancia', convenio_id=convenio_id)
    else:
        return render(request, 'plantilla_convenio.html', {'convenio': convenio})

def login_instancia(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    if request.method == 'POST':
        contraseña = request.POST.get('contraseña')
        convenio_valido = CONVENIO.objects.filter(pk=convenio_id, contraseña_webservice=contraseña).first()
        if convenio_valido:
            return redirect('plantilla_convenio', id=convenio_id)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login_instancia.html', {'convenio': convenio})





def consultar(request):
    return render (request, 'consultar_cert.html')

def revocar(request):
    return render (request, 'revocar_cert.html')

def cambiar_pin(request):
    return render (request, 'cambiar_pin.html')

def firmar_doc(request):
    return render (request, 'firmar_documento.html')

def campos_form(request):
    return render(request,'campos-form.html')


def instancia(request):
    return render (request, 'instancia.html')


def form_pers_nat(request):
    return render(request, 'form_pers_nat.html')

def form_pers_jur(request):
    return render (request, 'form_pers_jur.html')

def form_pers_nat_rut(request):
    return render (request, 'form_per_nat_rut.html')

def form_pert_emp(request):
    return render (request, 'form_pert_emp.html')

def form_prof_titu(request):
    return render (request, 'form_prof_titu.html')

def form_fe_pj(request):
    return render (request, '_templates/formularios/form_fe_pj.html')

def form_fe_pn(request):
    return render (request, 'form_fe_pn.html')

def form_func_pub(request):
    return render (request, 'form_func_pub.html')

def form_siif_nac(request):
    return render (request, 'form_siif_nac.html')

def form_com_acad(request):
    return render (request, 'form_com_acad.html')

def form_rep_leg(request):
    return render (request, 'form_rep_leg.html')


def procesar_formulario_convenio(request):
    if request.method == 'POST':
        convenio = CONVENIO(nombre=request.POST['nombre'])
        convenio.save()

        certificados_seleccionados_ids = request.POST.getlist('tipos_certificados')

        for certificado_id in certificados_seleccionados_ids:
            TIPO_CERT = TIPO_CERT.objects.get(pk=certificado_id)
            convenio.certificados_seleccionados.add(TIPO_CERT)

        return render(request, 'tu_template.html', {'convenio': convenio})
    else:
        return render(request, 'tu_formulario.html')



# @csrf_exempt
# def guardar_convenios(request):
#     if request.method == 'POST':
#         data = request.POST.dict()

#         certificados_seleccionados = [key for key, value in data.items() if value == 'on']

#         tipo_certificado = ','.join(certificados_seleccionados)

#         convenio = CONFI_CERTIFICADOS(tipo_certificado=tipo_certificado)
#         convenio.save()

#         return JsonResponse({'message': 'Convenios guardados correctamente.'})

#     return JsonResponse({'error': 'Se esperaba una solicitud POST.'}, status=400)

def instancia_empresa(request, nombre_empresa):
    template_name = f'instancia_empresas/{nombre_empresa}.html'
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError(f'Error: La plantilla "{template_name}" no existe.')



@csrf_exempt
def crear_instancia(request):
    if request.method == 'POST':
        try:
            # Extraer datos del formulario para crear el convenio
            nombre = request.POST.get('nombre')
            logo = request.FILES.get('logo')
            url = request.POST.get('url')
            color_primario = request.POST.get('colorPrimario')
            color_secundario = request.POST.get('colorSecundario')
            id_vigenica = request.POST.get('id_vigenica')
            imagen_banner = request.FILES.get('imagenBanner')
            usuario_weservice = request.POST.get('usuario_weservice')
            usuario_convenio = request.POST.get('usuario_convenio')
            contraseña_webservice = request.POST.get('contraseña_webservice')
            contraseña_convenio = request.POST.get('contraseña')

            # Encriptar la contraseña del convenio
            contraseña_convenio_encriptada = make_password(contraseña_convenio)

            # Extraer datos de certificados del formulario
            certificado_persona_natural = request.POST.get('certificado_persona_natural')
            certificado_persona_juridica = request.POST.get('certificado_persona_juridica')
            certificado_pertenencia_empresa = request.POST.get('certificado_pertenencia_empresa')
            certificado_Comunidada_Académica = request.POST.get('certificado_Comunidada_Académica')
            certificado_Función_Publica_SIIF_Nación = request.POST.get('certificado_Función_Publica_SIIF_Nación')
            certificado_Profesional_Titulado = request.POST.get('certificado_Profesional_Titulado')
            certificado_Persona_Natural_Con_RUT = request.POST.get('certificado_Persona_Natural_Con_RUT')
            certificado_Facturacion_Electronica_Persona_JurÍdica = request.POST.get('certificado_Facturacion_Electronica_Persona_JurÍdica')
            certificado_Facturacion_Electronica_Persona_Natural = request.POST.get('certificado_Facturacion_Electronica_Persona_Natural')
            certificado_Funcion_Publica = request.POST.get('certificado_Funcion_Publica')
            certificado_Representante_Legal = request.POST.get('certificado_Representante_Legal')

            consultar_certificado = request.POST.get('consultar_certificado')
            revocar_certificado = request.POST.get('revocar_certificado')
            cambiar_pin = request.POST.get('cambiar_pin')
            reposicion_certificado = request.POST.get('reposicion_certificado')

            firmar_documento = request.POST.get('firmar_documento')
            verificar_firma = request.POST.get('verificar_firma')

            cambiar_otp = request.POST.get('cambiar_otp')
            firmar_con_otp = request.POST.get('firmar_con_otp')
            invalidar_otp = request.POST.get('invalidar_otp')

            vigencia_1_dia = request.POST.get('vigencia_1_dia')
            vigencia_1_mes = request.POST.get('vigencia_1_mes')
            vigencia_3_meses = request.POST.get('vigencia_3_meses')
            vigencia_6_meses = request.POST.get('vigencia_6_meses')
            vigencia_1_ano = request.POST.get('vigencia_1_ano')
            vigencia_18_meses = request.POST.get('vigencia_18_meses')
            vigencia_2_anos = request.POST.get('vigencia_2_anos')

            token_virtual = request.POST.get('token_virtual')
            token_fisico = request.POST.get('token_fisico')
            pkcs10 = request.POST.get('pkcs10')

            # Crear cadena de certificados y permisos
            certificados_permi = ','.join(filter(None, [
                certificado_Representante_Legal,
                certificado_Funcion_Publica,
                certificado_Facturacion_Electronica_Persona_JurÍdica,
                certificado_Facturacion_Electronica_Persona_Natural,
                certificado_Persona_Natural_Con_RUT,
                certificado_Profesional_Titulado,
                certificado_Función_Publica_SIIF_Nación,
                certificado_Comunidada_Académica,
                certificado_persona_natural,
                certificado_persona_juridica,
                certificado_pertenencia_empresa
            ]))
            o_cert_permi = ','.join(filter(None, [
                consultar_certificado,
                revocar_certificado,
                cambiar_pin,
                reposicion_certificado
            ]))
            o_firmado_permi = ','.join(filter(None, [
                firmar_documento,
                verificar_firma
            ]))
            o_otp_permi = ','.join(filter(None, [
                cambiar_otp,
                firmar_con_otp,
                invalidar_otp
            ]))
            vigencias_permi = ','.join(filter(None, [
                vigencia_1_dia,
                vigencia_1_mes,
                vigencia_3_meses,
                vigencia_6_meses,
                vigencia_1_ano,
                vigencia_18_meses,
                vigencia_2_anos
            ]))
            formatos_entrega_permi = ','.join(filter(None, [
                token_virtual,
                token_fisico,
                pkcs10
            ]))


            # Crear usuario y convenio
            user = User.objects.create_user(username=usuario_convenio, password=contraseña_convenio)
            convenio = CONVENIO.objects.create(
                nombre=nombre,
                logo=logo,
                url=url,
                color_primario=color_primario,
                color_secundario=color_secundario,
                id_vigenica=id_vigenica,
                imagen_banner=imagen_banner,
                contraseña_convenio=contraseña_convenio_encriptada,
                usuario_weservice=usuario_weservice,
                contraseña_webservice=contraseña_webservice,
                certificados_permi=certificados_permi,
                o_cert_permi=o_cert_permi,
                o_firmado_permi=o_firmado_permi,
                o_otp_permi=o_otp_permi,
                vigencias_permi=vigencias_permi,
                formatos_entrega_permi=formatos_entrega_permi,
                id_user=user,
                usuario_convenio=usuario_convenio
            )
            convenio.save()

            # Extraer datos de certificados desde el formulario
            certificados_permi = json.loads(request.POST.get('certificados_permi'))

            # Crear un registro para cada certificado
            for certificado in certificados_permi:
                vigencias_convertidas = [int(vigencia) for vigencia in certificado['vigencias']]

                CONFI_CERTIFICADOS.objects.create(
                    id_convenio=convenio,
                    tipo_certificado=certificado['id'],
                    vigencias=vigencias_convertidas,
                    formatos=certificado['formatos']
                )

            return JsonResponse({"message": "Datos guardados correctamente."}, status=200)

        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return JsonResponse({"error": "Error inesperado al procesar la solicitud"}, status=500)

    return render(request, 'index.html')


def formulario_instancia(request):
    return render(request, 'formulario.html')

def formulario1(request):
    departamentos = obtener_departamentos()  # Llamar a la función para obtener la lista de departamentos
    return render(request, 'formulario1.html', {'departamentos': departamentos})
def procesar_formulario(request):
    if request.method == 'POST':
        # Aquí puedes procesar los datos del formulario enviado
        # Por ejemplo, puedes acceder a los datos del formulario usando request.POST

        # Luego, puedes realizar cualquier lógica de procesamiento necesaria
        # Por ahora, simplemente devolveremos una respuesta de éxito
        return HttpResponse('¡Formulario procesado con éxito!')
    else:
        # Si la solicitud no es POST, puedes manejarlo según sea necesario
        return HttpResponse('¡Solicitud no válida!')
def campos_form(request):
    departamentos = obtener_departamentos()
    print("departamentos:", departamentos)  # Imprimirá los departamentos en la terminal
    return render(request, 'campos-form.html', {'departamentos': departamentos})


def obtener_conexion_db():
    return psycopg2.connect(
        dbname=settings.DATABASES["default"]["NAME"],
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
        host=settings.DATABASES["default"]["HOST"],
        port=settings.DATABASES["default"]["PORT"],
    )





def generar_cabecera_soap(request):
    convenios = request.user.CONVENIO.all()
    if convenios.exists():
        convenio = convenios.first()
        usuario_webservice = convenio.usuario_weservice
        contrasena_webservice = convenio.contraseña_webservice
        print("convenio:", convenio)

        # Generar la cabecera SOAP
        tm_created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        simple_nonce = random.randint(0, 1000000)
        encoded_nonce = base64.b64encode(str(simple_nonce).encode()).decode()
        passdigest = base64.b64encode(
            hashlib.sha1(f"{simple_nonce}{tm_created}{contrasena_webservice}".encode()).digest()
        ).decode()

        cabecera = f"""
        <soapenv:Header>
            <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:UsernameToken wsu:Id="UsernameToken-7967B371AB1C77594517104219622713">
                    <wsse:Username>{usuario_webservice}</wsse:Username>
                    <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{passdigest}</wsse:Password>
                    <wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{encoded_nonce}</wsse:Nonce>
                    <wsu:Created>{tm_created}</wsu:Created>
                </wsse:UsernameToken>
            </wsse:Security>
        </soapenv:Header>
        """

        return {
            'status': 'success',
            'cabecera': cabecera
        }

    return {
        'status': 'error',
        'message': 'No se encontró ningún convenio para este usuario'
    }


def credenciales_webservice(request):
    resultado = generar_cabecera_soap(request)

    if resultado['status'] == 'success':
        request.session['soap_header'] = resultado['cabecera']
        return JsonResponse(resultado)
    else:
        return JsonResponse(resultado)



def obtener_departamentos(request):
    # Obtener datos para la respuesta SOAP
    response = credenciales_webservice(request)

    if isinstance(response, JsonResponse):
        response_content = json.loads(response.content)

        if response_content['status'] == 'success':
            cabecera = response_content['cabecera']

            cuerpo_soap = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    {cabecera}
                </soapenv:Header>
                <soapenv:Body>
                    <and:DepartamentoRequest xmlns:and="http://www.andesscd.com.co/">
                        <and:cadena/>
                    </and:DepartamentoRequest>
                </soapenv:Body>
            </soapenv:Envelope>
            """

            soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
            headers = {
                "Content-Type": "text/xml; charset=utf-8",
            }

            # Hacer la solicitud SOAP para obtener departamentos
            response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

            # Extraer la información de la respuesta SOAP
            root = ET.fromstring(response_soap.text)
            departamento_response = root.find(".//ns1:DepartamentoResponse", namespaces={
                'ns1': 'http://www.andesscd.com.co/'
            })


            departamentos = []

            if departamento_response is not None:
                for item in departamento_response.findall(".//ns1:mensaje", namespaces={
                    'ns1': 'http://www.andesscd.com.co/'
                }):
                    mensajes = json.loads(item.text)
                    print("departamentos:", departamentos)

                    # Agregar tanto ID como nombre a la lista
                    departamentos.extend([{'id_departamento': d['id_departamento'], 'nombre': d['nombre']} for d in mensajes])
                    print("departamentos1:", departamentos)
            return JsonResponse({
                'status': 'success',
                'departamentos': departamentos
            })

    #
    return JsonResponse({
        'status': 'error',
        'message': 'Error al obtener los departamentos'
    })


def obtener_docs(request):
    # Obtener el ID del tipo de certificado del formulario
    id_certificado = request.POST.get('id_certificado')  # Asumiendo que se envía como POST

    # Obtener credenciales del servidor
    response_credenciales = credenciales_webservice(request)  # Función que obtiene las credenciales

    if isinstance(response_credenciales, JsonResponse):
        response_content = json.loads(response_credenciales.content)

        if response_content['status'] == 'success':
            cabecera = response_content['cabecera']

            # Construir la solicitud SOAP para obtener documentos
            cuerpo_soap_documentos = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
                <soapenv:Header>
                    {cabecera}
                </soapenv:Header>
                <soapenv:Body>
                    <and:ListarDocumentosCertificadoRequest>
                        <and:idtipocertificado>{id_certificado}</and:idtipocertificado>
                    </and:ListarDocumentosCertificadoRequest>
                </soapenv:Body>
            </soapenv:Envelope>
            """

            soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
            headers = {
                "Content-Type": "text/xml; charset=utf-8",
            }

            # Realizar la solicitud SOAP para obtener documentos
            response_soap_documentos = requests.post(soap_url, data=cuerpo_soap_documentos, headers=headers)

            # Procesar la respuesta SOAP
            root_documentos = ET.fromstring(response_soap_documentos.text)
            documentos_response = root_documentos.find(".//ns1:ListarDocumentosCertificadoResponse", namespaces={
                'ns1': 'http://www.andesscd.com.co/'
            })

            documentos = []

            if documentos_response is not None:
                for item in documentos_response.findall(".//ns1:mensaje", namespaces={
                    'ns1': 'http://www.andesscd.com.co/'
                }):
                    mensajes = json.loads(item.text)
                    nombres_documentos = [d['nombre'] for d in mensajes]
                    # Crear una lista enumerada con los nombres de los documentos
                    documentos = [nombre for nombre in nombres_documentos]
                    print("documentos enumerados:", documentos)
            else:
                # Registrar un mensaje si no se encuentra la respuesta esperada
                print("No se encontró 'ListarDocumentosCertificadoResponse' en la respuesta SOAP.")

            return JsonResponse({
                'status': 'success',
                'documentos': documentos
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Error al obtener los departamentos o documentos'
    })




def obtener_municipios(request, departamento_id):
    # Obtener credenciales SOAP
    response = credenciales_webservice(request)
    response_content = json.loads(response.content)

    if response_content['status'] == 'success':
        cabecera = response_content['cabecera']
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                {cabecera}
            </soapenv:Header>
            <soapenv:Body>
                <and:MunicipioRequest xmlns:and="http://www.andesscd.com.co/">
                    <and:id_departamento>{departamento_id}</and:id_departamento>
                </and:MunicipioRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        # Hacer la solicitud SOAP para obtener municipios
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        # Extraer municipios de la respuesta SOAP
        root = ET.fromstring(response_soap.text)
        municipio_response = root.find(".//ns1:MunicipioResponse", namespaces={
            'ns1': 'http://www.andesscd.com.co/'
        })

        municipios = []
        if municipio_response is not None:
            for item in municipio_response.findall(".//ns1:mensaje", namespaces={
                'ns1': 'http://www.andesscd.com.co/'
            }):
                mensajes = json.loads(item.text)

                # Asegurarse de usar las claves correctas para ID y nombre
                municipios.extend([{'id': d['id_municipio'], 'nombre': d['nombre']} for d in mensajes])


        return JsonResponse({
            'status': 'success',
            'municipios': municipios  # Ahora la lista tiene ID y nombre
        })

    return JsonResponse({
        'status': 'error',
        'message': 'No se pudo obtener los municipios'
    })

def obtener_universidades(request, municipio_id):
    # Obtener datos para la respuesta SOAP
    response = credenciales_webservice(request)
    response_content = json.loads(response.content)

    if response_content['status'] == 'success':
        cabecera = response_content['cabecera']
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                {cabecera}
            </soapenv:Header>
            <soapenv:Body>
                <and:ListarUniversidadesRequest xmlns:and="http://www.andesscd.com.co/">
                    <and:id_municipio>{municipio_id}</and:id_municipio>
                </and:ListarUniversidadesRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
        }

        # Realizar la solicitud SOAP para obtener universidades
        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        # Extraer datos de la respuesta SOAP
        root = ET.fromstring(response_soap.text)
        mensaje = root.find(".//ns1:mensaje", namespaces={
            'ns1': 'http://www.andesscd.com.co/'
        })

        universidades = []
        if mensaje is not None:
            universidades_data = json.loads(mensaje.text)
            for universidad in universidades_data:
                universidades.append({
                    'id_icfes_u': universidad['id_icfes_u'],
                    'nombre': universidad['nombre']
                })

        return JsonResponse({
            'status': 'success',
            'universidades': universidades
        })

    return JsonResponse({
        'status': 'error',
        'message': 'No se pudo obtener las universidades'
    })


def obtener_titulos(request, universidad_id):
    try:
        # Obtener credenciales para el cuerpo SOAP
        response = credenciales_webservice(request)
        if not isinstance(response, JsonResponse):
            return JsonResponse({'status': 'error', 'message': 'Error al obtener credenciales'})

        response_content = json.loads(response.content)
        if response_content['status'] != 'success':
            return JsonResponse({'status': 'error', 'message': 'Credenciales no válidas'})

        cabecera = response_content['cabecera']

        # Construir el cuerpo SOAP para obtener títulos profesionales
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                {cabecera}
            </soapenv:Header>
            <soapenv:Body>
                <and:ListarTitulosProfesionalesRequest xmlns:and="http://www.andesscd.com.co/">
                    <and:id_universidad>{universidad_id}</and:id_universidad>
                </and:ListarTitulosProfesionalesRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        # Hacer la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            # Analizar la respuesta SOAP
            root = ET.fromstring(response_soap.text)
            mensaje = root.find(".//ns1:mensaje", namespaces={'ns1': 'http://www.andesscd.com.co/'})
            titulos_profesionales = []
            if mensaje is not None:
                titulos_data = json.loads(mensaje.text)
                for titulo in titulos_data:
                    titulos_profesionales.append({
                        'id_icfes_tp': titulo['id_icfes_tp'],
                        'nombre': titulo['nombre']
                    })
            print("titulos-profesinales:", titulos_profesionales)

            return JsonResponse({
                'status': 'success',
                'titulos_profesionales': titulos_profesionales
            })

        return JsonResponse({
            'status': 'error',
            'message': 'Error al obtener títulos profesionales'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def radicado_pers_nat(request):
    # Comprobar si se obtuvo la cabecera SOAP correctamente
    response = credenciales_webservice(request)

    if isinstance(response, JsonResponse):
        response_content = json.loads(response.content)

        if response_content['status'] == 'success':
            cabecera = response_content['cabecera']
            print("Cabecera SOAP obtenida:", cabecera)  # Imprimir la cabecera para verificar

    # Obtener el id del convenio desde la sesión
    convenios = request.user.CONVENIO.all()
    if convenios.exists():
        convenio = convenios.first()
        id = convenio.id

    # Validar que el convenio_id está presente
    if not id:
        print("Error: No se encontró el ID del convenio.")
        return JsonResponse({
            'status': 'error',
            'message': 'No se encontró el ID del convenio en la sesión'
        }, status=400)

    # Validar datos del formulario
    tipo_doc = request.POST.get('tipo-documento', '')
    documento = request.POST.get('numero-documento', '')
    nombres = request.POST.get('nombres', '')
    apellidos = request.POST.get('apellidos', '')
    municipio = request.POST.get('municipio', '')
    direccion = request.POST.get('direccion', '')
    email = request.POST.get('correo', '')
    telefono = request.POST.get('numero-celular', '')
    fecha_cert = request.POST.get('fecha-certificado', '')
    vigencia = request.POST.get('vigencia', '')
    formato = request.POST.get('formato-entrega', '')

    # Verificar campos obligatorios
    if not (tipo_doc and documento and nombres and apellidos and municipio and direccion and email):
        return JsonResponse({
            'status': 'error',
            'message': 'Faltan datos obligatorios'
        })

    # Leer el archivo .zip y convertir a base64
    soporte = request.FILES.get('documentos', None)

    if not soporte:
        return JsonResponse({
            'status': 'error',
            'message': 'El archivo .zip no se encontró'
        })
    contenido_zip = soporte.read()



    soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')

    # Construir el cuerpo SOAP
    cuerpo_soap = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
        <soapenv:Header>
            {cabecera}
        </soapenv:Header>
            <soapenv:Body>
              <and:CertificadosRequest>
                 <and:tipoCert>16</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio}</and:municipio>
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:telefono>{telefono}</and:telefono>
                 <and:celular>{telefono}</and:celular>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:formato>{formato}</and:formato>
                 <and:soporte>{soporte_base64}</and:soporte>


              </and:CertificadosRequest>
           </soapenv:Body>

    </soapenv:Envelope>
    """

    # Enviar la solicitud SOAP
    soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Accept-Encoding": "identity"
    }

    # Realizar la solicitud POST
    response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

    print("respuesta soap", response_soap.status_code)
    if response_soap.status_code == 200:
        try:
            root = ET.fromstring(response_soap.text)  # Analizar la respuesta SOAP
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text
            print("estado:", estado)
            print("mensaje:", mensaje)

            if int(estado) == 0:
                # Guardar datos en la tabla DATOS
                print(f"id{id} mensaje{mensaje}")
                datos = DATOS(
                    id_conv=id,  # Relacionar con el convenio
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,
                       # Guardar el número de radicado
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        except ET.ParseError:
            return JsonResponse({
                'status': 'error',
                'message': 'Error al analizar el XML de respuesta SOAP'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Error desconocido: {str(e)}"
            })

    else:
        return JsonResponse({
            'status': 'error',
            'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
        })

def radicado_pers_nat_rut(request):
    # Obtener las credenciales del Web Service
    response = credenciales_webservice(request)

    if isinstance(response, JsonResponse):
        response_content = json.loads(response.content)
        if response_content['status'] == 'success':
            cabecera = response_content['cabecera']
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Error obteniendo las credenciales'
            })

    convenios = request.user.CONVENIO.all()
    if convenios.exists():
        convenio = convenios.first()
        id = convenio.id

    # Validar datos del formulario
    tipo_doc = request.POST.get('tipo-documento', '')
    documento = request.POST.get('numero-documento', '')
    nombres = request.POST.get('nombres', '')
    apellidos = request.POST.get('apellidos', '')
    municipio = request.POST.get('municipio', '')
    direccion = request.POST.get('direccion', '')
    email = request.POST.get('correo', '')
    telefono = request.POST.get('numero-celular', '')
    fecha_cert = request.POST.get('fecha-certificado', '')
    vigencia = request.POST.get('vigencia', '')
    formato = request.POST.get('formato-entrega', '')

    # Verificar campos obligatorios
    if not (tipo_doc, documento, nombres, apellidos, municipio, direccion, email):
        return JsonResponse({
            'status': 'error',
            'message': 'Faltan datos obligatorios'
        })

    # Codificar el soporte en base64 si corresponde
    soporte = request.FILES.get('documentos', None)

    if not soporte:
        return JsonResponse({
            'status': 'error',
            'message': 'El archivo .zip no se encontró'
        })
    contenido_zip = soporte.read()





    soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')

    # Construir el cuerpo SOAP
    cuerpo_soap = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
        <soapenv:Header>
            {cabecera}
        </soapenv:Header>
        <soapenv:Body>
            <and:CertificadosPersonaNaturalRUTRequest>
                <and:tipoCert>15</and:tipoCert>
                <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                <and:documento>{documento}</and:documento>
                <and:nombres>{nombres}</and:nombres>
                <and:apellidos>{apellidos}</and:apellidos>
                <and:municipio>{municipio}</and:municipio>
                <and:direccion>{direccion}</and:direccion>
                <and:email>{email}</and:email>
                <and:telefono>{telefono}</and:telefono>
                <and:celular>{telefono}</and:celular>
                <and:fechaCert>{fecha_cert}</and:fechaCert>
                <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                <and:formato>{formato}</and:formato>
                <and:soporte>{soporte_base64}</and:soporte>
            </and:CertificadosPersonaNaturalRUTRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    #print(cuerpo_soap)
    # Enviar la solicitud SOAP
    soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Accept-Encoding": "identity"
    }

    # Realizar la solicitud POST
    response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

    if response_soap.status_code == 200:
        try:
            # Analizar la respuesta SOAP
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text
            print(mensaje)
            if int(estado) == 0:
                # Guardar datos en la base de datos usando el modelo DATOS
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    tipo_certificado=15,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        except ET.ParseError:
            return JsonResponse({
                'status': 'error',
                'message': 'Error al analizar el XML de respuesta SOAP'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Error desconocido: {str(e)}"
            })

    else:
        return JsonResponse({
            'status': 'error',
            'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
        })

def radicado_prof_titulado(request):
    try:
        # Obtener cabecera de credenciales
        response = credenciales_webservice(request)
        if not isinstance(response, JsonResponse):
            return JsonResponse({'status': 'error', 'message': 'Error al obtener credenciales'})

        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        response_content = json.loads(response.content)
        if response_content['status'] != 'success':
            return JsonResponse({'status': 'error', 'message': 'Credenciales no válidas'})

        cabecera = response_content['cabecera']

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio = request.POST.get('municipio', '')
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        telefono = request.POST.get('numero-celular', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        vigencia = request.POST.get('vigencia', '')
        formato = request.POST.get('formato-entrega', '')


        ocupacion = request.POST.get('ocupacion', '')
        universidad = request.POST.get('universidad', '')
        tituloprofesional = request.POST.get('titulos_profesionales', '')
        matriculaprofesional = request.POST.get('matricula_profesional', '')
        emisortarjetaprofesional = request.POST.get('emisortarjetaprofesional', '')
        facultad = request.POST.get('facultad', '')
        print("titulo-profe:", tituloprofesional)
        # Verificar campos obligatorios
        if not (tipo_doc and documento and nombres and apellidos and municipio and direccion and email):
            return JsonResponse({'status': 'error', 'message': 'Faltan datos obligatorios'})

        # Codificar soporte en base64 si corresponde
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()



        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
            <soapenv:Header>
                {cabecera}
            </soapenv:Header>
           <soapenv:Body>
              <and:CertificadoProfesionalTituladoRequest>
                 <and:tipoCert>7</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio}</and:municipio>
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:celular>{telefono}</and:celular>
                 <and:universidad>{universidad}</and:universidad>
                 <and:tituloprofesional>{tituloprofesional}</and:tituloprofesional>
                 <and:matriculaprofesional>{matriculaprofesional}</and:matriculaprofesional>
                 <and:emisortarjetaprofesional>{emisortarjetaprofesional}</and:emisortarjetaprofesional>
                 <and:facultad>{facultad}</and:facultad>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:formato>{formato}</and:formato>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificadoProfesionalTituladoRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        #print("cuerpo-soap:", cuerpo_soap)

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        # Realizar la solicitud POST
        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)
        print("soap:",response_soap)
        if response_soap.status_code == 200:
            # Analizar el XML para obtener el estado y el mensaje
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text
            print("mensaje:", mensaje)
            if int(estado) == 0:
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    tipo_certificado=15,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio,
                    universidad=universidad,
                    facultad=facultad,
                    matricula_profesional=matriculaprofesional,
                    titulo_profesional=tituloprofesional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                )

                datos.save()





                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def radicado_pert_empresa(request):
    try:
        # Obtener cabecera de credenciales
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio_persona = request.POST.get('municipio-persona', '')
        municipio_empresa = request.POST.get('municipio-empresa', '')
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        emailEnt = request.POST.get('correo-entidad', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        if not (tipo_doc and documento and nombres and apellidos and direccion and email):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si es necesario
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()



        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
           <soapenv:Header>
              {cabecera}
           </soapenv:Header>
           <soapenv:Body>
              <and:CertificateVinculacionEmpresaRequest>
                 <and:tipoCert>9</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio_persona}</and:municipio>  # Primera selección
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_empresa}</and:municipioEnt>  # Segunda selección
                 <and:direccionEnt>{direccion}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificateVinculacionEmpresaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }
        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            # Analizar el XML para obtener estado y mensaje
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text
            print(mensaje)
            if int(estado) == 0:
                # Guardar en la base de datos
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio_persona,
                    ocupacion=ocupacion,
                    cargo=cargo,
                    unidad_organizacional=unidad_organizacional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,
                    tipo_certificado=9,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
                'status': 'error',
                'message': f"Error desconocido: {str(e)}"
            })


def radicado_fun_publica(request):
    try:
        # Obtener credenciales para el Web Service
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })

        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio_persona = request.POST.get('municipio-persona', None)
        municipio_empresa = request.POST.get('municipio-empresa', None)
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        emailEnt = request.POST.get('correo-entidad', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        if not (tipo_doc and documento and nombres and apellidos and direccion and email):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si es necesario
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()



        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
           <soapenv:Header>
              {cabecera}
           </soapenv:Header>
           <soapenv:Body>
              <and:CertificateVinculacionEmpresaRequest>
                 <and:tipoCert>12</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio_persona}</and:municipio>  # Primera selección
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_empresa}</and:municipioEnt>  # Segunda selección
                 <and:direccionEnt>{direccion}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificateVinculacionEmpresaRequest>
           </soapenv:Body>

        </soapenv:Envelope>
        """

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            # Analizar el XML para obtener estado y mensaje
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text
            print("mensaje:", mensaje)
            if int(estado) == 0:
                # Guardar en la base de datos solo con campos permitidos
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio_persona,
                    ocupacion=ocupacion,
                    cargo=cargo,
                    unidad_organizacional=unidad_organizacional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,
                    tipo_certificado=12,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })

def radicado_perso_juridica(request):
    try:
        # Obtener credenciales para el Web Service
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio_persona = request.POST.get('municipio-persona', None)
        municipio_empresa = request.POST.get('municipio-empresa', None)
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        emailEnt = request.POST.get('correo-entidad', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        if not (tipo_doc, documento, nombres, apellidos, direccion, email):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si es necesario
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()




        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
           <soapenv:Header>
              {cabecera}
           </soapenv:Header>
           <soapenv:Body>
              <and:CertificateVinculacionEmpresaRequest>
                 <and:tipoCert>13</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio_persona}</and:municipio>  # Primera selección
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_empresa}</and:municipioEnt>  # Segunda selección
                 <and:direccionEnt>{direccion}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificateVinculacionEmpresaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            # Analizar el XML para obtener estado y mensaje
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text
            print("mensaje:", mensaje)
            if int(estado) == 0:
                # Guardar datos en la base de datos solo con campos esperados
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio_persona,
                    ocupacion=ocupacion,
                    cargo=cargo,
                    unidad_organizacional=unidad_organizacional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                    tipo_certificado=13,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })

def radicado_fe_natural(request):
    try:
        # Obtener cabecera de autenticación
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio = request.POST.get('municipio-persona', '')
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        telefono = request.POST.get('telefono', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        municipio_ent = request.POST.get('municipio-empresa', '')
        direccion_ent = request.POST.get('direccion-entidad', '')
        emailEnt = request.POST.get('correo-entidad', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        organizacion_factel = request.POST.get('organizacion-factel', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        campos_obligatorios = [tipo_doc, documento, nombres, apellidos, municipio, direccion, email]
        if not all(campos_obligatorios):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si corresponde
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()



        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')  # Convertir a base64

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
            <soapenv:Header>
                {cabecera}
            </soapenv:Header>
           <soapenv:Body>
              <and:CertificadoFacturacionElectronicaRequest>
                 <and:tipoCert>10</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio}</and:municipio>
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:telefono>{telefono}</and:telefono>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_ent}</and:municipioEnt>
                 <and:direccionEnt>{direccion_ent}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:organizacionFactel>{organizacion_factel}</and:organizacionFactel>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificadoFacturacionElectronicaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Realizar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text

            if int(estado) == 0:
                # Guardar datos en la base de datos solo con campos esperados
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio,
                    ocupacion=ocupacion,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                    tipo_certificado=10,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })

def radicado_fe_juridica(request):
    try:
        # Obtener cabecera de autenticación
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio = request.POST.get('municipio-persona', '')
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        telefono = request.POST.get('telefono', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        municipio_ent = request.POST.get('municipio-empresa', '')
        direccion_ent = request.POST.get('direccion-entidad', '')
        emailEnt = request.POST.get('correo-entidad', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        organizacion_factel = request.POST.get('organizacion-factel', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        campos_obligatorios = [tipo_doc, documento, nombres, apellidos, municipio, direccion, email]
        if not all(campos_obligatorios):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si corresponde
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()




        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')  # Convertir a base64

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
            <soapenv:Header>
                {cabecera}
            </soapenv:Header>
           <soapenv:Body>
              <and:CertificadoFacturacionElectronicaRequest>
                 <and:tipoCert>11</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio}</and:municipio>
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:telefono>{telefono}</and:telefono>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_ent}</and:municipioEnt>
                 <and:direccionEnt>{direccion_ent}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:organizacionFactel>{organizacion_factel}</and:organizacionFactel>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificadoFacturacionElectronicaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Realizar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text

            if int(estado) == 0:
                # Guardar datos en la base de datos solo con campos esperados
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio,
                    ocupacion=ocupacion,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                    tipo_certificado=11,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })

def radicado_com_academica(request):
    try:
        # Obtener cabecera de autenticación
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio_persona = request.POST.get('municipio-persona', None)
        municipio_empresa = request.POST.get('municipio-empresa', None)
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        emailEnt = request.POST.get('correo-entidad', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        campos_obligatorios = [tipo_doc, documento, nombres, apellidos, municipio_persona, direccion, email]
        if not all(campos_obligatorios):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si es necesario
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()



        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')  # Convertir a base64

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
           <soapenv:Header>
              {cabecera}
           </soapenv:Header>
           <soapenv:Body>
              <and:CertificateVinculacionEmpresaRequest>
                 <and:tipoCert>6</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio_persona}</and:municipio>  # Primera selección
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_empresa}</and:municipioEnt>  # Segunda selección
                 <and:direccionEnt>{direccion}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificateVinculacionEmpresaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text

            if int(estado) == 0:
                # Guardar datos en la base de datos solo con campos esperados
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio_persona,
                    ocupacion=ocupacion,
                    cargo=cargo,
                    unidad_organizacional=unidad_organizacional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                    tipo_certificado=6,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })

def radicado_com_siif(request):
    try:
        # Obtener cabecera de autenticación
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio_persona = request.POST.get('municipio-persona', None)
        municipio_empresa = request.POST.get('municipio-empresa', None)
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        emailEnt = request.POST.get('correo-entidad', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        campos_obligatorios = [tipo_doc, documento, nombres, apellidos, municipio_persona, direccion, email]
        if not all(campos_obligatorios):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si es necesario
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()




        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')  # Convertir a base64

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
           <soapenv:Header>
              {cabecera}
           </soapenv:Header>
           <soapenv:Body>
              <and:CertificateVinculacionEmpresaRequest>
                 <and:tipoCert>14</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio_persona}</and:municipio>  # Primera selección
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_empresa}</and:municipioEnt>  # Segunda selección
                 <and:direccionEnt>{direccion}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificateVinculacionEmpresaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text

            if int(estado) == 0:
                # Guardar datos en la base de datos solo con campos esperados
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio_persona,
                    ocupacion=ocupacion,
                    cargo=cargo,
                    unidad_organizacional=unidad_organizacional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                    tipo_certificado=14,
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })

def radicado_repre_legal(request):
    try:
        # Obtener cabecera de autenticación
        response = credenciales_webservice(request)
        if isinstance(response, JsonResponse):
            response_content = json.loads(response.content)
            if response_content['status'] == 'success':
                cabecera = response_content['cabecera']
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciales no válidas'
                })
        convenios = request.user.CONVENIO.all()
        if convenios.exists():
            convenio = convenios.first()
            id = convenio.id

        # Validar datos del formulario
        tipo_doc = request.POST.get('tipo-documento', '')
        documento = request.POST.get('numero-documento', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        municipio_persona = request.POST.get('municipio-persona', None)
        municipio_empresa = request.POST.get('municipio-empresa', None)
        direccion = request.POST.get('direccion', '')
        email = request.POST.get('correo', '')
        emailEnt = request.POST.get('correo-entidad', '')
        celular = request.POST.get('celular', '')
        ocupacion = request.POST.get('ocupacion', '')
        tipo_doc_ent = request.POST.get('tipo-documento-entidad', '')
        documento_ent = request.POST.get('numero-documento-entidad', '')
        razon_social = request.POST.get('razon-social', '')
        cargo = request.POST.get('cargo', '')
        unidad_organizacional = request.POST.get('unidad-organizacional', '')
        fecha_cert = request.POST.get('fecha-certificado', '')
        formato = request.POST.get('formato-entrega', '')
        vigencia = request.POST.get('vigencia', '')

        # Verificar campos obligatorios
        if not (tipo_doc and documento and nombres and apellidos and direccion and email):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan datos obligatorios'
            })

        # Codificar soporte en base64 si es necesario
        soporte = request.FILES.get('documentos', None)

        if not soporte:
            return JsonResponse({
                'status': 'error',
                'message': 'El archivo .zip no se encontró'
            })
        contenido_zip = soporte.read()



        soporte_base64 = base64.b64encode(contenido_zip).decode('utf-8')  # Convertir a base64

        # Construir el cuerpo SOAP
        cuerpo_soap = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
           <soapenv:Header>
              {cabecera}
           </soapenv:Header>
           <soapenv:Body>
              <and:CertificateVinculacionEmpresaRequest>
                 <and:tipoCert>8</and:tipoCert>
                 <and:tipoDoc>{tipo_doc}</and:tipoDoc>
                 <and:documento>{documento}</and:documento>
                 <and:nombres>{nombres}</and:nombres>
                 <and:apellidos>{apellidos}</and:apellidos>
                 <and:municipio>{municipio_persona}</and:municipio>  # Primera selección
                 <and:direccion>{direccion}</and:direccion>
                 <and:email>{email}</and:email>
                 <and:emailEnt>{emailEnt}</and:emailEnt>
                 <and:celular>{celular}</and:celular>
                 <and:ocupacion>{ocupacion}</and:ocupacion>
                 <and:tipoDocEnt>{tipo_doc_ent}</and:tipoDocEnt>
                 <and:documentoEnt>{documento_ent}</and:documentoEnt>
                 <and:razonsocial>{razon_social}</and:razonsocial>
                 <and:municipioEnt>{municipio_empresa}</and:municipioEnt>  # Segunda selección
                 <and:direccionEnt>{direccion}</and:direccionEnt>
                 <and:cargo>{cargo}</and:cargo>
                 <and:unidadOrganizacional>{unidad_organizacional}</and:unidadOrganizacional>
                 <and:fechaCert>{fecha_cert}</and:fechaCert>
                 <and:formato>{formato}</and:formato>
                 <and:vigenciaCert>{vigencia}</and:vigenciaCert>
                 <and:soporte>{soporte_base64}</and:soporte>
              </and:CertificateVinculacionEmpresaRequest>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        # Enviar la solicitud SOAP
        soap_url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "Accept-Encoding": "identity"
        }

        response_soap = requests.post(soap_url, data=cuerpo_soap, headers=headers)

        if response_soap.status_code == 200:
            root = ET.fromstring(response_soap.text)
            estado = root.find('.//ns1:estado', {'ns1': 'http://www.andesscd.com.co/'}).text
            mensaje = root.find('.//ns1:mensaje', {'ns1': 'http://www.andesscd.com.co/'}).text

            if int(estado) == 0:
                # Guardar datos en la base de datos solo con campos esperados
                datos = DATOS(
                    id_conv=id,
                    tipo_doc=tipo_doc,
                    nombre=nombres,
                    apellido=apellidos,
                    numero_doc=documento,
                    correo=email,
                    direccion=direccion,
                    municipio=municipio_persona,
                    ocupacion=ocupacion,
                    cargo=cargo,
                    unidad_organizacional=unidad_organizacional,
                    formato_entrega=formato,
                    vigencia=vigencia,
                    radicado=mensaje,  # Guardar el número de radicado
                    tipo_certificado=8
                )

                datos.save()  # Guardar en la base de datos

                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada correctamente',
                    'radicado': mensaje
                })

            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en la solicitud SOAP',
                    'message': mensaje
                })

        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Error en la solicitud SOAP: {response_soap.status_code}"
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f"Error desconocido: {str(e)}"
        })



