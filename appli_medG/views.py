# -*- coding: utf-8 -*-
from typing import Optional, Any

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
import time

from appli_medG.models import Patient, Medecin, Maladie, Document, Examen, CarnetSante, Traitement, Addiction
from appli_medG.forms import CreatePatientForm, PatientSearchForm, CarnetSanteForm, MaladieForm, TraitementSearchForm, AddictionForm
from functools import reduce
import operator

from search_views.search import SearchListView
from search_views.filters import BaseFilter



# --------------------------------------
# vues génériques
# --------------------------------------
# 1. vues génériques de base
from django.views.generic import View, TemplateView, RedirectView

# 2. Vues génériques d'affichage
from django.views.generic import ListView, DetailView

# 3. Vues génériques d'édition
from django.views.generic import FormView, CreateView, UpdateView, DeleteView

# 4. Vues génériques basées sur les dates
# from django.views.generic import ArchiveIndexView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView


# --------------------------------------------
# Méthodes des vues génériques
# --------------------------------------------
'''
# get_context_data  
# -------------------------------
def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs) 					# Call the base implementation first to get a context
    # context = super(PatientListView,self).get_context_data(**kwargs) 			# Call the base implementation first to get a context
    context = ListView.get_context_data(self, **kwargs)
    context['current_date'] = datetime.now( )
    return context



# get_queryset -> Pour une vue générique : ListView
# -------------------------------
def get_queryset(self):
    # return Patient.objects.filter(nom__contains="Fu")

# obtenir un queryset avec les données de l'url
def get_queryset(self):
    self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
    return Book.objects.filter(publisher=self.publisher)

# get_object -> Pour une vue générique DetailView, UpdateView
# -------------------------------

# Modification de paramètre
def get_object(self):
    # On récupère l'objet via la superclass içi la superclass est DetailView et possède la méthode get_objet
    # patient = super(PatientDetailView,self).get_object()
    # patient = super().get_object()
    patient = DetailView.get_object(self)
    patient.date_derniere_visite = datetime.now( )
    patient.save( )

    return patient

# Pour obtenir un objet avec autre chose que la clé primaire pk
def get_object(self):
    numero_secu_ = self.kwargs.get('numero_secu_soc',None) # on recupere l'ipp donné en argument denas l'url
    return get_object_or_404(Patient, numero_secu=numero_secu_) # renvoi l'objet dont l'ipp correspond à celui fournit



# form_valid -> FormView, CreateView, UpdateView / Redéfinition de la méthode form_valid appelé lorsque le formulaire est validée
# -------------------------------

# ajout de fonctionalités
def form_valid(self, form):
    self.object =form.save()                                # enregistrement des modifications
    messages.success(self.request,"La fiche patient est bien remplie")                 # ajout de fonctionalités
    return HttpResponseRedirect(self.get_success_url())     # redirection de l'utilisateur


'''



# I. Exemple d'une vue avec une liste d'instance d'un modèle
# ------------------------------------------------------------------------------------

# I.1. Fonction prenant en argument la requete HTTP
def accueil(request):
    patients = Patient.objects.all( )
    return render(request, 'appli_medG/accueil.html', {'derniers_patients': patients,
                                                       'current_date': datetime.now( )})  # on passe en argument toute les variables de la fonction


# I.2. Classe basée sur la vue générique ListView
class PatientListView(ListView):

    # Les deux commandes ci dessous sont équivalentes : soit on fournit model soit queryset
    # L'avantage avec queryset c'est qu'on peut filtrer les données
    model = Patient  # model = Patient est un raccourci pour dire queryset = Patient.objects.all()
    # queryset = Patient.objects.all()

    # optionnel
    # -----------
    # context_object_name 		= 	"patient"						# Paramétres par défaut "nom_objet_minuscule"
    template_name = "appli_medG/accueil.html"  # Paramétres par défaut "nom_objet_minuscule" + "_list"
    # template_name = "appli_medG/accueil.html"  # Paramétres par défaut "nom_objet_minuscule" + "_list"

    # Surcharge de la methode get_context_data
    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs) 					# Call the base implementation first to get a context
        # context = super(PatientListView,self).get_context_data(**kwargs) 			# Call the base implementation first to get a context
        context = ListView.get_context_data(self, **kwargs)
        context['current_date'] = datetime.now( )
        return context

    def get_queryset(self):
        # return Patient.objects.all()

        # Les deux lignes ci-dessous sont équivalente
        # return Patient.objects.filter(nom__contains="Fu")
        # return Patient.objects.filter(Q(nom__contains="Fu")) # utilisation de l'objet Q

        # return Patient.objects.filter(Q(nom__contains="Fu") | Q(prenom__contains="Chou") ) # operateur OU
        # return Patient.objects.filter(~Q(nom__contains="Fu")) # operateur negation
        # return Patient.objects.filter(Q(nom__contains="Fu"),  Q(prenom__contains="Chou") ) # opérateur ET
        #
        # autres exemples
        conditions = [('nom','Fuss'),('nom','Michelon')]
        objet_q = [Q(x) for x in conditions]
        return Patient.objects.filter(reduce(operator.or_,objet_q))


class TraitementListView(ListView):
    model = Traitement

# ------------------------------------------------------------------------------------


# II. Exemple d'une vue avec un objet précis d'un modèle
# ------------------------------------------------------------------------------------

# II.1. Fonction prenant en argument la requete HTTP
def description(request, id):
    patient = get_object_or_404(Patient, id=id)
    return render(request, 'appli_medG/description.html', {'patient': patient, 'maladies': patient.maladie.all})


# II.2. Classe basée sur la vue générique DetailView
class PatientDetailView(DetailView):
    model = Patient

    # optionnel
    # -----------
    # context_object_name 		= 	"patient"								# Paramétres par défaut "nom_objet_minuscule"
    # template_name 			=	"appli_medG/patient_detail.html"		# Paramétres par défaut "nom_objet_minuscule" + "_detail"

    # Optionel: pour modification d'un attribut de l'objet
    def get_object(self):
        # On récupère l'objet via la superclass içi la superclass est DetailView et possède la méthode get_objet
        # patient = super(PatientDetailView,self).get_object()
        # patient = super().get_object()
        patient = DetailView.get_object(self)
        patient.date_derniere_visite = datetime.now( )
        patient.save( )

        # accès a la requete
        # print(self.request)

        return patient


# ------------------------------------------------------------------------------------


# III. Exemple d'une vue avec un formulaire
# ------------------------------------------------------------------------------------

# III.1. Fonction prenant en argument la requete HTTP
def createPatient(request):
    # GET : pas de formulaire envoyé
    # POST; formulaire complété et envoyé
    envoi = False
    if request.method == 'POST':  # requete POST : lorsque le formulaire a déja été commencer à etre rempli
        form = CreatePatientForm(request.POST)  # nous reprenons les données

        if form.is_valid( ):  # Nous vérifions que les toutes les données du formulaire sont valides
            form.save( )  # on sauve les données dans la base de données
            envoi = True
            return redirect('accueil')  # on donne le name
    else:  # requete GET : à l'initialisation
        form = CreatePatientForm( )  # création d'un formulaire vide
    return render(request, 'appli_medG/patient_form.html', locals( ))



# III.2. Classe basée sur la vue View
class PatientCreateView(View):
    form_class = CreatePatientForm
    template_name = 'appli_medG/patient_form.html'
    # initial = {"nom" : "Fuss"}
    initial = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('accueil')
        return render(request,self.template_name,{'form':form})



# III.3. Classe basée sur la vue générique CreateView
class PatientCreateView2(CreateView):
    model = Patient
    form_class = CreatePatientForm
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci

    # optionnel
    # -----------
    # template_name 	= 'appli_medG/patient_form.html' # Paramétres par défaut "nom_objet_minuscule" + "_form"

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(PatientDetailView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['medecin_traitant'] = Medecin.objects.filter(nom__contains="Fu")

        return initial

class MaladieCreateView(CreateView):
    model = Maladie
    form_class = MaladieForm
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci

    def get_initial(self):
        initial = super().get_initial()
        # cpf - it's the name of the field on your current form
        # self.args will be filled from URL. I'd suggest to use named parameters
        # so you can access e.g. self.kwargs['cpf_initial']

        pk = self.kwargs['pk']
        pat= get_object_or_404(Patient, pk=pk) # renvoi l'objet dont l'ipp correspond à celui fournit
        initial['carnet_sante'] = pat.carnetsante
        return initial


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 					# Call the base implementation first to get a context
        context['patient_pk'] = self.kwargs['pk']
        return context



class AddictionCreateView(CreateView):
    model = Addiction
    form_class = AddictionForm
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci

    def get_initial(self):
        initial = super().get_initial()
        # cpf - it's the name of the field on your current form
        # self.args will be filled from URL. I'd suggest to use named parameters
        # so you can access e.g. self.kwargs['cpf_initial']

        pk = self.kwargs['pk']
        pat= get_object_or_404(Patient, pk=pk) # renvoi l'objet dont l'ipp correspond à celui fournit
        initial['carnet_sante'] = pat.carnetsante
        return initial


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 					# Call the base implementation first to get a context
        context['patient_pk'] = self.kwargs['pk']
        return context




# IV. Exemple d'une vue avec un formulaire pré-rempli pour un objet qui existe déja
# ------------------------------------------------------------------------------------
class PatientUpdateView( UpdateView):
    model = Patient
    form_class = CreatePatientForm
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci

    # optionnel
    # -----------
    template_name = 'appli_medG/patient_update_form.html'  # Paramétres par défaut "nom_objet_minuscule" + "_form"

    # Optionel: pour obtenir un objet avec autre chose que la clé primaire pk
    def get_object(self):

        numero_secu_ = self.kwargs.get('numero_secu_soc',None) # on recupere l'ipp donné en argument denas l'url
        print(self.args) # Tuple lié à la vue
        print(self.kwargs) # Dictionnaire lié à la vue : {'ipp_numero': '656'}
        print(self.request) # requete liée à la vue : <WSGIRequest: GET '/medG/patient_edit/656'>
        print(self.request.method) # method
        print(self.request.user) # user
        # print(self.request.__dict__) #  données associées à l'objet request:



        return get_object_or_404(Patient, numero_secu=numero_secu_) # renvoi l'objet dont l'ipp correspond à celui fournit

    # Optionnel : redéfinition de la méthode form_valid appelé lorsque le formulaire est validée
    def form_valid(self, form):
        self.object =form.save()                                # enregistrement des modifications
        messages.success(self.request,"La fiche patient est bien remplie")                 # ajout de fonctionalités
        return HttpResponseRedirect(self.get_success_url())     # redirection de l'utilisateur


# V. Exemple d'une vue pour la suppression d'un objet
# -----------------------------------------------------------------------------------
class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci

    # optionnel
    # -----------
    # template_name = 'appli_medG/patient_confirm_delete.html'  # Paramétres par défaut "nom_objet_minuscule" + "_confirm_delete"
    # context_object_name 		= 	"patient"								# Paramétres par défaut "nom_objet_minuscule"


    # Optionel: pour obtenir un objet avec autre chose que la clé primaire pk
    def get_object(self):
        numero_secu_ = self.kwargs.get('numero_secu_soc',None) # on recupere l'ipp donnée en argument denas l'url
        return get_object_or_404(Patient, numero_secu=numero_secu_) # renvoi l'objet dont l'ipp correspond à celui fournit




class MaladieDeleteView(DeleteView):
    model = Maladie
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci




class AddictionDeleteView(DeleteView):
    model = Addiction
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci




# VI. Vue pour recherche d'un patient à l'aide du package searchviews
# -----------------------------------------------------------------------------------

class PatientFilter(BaseFilter):
    search_fields = {
        'search_text' : ['nom', 'prenom'],
        'search_lieu_naissance_exact': {'operator': '__exact', 'fields': ['lieu_naissance']},
    }


class ProfileSearchView(SearchListView):
    model = Patient
    paginate_by = 30
    template_name = "appli_medG/patient_search_form.html"
    form_class = PatientSearchForm
    filter_class = PatientFilter


class TraitementFilter(BaseFilter):
    search_fields = {
        'search_text' : ['medicament']
    }


class TraitementSearchView(SearchListView):
    model = Traitement
    paginate_by = 30
    template_name = "appli_medG/traitement_search_form.html"
    form_class = TraitementSearchForm
    filter_class = TraitementFilter



# VII. Exemple d'une vue pour l'édition du carnet de santé
# -----------------------------------------------------------------------------------
class CarnetUpdateView(UpdateView):
    model = CarnetSante
    form_class = CarnetSanteForm
    success_url = reverse_lazy("accueil")  # avec reverse_lazy on a accès à l'URL en donnant le nom de celle-ci

    # optionnel
    # -----------
    template_name = 'appli_medG/carnet_sante_form.html'  # Paramétres par défaut "nom_objet_minuscule" + "_form"

    # Optionel: pour obtenir un objet avec autre chose que la clé primaire pk
    def get_object(self):
        numero_secu_ = self.kwargs.get('numero_secu_soc',None) # on recupere l'ipp donné en argument denas l'url
        patient = get_object_or_404(Patient, numero_secu=numero_secu_)
        return patient.carnetsante








#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
def view_perso2(request, username):
    """ Vue qui affiche un article selon son identifiant (ou ID,
    ici un numéro). Son ID est le second paramètre de la fonction
    (pour rappel, le premier paramètre est TOUJOURS la requête de
    l'utilisateur) """

    if username == "Lau":
        text = "C'est ton espace perso " + username + " tu peux partager des photos de noir ici"
        nom_image = "/appli_medG/image/Cam_lacourt.jpg"
    elif username == "chou":
        text = username + " est un gros deguelasse"
        nom_image = "/appli_medG/image/chinois.gif"
    elif username == "Beppina":
        text = "ici c'est pour les photos de fleurs"
        nom_image = "/appli_medG/image/fleurs.jpg"
    elif username == "Bianca":
        text = "tanti cappelli " + username
        nom_image = "/appli_medG/image/bianca.jpg"
    elif username == "Adriano":
        text = "ici espace perso de adriano attention confidentiel !!!!!!!!!!!!!!! beaucoup de blonde  Voici ma blonde preferée qui est toujours dans la bonne position... Celle du kaka"
        nom_image = "/appli_medG/image/lindsey_von.jpg"

    elif username == "toto":  # Exemple de redirection vers une autre URL
        return redirect('accueil')  # on donne le name

    else:
        raise Http404  # Exemple pour retour d'une page d'erreur

    return render(request, 'appli_medG/page_perso.html',locals( ))  # on passe en argument toute les variables de la fonction
