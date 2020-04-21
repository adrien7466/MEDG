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
from appli_medG.views import ProfileSearchView
from appli_medG.views import PatientDetailView, PatientListView, TraitementListView, PatientCreateView, PatientCreateView2, PatientUpdateView, PatientDeleteView, CarnetUpdateView
from appli_medG.views import MaladieCreateView, AddictionCreateView
from appli_medG.views import MaladieDeleteView
from appli_medG.views import TraitementSearchView


urlpatterns = [

	# I. Exemple d'une URL liée à vue avec une liste d'instance d'un modèle
    # path("", views.accueil,name="accueil"),
    path("", PatientListView.as_view(),name="accueil"),
    path("liste_medicament", TraitementListView.as_view(),name="list_traitement"),

	# II. Exemple d'une URL liée à une vue qui affiche un objet précis d'un modèle
	# path("patient/<id>", views.description,name='desciption_patient'), 			# Vue de l'espace perso
	path("patient_detail/<pk>", PatientDetailView.as_view( ), name='desciption_patient'),  # Vue de l'espace perso

	# III. Exemple d'une URL liée à une vue qui crée un objet (formulaire)
	# path("add_patient/", views.createPatient,name='create_new_patient'), # Formulaire pour création d'unnouveau patient
	# path("add_patient/", PatientCreateView.as_view(),name='create_new_patient'), # Formulaire pour création d'unnouveau patient
	path("add_patient/", PatientCreateView2.as_view(),name='create_new_patient'), # Formulaire pour création d'unnouveau patient

	path("add_maladie/<pk>", MaladieCreateView.as_view(),name='create_new_maladie'), # Formulaire pour création d'unnouveau patient
	path("add_addiction/<pk>", AddictionCreateView.as_view(),name='create_new_addiction'), # Formulaire pour création d'unnouveau patient

	# IV. Exemple d'une URL liée à une vue qui modifie un objet (modification d'un formulaire)
	# path("patient_edit/<pk>", PatientUpdateView.as_view( ), name='edition_patient'),  # URL avec clé primaire
	path("patient_edit/<numero_secu_soc>", PatientUpdateView.as_view( ), name='edition_patient'),  # URL avec un attribut unique de Patient : numero_secu_soc

	# V. Exemple d"une URL liée à une vue pour supprimer un objet
	path("patient_del/<numero_secu_soc>", PatientDeleteView.as_view( ), name='suppression_patient'),  # URL avec un attribut unique de Patient : numero_secu_soc
	path("maladie_del/<pk>", MaladieDeleteView.as_view( ), name='suppression_maladie'),  # URL avec un attribut unique de Patient : numero_secu_soc



	# VI. Exemple d"une URL liée à une Vue pour recherche d'un patient à l'aide du package searchviews
	path("search_pat", ProfileSearchView.as_view( ), name="search_patient"),
	path("search_med", TraitementSearchView.as_view( ), name="search_traitement"),



	# VII. Exemple d"une URL liée à une vue pour l'édition du carnet de santé
	path("carnet/<numero_secu_soc>", CarnetUpdateView.as_view( ), name='edition_carnet'),  # URL avec un attribut unique de Patient : numero_secu_soc






	path("<username>/", views.view_perso2,name='espace_perso'), # Vue de l'espace perso


]
