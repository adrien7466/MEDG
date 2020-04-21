#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from datetime import datetime
from italiano.models import Mot, Expression
from italiano.forms import TestMotForm
from django.views.generic import TemplateView, ListView, DetailView # vues génériques
from django.db.models import Q

# def accueil_it(request):
# 	mots=Mot.objects.all()
# 	expressions = Expression.objects.all()
# 	return render(request, 'italiano/accueil.html', {'mots':mots ,'expressions':expressions ,'current_date':datetime.now() }) # on passe en argument toute les variables de la fonction



# La classe ci-dessous (vue générique) fait le meme travail que la fonction définie ci-dessus
class Liste_Mots(ListView):

	model = Mot										#  model = Mot est un raccourci pour dire queryset = Mot.objects.all()
	# template_name ="italiano/mot_list.html"		# Paramétres par défaut "nom_objet_minuscule" + "_list"
	# context_object_name = "mot_list"				# Paramétres par défaut "nom_objet_minuscule" + "_list"

	def get_queryset(self):
		return Mot.objects.filter(name_fr__contains="se")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 			# Call the base implementation first to get a context
		context['expression_list'] = Expression.objects.all()  	# Add in a QuerySet of all the expression
		return context



class Detail_Mots(DetailView):
	model = Mot
	template_name ="italiano/accueil2.html"
	context_object_name = "mots"






def testMot(request):

	# GET : pas de formulaire envoyé
	# POST; formulaire complété et envoyé
	envoi = False

	if request.method == 'POST': # requete POST : lorsque le formulaire a déja été commencer à etre rempli
		form = TestMotForm(request.POST) # nous reprenons les données

		if form.is_valid(): # Nous vérifions que les toutes les données du formulaire sont valides
			# # les données du formulaire sont insérées dans l'attribut cleaned_data
			nom_it 			= form.cleaned_data["name_it"]

			envoi = True
			# return redirect('accueil')  # on donne le name


	else: # requete GET : à l'initialisation
		form = TestMotForm() # création d'un formulaire vide

	return render(request,'italiano/interrogation_mots.html',locals())

