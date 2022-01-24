"""myclub_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import contact
# from events.admin import admin_site
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView
from events.views import TemplateViewDemo, Register


admin.site.site_header = 'MyClub Administration'
admin.site.site_title = 'MyClub Site Admin'
admin.site.index_title = 'MyClub Site Admin Home'


urlpatterns = [
    # path('cbvdemo/', TemplateView.as_view(template_name='events/cbv_demo.html')),
    path('cbvdemo/', TemplateViewDemo.as_view()),
    path('home/', RedirectView.as_view(url='/', permanent=True)),
    path('admin/', admin.site.urls),
    # path('eventsadmin/', admin_site.urls),
    # path('contact/', contact.contact, name='contact'),
    path('contact/', contact.ContactUs.as_view(), name='contact'),
    path(
    'admin/password_reset/',
    auth_views.PasswordResetView.as_view(),
    name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('', include('events.urls')),
    path(
        'register/success/',
        TemplateView.as_view(template_name="registration/success.html"),
        name ='register-success',
    ),
    path('register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]
