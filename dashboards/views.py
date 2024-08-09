import requests
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from dashboards.models import CONFI_CERTIFICADOS, CONVENIO, DATOS
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.exceptions import TemplateDoesNotExist
from django.http import JsonResponse, HttpResponse
import traceback

class DashboardsView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/dashboards/index.html'
    
    def get_context_data(self, **kwargs):
        # Inicializar el contexto base
        context = super().get_context_data(**kwargs)
        
        # Obtener el usuario logueado
        usuario_logueado = self.request.user
        
        # Ordenar convenios y aplicar paginación
        convenios_ordenados = CONVENIO.objects.order_by('-id')
        paginator = Paginator(convenios_ordenados, 10)
        page_number = self.request.GET.get('page')
        
        try:
            convenios_paginados = paginator.page(page_number)
        except PageNotAnInteger:
            convenios_paginados = paginator.page(1)
        except EmptyPage:
            convenios_paginados = paginator.page(paginator.num_pages)
        
        # Añadir convenios paginados al contexto
        context['convenios'] = convenios_paginados
        
        # Inicializar el layout global
        context = KTLayout.init(context)
        
        # Incluir vendors y archivos JavaScript para los widgets del dashboard
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        
        return context

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
        "1": 'consultar',
        "2": 'revocar',
        "3": 'cambiar_pin',
        "4": 'reposicion'
    }

    mapeo_operaciones_firmado = {
        "1": 'firmar_doc',
        "2": 'verificar_firma'
    }

    mapeo_operaciones_otp = {
        "1": 'cambiar_tiempo',
        "2": 'firmar_otp',
        "3": 'invalidar'
    }

    convenio = get_object_or_404(CONVENIO, nombre=nombre)
    confi_certificados = CONFI_CERTIFICADOS.objects.filter(id_convenio=convenio.id)

    # Imprimir los valores de tipo_certificado para depuración
    for cert in confi_certificados:
        print("Tipo de Certificado:", cert.tipo_certificado)

    certificados_con_nombre_y_formulario = [
        {
            'tipo_certificado': mapeo_tipos_certificado.get(str(cert.tipo_certificado), 'Tipo desconocido'),
            'formulario': mapeo_certificados_formularios.get(str(cert.tipo_certificado), '#'),  # Default to '#'
            'detalles_certificado': cert,
        }
        for cert in confi_certificados
    ]

    for cert in certificados_con_nombre_y_formulario:
        print(cert)

    print("color: ", convenio.color_primario)
    print("Nombre del convenio:", convenio.nombre)
    print("Color primario del convenio:", convenio.color_primario)

    numeros_operacion_cert = convenio.o_cert_permi.split(',') if convenio.o_cert_permi else []
    operaciones_certificado = [mapeo_operacion_cert.get(numero) for numero in numeros_operacion_cert]

    numeros_operaciones_firmado = convenio.o_firmado_permi.split(',') if convenio.o_firmado_permi else []
    operaciones_firmado = [mapeo_operaciones_firmado.get(numero) for numero in numeros_operaciones_firmado]

    numeros_operaciones_otp = convenio.o_otp_permi.split(',') if convenio.o_otp_permi else []
    operaciones_otp = [mapeo_operaciones_otp.get(numero) for numero in numeros_operaciones_otp]

    return render(request, 'pages/dashboards/plantilla_dinamica.html', {
        'convenio': convenio,
        'certificados_con_nombre_y_formulario': certificados_con_nombre_y_formulario,
        'operaciones_certificado': operaciones_certificado,
        'operaciones_firmado': operaciones_firmado,
        'operaciones_otp': operaciones_otp
    })

def plantilla_convenio(request, id):
    convenio = get_object_or_404(CONVENIO, id=id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})


def formulario_view(request, formulario):
    print("Entrando a la función")
    templates = {
        'form_fe_pj': 'formularios/form_fe_pj.html',
        'form_fe_pn': 'formularios/form_fe_pn.html',
        'form_com_acad': 'formularios/form_com_acad.html',
        'form_pert_emp': 'formularios/form_pert_emp.html',
        'form_prof_titu': 'formularios/form_prof_titu.html',
        'form_rep_leg': 'formularios/form_rep_leg.html',
        'form_func_pub': 'formularios/form_func_pub.html',
        'form_pers_jur': 'formularios/form_pers_jur.html',
        'form_siif_nac': 'formularios/form_siif_nac.html',
        'form_pers_nat': 'formularios/form_pers_nat.html',
        'form_pers_nat_rut': 'formularios/form_pers_nat_rut.html'
    }

    template_name = templates.get(formulario)
    print("template:", template_name)
    if template_name:
        try:
            html = render_to_string(template_name, {})
            print("html:", html)
            print("HTML generado correctamente")
            return JsonResponse({'html': html})
        except TemplateDoesNotExist:
            print(f"Error: la plantilla {template_name} no existe.")
            return JsonResponse({'error': f"La plantilla {template_name} no existe."}, status=404)
        except Exception as e:
            print("Error al renderizar la plantilla:", e)
            print(traceback.format_exc())
            return JsonResponse({'error': 'Error al renderizar la plantilla.'}, status=500)
    else:
        return JsonResponse({'error': 'Formulario no encontrado.'}, status=404)