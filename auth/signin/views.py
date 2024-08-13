from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get('usuario')
        password = request.POST.get('contraseña')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirectUrl': '/index'})
        else:
            context = self.get_context_data()
            context['error'] = 'Usuario o contraseña incorrectos, Verificalos y vuelve a intentar'
            return JsonResponse({'message': context['error']})

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)
