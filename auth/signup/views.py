from django.views.generic import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme

@method_decorator(never_cache, name='dispatch')
class AuthLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Lógica para cerrar sesión
        request.session.flush()

        # Redirigir a la página de inicio de sesión después de cerrar sesión
        response = redirect('auth:signin')
        
        # Establecer encabezados para evitar almacenamiento en caché
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class AuthSignupView(TemplateView):
    template_name = 'pages/auth/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context