"""Site_Adrien URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# Administration
from django.contrib import admin
admin.autodiscover()


from django.urls import path, include
from django.views.generic import TemplateView
from appli_medG import views as med_views
from italiano import views as ital_views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', TemplateView.as_view(template_name='homepage.html'), name="homepage"), # création d'une vue générique
	path('appli_medG/', include('appli_medG.urls')),
	path('it/', include('italiano.urls')),
]

# pour aller chercher les fichiers dans static
#attention !!!!!!!!!!!doit etre enlevé lorsque l'on est en DEBUG=False
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

