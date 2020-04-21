from django.contrib import admin
from appli_medG.models import Patient, Medecin, Maladie, Document, Examen


class PatientAdmin(admin.ModelAdmin):
	list_display 	= ('nom', 'prenom', 'apercu_antecedant')
	# list_filter 	= ('',)
	date_hierarchy 	= 'date_naissance'
	ordering 		= ('date_naissance', )
	search_fields 	= ('sexe', 'antecedent')

	# Configuration du formulaire d'édition
	fieldsets = (
		#fieldset 1
		('Général', {
			'classes': ['collapse'],
			'fields': ('nom', 'prenom', 'sexe', 'date_naissance',)
		}),

		#fieldset 2
		('Maladies et antécédants',{
			"fields" :('maladie','antecedant')
		}),
	)

	# Colonne personnalisée
	def apercu_antecedant(self, patient):
		if patient.antecedant == None:
			return 'Aucun antécédent'
		else:
			text = patient.antecedant[0:40]
			if len(patient.antecedant) > 40:
				return '%s...' % text
			else:
				return text
		
	# En-tête de notre colonne
	apercu_antecedant.short_description = u'Aperçu des antécédents'





admin.site.register(Patient,PatientAdmin)
admin.site.register(Medecin)
admin.site.register(Maladie)
admin.site.register(Document)
admin.site.register(Examen)







# nom 					=	models.CharField('Nom du patient', max_length=120)
# prenom 					=	models.CharField('Prénom du patient', max_length=120)
# sexe 					=	models.CharField('sexe', max_length=120)
# ipp 					=	models.CharField('IPP', max_length=120)
# date_naissance  		=	models.DateTimeField('Date naissance')
# lieu_naissance			=	models.CharField('lieu de naissance', max_length=120)	
# maladie 				=	models.ManyToManyField('Maladie') 					# Un patient peut avoir plusieurs maladies
# document 				=	models.ManyToManyField('Document') 					# Un patient peut avoir eu plusieurs documents
# antecedent 				=	models.TextField(null=True)
# date_premiere_visite 	=	models.DateTimeField(auto_now_add=True, auto_now=False,	verbose_name="Date de la premiere visite")
# date_derniere_visite 	=	models.DateTimeField(auto_now_add=False, auto_now=True,	verbose_name="Date de derniere visite")
