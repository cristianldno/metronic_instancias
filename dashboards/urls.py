from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView
from dashboards.views import DashboardsView, plantilla_dinamica
from .views import formulario_view


app_name = 'dashboards'

urlpatterns = [
    path('index', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('convenio/<str:nombre>/',plantilla_dinamica, name='detalle_convenio'),
    path('formulario/<str:formulario>/', formulario_view, name='formulario_view'),
    #path('plantilla_dinamica/<str:nombre>/', plantilla_dinamica, name='detalle_convenio'),
    path('plantilla_dinamica/<str:nombre>/', plantilla_dinamica, name='plantilla_dinamica'),
    path('dinamica', DashboardsView.as_view(template_name = 'pages/dashboards/dinamica.html'), name='dinamica'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]