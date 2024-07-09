from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('vista', DashboardsView.as_view(template_name = 'pages/dashboards/vista.html'), name='vista'),
    path('dinamica', DashboardsView.as_view(template_name = 'pages/dashboards/dinamica.html'), name='dinamica'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]