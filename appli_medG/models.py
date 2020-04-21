from django.db import models
from datetime import date
from django.core.validators import RegexValidator
from django.db.models import signals
from django.core.validators import MaxValueValidator, MinValueValidator

# Liaisons entre modèles
# ---------------------------------------------------------

# 1. ForeignKey : liaisons plusieurs-à-un
# la clé étrangère ne peut avoir qu'une seule valeur
# Exige deux paramètres : la classe à laquelle le modèle est lié et l’option on_delete.
# Lorsqu’un objet référencé par une ForeignKey est supprimé, Django simule le comportement de la contrainte SQL définie par le paramètre on_delete.
# CASCADE : Supprime en cascade. Django simule le comportement de la contrainte SQL ON DELETE CASCADE et supprime aussi l’objet contenant la clé ForeignKey.

# 2. ManyToManyField :Une relation plusieurs-à-plusieurs.
# la clé étrangère peut avoir plusieurs valeurs
# Exige un paramètre positionnel : la classe à laquelle le modèle est lié, qui fonctionne exactement de la même manière que pour ForeignKey, y compris les relations récursives et différées.
# Django génère automatiquement une table pour gérer les relations plusieurs-à-plusieurs. Cependant, si vous désirez spécifier manuellement la table intermédiaire, vous pouvez utiliser l’option through pour indiquer le modèle Django qui représente cette table intermédiaire.

# 3. OneToOneField : Une relation un-à-un.
# la clé étrangère ne peut avoir qu'une seule valeur et cette valeur est obligatoirement associé à l'objet
# Conceptuellement, ceci est similaire à un champ ForeignKey avec l’attribut unique=True, mais le côté « inverse » de la relation renvoie directement un objet unique.


class Personne(models.Model):
	abrev_civil = (
		('Mme', 'Mme'),
		('Mlle', 'Mlle'),
		('Mr', 'Mr'),
	)

	CP_regex 	= 	RegexValidator(regex=r'^\d{5}$',message="Le code postal doit comporter 5 chiffres).")
	phone_regex = RegexValidator(regex=r'^0?\d{9}$', message="Un numéro de téléphone doit être entré au format : '0999999999' (10 chiffres).")


	civilite 				=	models.CharField('Civilité',choices= abrev_civil, max_length=6)
	nom 					=	models.CharField('Nom', max_length=120)
	prenom 					=	models.CharField('Prénom', max_length=120)
	adresse					=	models.CharField(null=True,blank=True, max_length=120)
	ville					=	models.CharField(null=True,blank=True, max_length=120)
	code_postal				=	models.CharField(validators=[CP_regex],null=True,blank=True, max_length=120)
	mail					= 	models.EmailField("Mail",null=True,blank=True)
	telephone 				= models.CharField('Téléphone', validators=[phone_regex], max_length=17, blank=True,null=True)  # validators should be a list

	class Meta:
		unique_together = ('nom', 'prenom',) # Ces attributs sont uniques s'ils sont associés tous les deux


	def __str__(self):
		return "{}. {} {}".format(self.civilite, self.nom, self.prenom)



class Patient(Personne):
	secu_regex 				= 	RegexValidator(regex=r'^\d{13}$',message="Le numéro de sécu doit comporter 13 chiffres.")
	numero_secu				=	models.CharField('Numéro de sécurité sociale', max_length=120, validators=[secu_regex],unique =True)
	medecin_traitant		= 	models.ForeignKey('Medecin', null=True, on_delete=models.CASCADE)
	date_naissance  		=	models.DateField('Date naissance')
	lieu_naissance			=	models.CharField('lieu de naissance', max_length=120)
	age 					= 	models.IntegerField()
	date_premiere_visite 	=	models.DateTimeField(auto_now_add=True, auto_now=False,	verbose_name="Date de la première visite")
	date_derniere_visite 	=	models.DateTimeField(auto_now_add=False, auto_now=True,	verbose_name="Date de la dernière visite")


	def __str__(self):
		return "{}. {} {} né le {} à {}".format(self.civilite, self.nom, self.prenom, self.date_naissance, self.lieu_naissance)

	def get_age(self):
		return	date.today().year - self.date_naissance.year - ((date.today().month, date.today().day) < (self.date_naissance.month, self.date_naissance.day))

	def save(self, *args, **kwargs):
		self.age = self.get_age( )

		is_new = self.id is None
		super(Patient, self).save(*args, **kwargs)
		if is_new:
			CarnetSante.objects.create(patient=self)


		#
		# #  Creation d'un carnet de sante automatiquement
		# def create_carnetsante(sender, instance, created, **kwargs):
		# 	"""Create CarnetSante for every new Patient."""
		# 	if created:
		# 		CarnetSante.objects.create(patient=instance)
		#
		# signals.post_save.connect(create_carnetsante, sender=Patient, weak=False,
		# 						  dispatch_uid='models.create_carnetsante')






class CarnetSante(models.Model):
	patient 				= 	models.OneToOneField(Patient, on_delete=models.CASCADE)		# un patient est lié au carnet de santé, et le carnet de santé est valable que pour ce patient
	allergie				=	models.ManyToManyField('Traitement',blank=True, null=True)	# plusieurs allergies sont possibles
	antecedant 				=	models.TextField("Antecedant",blank=True, null=True)

	poids 				=	models.FloatField("Poids du patient en [kg]", null=True,validators=[MinValueValidator(0.0), MaxValueValidator(250)])
	taille				=	models.IntegerField("Taille du patient en [cm]",null=True ,validators=[MinValueValidator(0.0), MaxValueValidator(300)])
	imc					=	models.IntegerField("Indice de masse corporelle",null=True, blank=True)
	interpretation_imc	=	models.CharField("Interprétation de l'IMC selon l’OMS", max_length=120, null=True, blank=True)
	ta_systolique		=	models.FloatField("TA systolique", null=True, blank=True)
	ta_diastolique		=	models.FloatField("TA diastolique", null=True, blank=True)
	analyse_biologique	=	models.CharField("Analyses biologiques", max_length=120, null=True, blank=True)
	depistage			=	models.CharField("Dépistage", max_length=120, null=True, blank=True)



	def get_imc(self):
		if self.poids and self.taille:
			return int(self.poids/(self.taille*0.01)**2)
		else:
			return None

	def get_interpretation_imc(self):
		if self.imc:
			if self.imc<16:  		return "Anorexie ou dénutrition"
			elif self.imc<18.5:  	return "Maigreur"
			elif self.imc<25:  		return "Corpulence normale"
			elif self.imc<30:  		return "Surpoids"
			elif self.imc<35:  		return "Obésité modérée (Classe 1)"
			elif self.imc<40:  		return "Obésité élevée (Classe 2)"
			else:			  		return "Obésité morbide ou massive"
		else:
			return None

	def save(self, *args, **kwargs):
		self.imc 				= self.get_imc( )
		self.interpretation_imc = self.get_interpretation_imc( )
		super(CarnetSante, self).save(*args, **kwargs)

	def __str__(self):
		return "Carnet de santé de {}. {} {}".format(self.patient.civilite, self.patient.nom, self.patient.prenom)


class Medecin(Personne):
	specialite		= models.CharField('Spécialité du médecin', max_length=120)

	def __str__(self):
		"""Méthode permettant d'afficher plus joliment notre objet"""
		return "{}. {} {} ({})".format(self.civilite, self.nom, self.prenom,self.specialite)


class Maladie(models.Model):
	# une maladie ne peut correspondre qu'a un seul carnet de sante
	# pluseirurs maladies peuvent appartenir à un carnet de sante
	carnet_sante		= models.ForeignKey('CarnetSante', null=True, blank=True, on_delete=models.CASCADE)
	nom_m 				= models.CharField('Nom de la maladie', max_length=120)
	date_diagnostique 	= models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Date du diagnostique de la maladie")
	traitement 			= models.ManyToManyField('Traitement')


	statut_maladie = (
		('en cours','En cours'),
		('terminée','Terminée'),
	)
	statut 				=	models.CharField('Statut',default ='en cours', choices= statut_maladie, max_length=20)

	def __str__(self):
		return "{} ({})".format(self.nom_m,self.statut)



class Traitement(models.Model):
	CIS_code = models.IntegerField('CIS code', max_length=120)
	medicament = models.CharField('Nom du médicament', max_length=120)
	forme = models.CharField('Forme pharmaceutique', max_length=120)
	voie_admi = models.CharField("Voies d'administration", max_length=120)
	taux_remboursement =models.CharField("Taux de remboursement du médicament", max_length=120)
	prix	= models.CharField("Prix du médiacment", max_length=120)

	def __str__(self):
		return self.medicament



class Addiction(models.Model):
	type_addiction = (
		('tabac','tabac'),
		('alcool','alcool'),
		('drogue','drogue'),
	)

	type_degre_addiction = (
		('Abstinence','Abstinence'),
		('Usage simple','Usage simple'),
		('Usage nocif','Usage nocif'),
		('Dépendance','Dépendance'),
	)
	carnet_sante		= models.ForeignKey('CarnetSante', null=True, blank=True, on_delete=models.CASCADE)
	nom_addiction 	= models.CharField("Nom de l'addiction", choices=type_addiction, max_length=120)
	degre_addiction = models.CharField("Degré de l'addiction", choices=type_degre_addiction, max_length=120)

	def __str__(self):
		return "{} ({})".format(self.nom_addiction , self.degre_addiction)


class Document(models.Model):
	titre 			= models.CharField('Titre du document', max_length=120)
	auteur 			= models.CharField('Auteur du document', max_length=120)
	date_doc		= models.DateTimeField('Date du document')
	contenu 		= models.TextField(null=True)

	def __str__(self):
		"""Méthode permettant d'afficher plus joliment notre objet"""
		return "{} écrit par {}, le {}".format(self.titre, self.auteur,self.date_doc)



class Examen(models.Model):
	medecin 		= models.ForeignKey('Medecin', null=True , on_delete=models.CASCADE) # un medecin est le rédacteur de l'examen
	type			= models.CharField("Type d'examen", max_length=120)
	date_examen		= models.DateTimeField("Date de l'examen")
	# image
	document 		= models.ForeignKey('Document', null=True , on_delete=models.CASCADE)

	def __str__(self):
		return "{} / {}".format(self.type , self.medecin)


