from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView
from dashboards.views import DashboardsView, plantilla_dinamica
from django.conf.urls.static import static
from .views import formulario_view 
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('index', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('convenio/<str:nombre>/',plantilla_dinamica, name='detalle_convenio'),
    #path('formulario/<str:formulario>/', formulario_view, name='formulario_view'),
    path('formulario/<str:certificado_id>/', formulario_view, name='formulario_view'),
    #path('plantilla_dinamica/<str:nombre>/', plantilla_dinamica, name='detalle_convenio'),
    path('plantilla_dinamica/<str:nombre>/<str:certificado_id>/', formulario_view, name='formulario_view'),
    path('plantilla_dinamica/<str:nombre>/', plantilla_dinamica, name='plantilla_dinamica'),
    path('plantilla_dinamica/<str:nombre>/', views.plantilla_dinamica, name='detalle_convenio'),
    path('dinamica', DashboardsView.as_view(template_name = 'pages/dashboards/dinamica.html'), name='dinamica'),
    path('plantilla_convenio/<str:nombre>/', views.plantilla_convenio, name='plantilla_convenio'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
    path('form_pers_nat/', views.form_pers_nat, name='form_pers_nat'),
    path('form_rep_leg/', views.form_rep_leg, name='form_rep_leg'),
    path('form_func_pub/', views.form_func_pub, name='form_func_pub'),
    path('form_siif_nac/', views.form_siif_nac, name='form_siif_nac'),
    path('form_com_acad/', views.form_com_acad, name='form_com_acad'),
    path('form_pers_jur/', views.form_pers_jur, name='form_pers_jur'),
    path('form_pers_nat_rut/', views.form_pers_nat_rut, name='form_pers_nat_rut'),
    path('form_pert_emp/', views.form_pert_emp, name='form_pert_emp'), 
    path('form_prof_titu/', views.form_prof_titu, name='form_prof_titu'),
    path('form_fe_pj/', views.form_fe_pj, name='form_fe_pj'),
    path('form_fe_pn/', views.form_fe_pn, name='form_fe_pn'),
    #path('procesar-formulario/', views.procesar_formulario, name='procesar_formulario'),
    path('crear_instancia/', views.crear_instancia, name='crear_instancia'),
    path('credenciales_webservice/', views.credenciales_webservice, name='credenciales_webservice'),
    path('generar_cabecera_soap/', views.generar_cabecera_soap, name='generar_cabecera_soap'),
    path('radicado_pers_nat/', views.radicado_pers_nat, name='radicado_pers_nat'),
    path('radicado_pers_nat_rut/', views.radicado_pers_nat_rut, name='radicado_pers_nat_rut'),
    path('obtener_universidades/<int:municipio_id>/', views.obtener_universidades, name='obtener_universidades'),
    path('radicado_prof_titulado/', views.radicado_prof_titulado, name='radicado_prof_titulado'),
    path('obtener_titulos/<int:universidad_id>/', views.obtener_titulos, name='obtener_titulos'),
    path('radicado_pert_empresa/', views.radicado_pert_empresa, name='radicado_pert_empresa'),
    path('radicado_fe_juridica/', views.radicado_fe_juridica, name='radicado_fe_juridica'),
    path('radicado_fe_natural/', views.radicado_fe_natural, name='radicado_fe_natural'),
    path('radicado_fun_publica/', views.radicado_fun_publica, name='radicado_fun_publica'),
    path('radicado_perso_juridica/', views.radicado_perso_juridica, name='radicado_perso_juridica'),
    path('radicado_com_academica/', views.radicado_com_academica, name='radicado_com_academica'),
    path('radicado_com_siif/', views.radicado_com_siif, name='radicado_com_siif'),
    path('radicado_repre_legal/', views.radicado_repre_legal, name='radicado_repre_legal'),
    path('imagen_banner/', views.imagen_banner, name='imagen_banner'),
    path('obtener_docs/', views.obtener_docs, name='obtener_docs'),
    path('obtener_departamentos/', views.obtener_departamentos, name='obtener_departamentos'),
    path('obtener_municipios/<int:departamento_id>/', views.obtener_municipios, name='obtener_municipios'),
]

