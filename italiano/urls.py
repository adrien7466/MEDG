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

from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView, ListView # vues génériques
from italiano.models import Mot, Expression
from italiano.views import Liste_Mots, Detail_Mots

urlpatterns = [
    # path("home", views.accueil_it,name="accueil_it"),     # définition d'une fonction dans vue.py
    path("home",Liste_Mots.as_view(),name="accueil_it"),   # vue générique, définition d'une classe dans vue.py
    # path("home2/(?P<pk>\d+)$",Detail_Mots.as_view(),name="accueil_it3"),
    path("interrogation_mots", views.testMot,name="interro_mots"),

]
