# pour lancer : python manage.py shell
# pour lancer : exec(open("creation_objet.py").read())
from typing import Dict

from appli_medG.models import Personne, Patient, CarnetSante, Medecin, Maladie, Document, Examen, Traitement, Addiction
import datetime
import pandas as pd

CarnetSante.objects.all().delete()
Patient.objects.all().delete()
Medecin.objects.all().delete()
Maladie.objects.all().delete()
Traitement.objects.all().delete()
Addiction.objects.all().delete()




fields_1 = [
'CIS_code',         # Code CIS (Code Identifiant de Spécialité)
'nom_m',            # Dénomination du médicament
'forme',            # Forme pharmaceutique
'voie_admi',        # Voies d'administration (avec un séparateur « ; » entre chaque valeur quand il y en a plusieurs)
'statut_amin',      # Statut administratif de l’autorisation de mise sur le marché (AMM)
'type_AMM',         # Type de procédure d'autorisation de mise sur le marché (AMM)
'etat_commerce',    # Etat de commercialisation
'date_AMM',         # Date d’AMM (format JJ/MM/AAAA)
'StatutBdm',        # StatutBdm : valeurs possibles : « Alerte » (icône rouge) ou « Warning disponibilité » (icône grise)
'num_autoEUR',      # Numéro de l’autorisation européenne
'Titulaires',       # Titulaire(s) : S’il y a plusieurs titulaires, les valeurs seront séparées par des « ; »
'Surv_renforcee',   # Surveillance renforcée (triangle noir) : valeurs « Oui » ou « Non »

]

fields_2 = [
'CIS_code',              # Code CIS
'CIP7_code',             # Code CIP7 (Code Identifiant de Présentation à 7 chiffres)
'Lib',                   # Libellé de la présentation
'statut_amin',           # Statut administratif de la présentation
'etat_commerc',          # Etat de commercialisation de la présentation tel que déclaré par le titulaire de l'AMM
'date_comm',             # Date de la déclaration de commercialisation (format JJ/MM/AAAA)
'CIP13_code',           # Code CIP13 (Code Identifiant de Présentation à 13 chiffres)
'Agr_coll',             # Agrément aux collectivités ("oui", "non" ou « inconnu »)
'Taux_remboursement',        # Taux de remboursement (avec un séparateur « ; » entre chaque valeur quand il y en a plusieurs)
'Prix',                 # Prix du médicament en euro
'autre',
'Texte',                # Texte présentant les indications ouvrant droit au remboursement par l’assurance maladie s’il y a plusieurs taux de remboursement pour la même présentation.

]


url="http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt"
med1 =pd.read_csv(url, encoding = "ISO-8859-1",  sep = '\t' , index_col=0 , usecols=[0,1,2,3] , names=fields_1)

print(med1.head())

url="http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_CIP_bdpm.txt"
med2 =pd.read_csv(url, encoding = "ISO-8859-1",  sep = '\t'  , index_col=False , names=fields_2, usecols=[0,8,9] )
#
print(med2.head())


med3 = med1.join(med2.set_index("CIS_code"))
print(med3.head())

# med4 = med3[med3['nom_m'].str.contains("AUGMENT") & med3['voie_admi'].str.contains("orale")]
med4 = med3[med3['nom_m'].str.contains("AUGMENT")]
print(med4.head())





medicament_2 = med3[['nom_m','forme','voie_admi','Taux_remboursement','Prix']]
med_dict = medicament_2.to_dict()

# print(medicament_2.keys())
# print(medicament_2['nom_m'].keys())


model_instances = []
for CIS_code in med_dict['nom_m']:
    medicament_= med_dict['nom_m'][CIS_code]
    forme_= med_dict['forme'][CIS_code]
    voie_admi_= med_dict['voie_admi'][CIS_code]
    Taux_remboursement_= med_dict['Taux_remboursement'][CIS_code]
    Prix_= med_dict['Prix'][CIS_code]
    model_instances.append(Traitement(CIS_code=CIS_code, medicament=medicament_,forme=forme_, voie_admi=voie_admi_,prix=Prix_,taux_remboursement=Taux_remboursement_))

Traitement.objects.bulk_create(model_instances)
#
#
#


patients_ = [
    {"nom": 'Fuss', "prenom": 'Adrien', "civilite": 'Mr', "numero_secu": '1234', "date_naissance": datetime.date(1989, 6, 21),
     "lieu_naissance": 'Annecy'},
    {"nom": 'Michelon', "prenom": 'Laura', "civilite": 'Mlle', "numero_secu": '1275', "date_naissance": datetime.date(1991, 11, 6),
     "lieu_naissance": 'Connegliano'},
    {"nom": 'Michelon', "prenom": 'Lucio', "civilite": 'Mr', "numero_secu": '1475', "date_naissance": datetime.date(1960, 1, 1),
     "lieu_naissance": 'Connegliano'},
    {"nom": 'Ethan', "prenom": 'Chou', "civilite": 'Mr', "numero_secu": '1233', "date_naissance": datetime.date(1989, 10, 10),
     "lieu_naissance": 'Taipei'},
]


medecins_ = [
    {"nom": 'RABAH', "prenom": 'Cherif', "specialite": 'Sexologue', "adresse": 'Chez l infirmiere de garde', "mail": '',
     "telephone": '04 69 69 69 69' , "civilite": 'Mr'},
    {"nom": 'LYON-BILGER', "prenom": 'JONATHAN', "specialite": 'Generaliste', "adresse": 'AINAY LE CHÂTEAU', "mail": '',
     "telephone": '04 70 08 23 84' , "civilite": 'Mr'},
    {"nom": 'RABAN', "prenom": 'NICOLE', "specialite": 'Generaliste', "adresse": 'BOURBON LARCHAMBAULT', "mail": '',
     "telephone": '06 02 27 22 80' , "civilite": 'Mme'},
    {"nom": 'DIMICOLI', "prenom": 'CHARLES', "specialite": 'Generaliste', "adresse": 'BUXIERES LES MINES', "mail": '',
     "telephone": '04 70 66 00 41' , "civilite": 'Mr'},
    {"nom": 'DESRICHARD ', "prenom": 'JEAN-CHRISTIAN ', "specialite": 'Generaliste', "adresse": 'CERILLY ', "mail": '',
     "telephone": '04 70 67 52 51' , "civilite": 'Mr'},
    {"nom": 'FONTVIEILLE', "prenom": 'LAURENT', "specialite": 'Generaliste', "adresse": 'CHAMBLET', "mail": '',
     "telephone": '04 70 07 88 09' , "civilite": 'Mr'},
    {"nom": 'MICHELON', "prenom": 'LAURA', "specialite": 'Generaliste', "adresse": '18 rue de la glacière 69600  Oullins', "mail": 'mchl.laura@gmail.com',
     "telephone": '04 70 07 88 09' , "civilite": 'Mlle'},
]


print(medecins_)
print(patients_)


traitements_ =  [
    {"medicament": 'doliprane'},
    {"medicament": 'evian'},
    {"medicament": 'massage'},
]

patients = []
for p in patients_:
    patients.append(Patient(nom=p["nom"], prenom=p["prenom"], civilite=p["civilite"], numero_secu=p["numero_secu"], date_naissance=p["date_naissance"],
                 lieu_naissance=p["lieu_naissance"]))

medecins = []
for m in medecins_:
    medecins.append(
        Medecin(nom=m["nom"], prenom=m["prenom"], specialite=m["specialite"], adresse=m["adresse"], mail=m["mail"],
                telephone=m["telephone"], civilite=m["civilite"]))


# traitements = []
# for t in traitements_:
#     traitements.append(Traitement(medicament=t["medicament"]))
# for t in traitements: t.save()



# Association d'un traitement à une maladie
# type_maladies[0].traitement.add(traitements[0])
# type_maladies[1].traitement.add(traitements[1])
# type_maladies[2].traitement.add(traitements[2])


for p in patients: p.save()
for m in medecins: m.save()
# for m in type_maladies: m.save()




# Carnet de santé d'Adrien
# ---------------------------------------------

# Modification du code : le carnet de santé est créé automatiquement lorsque le patient est créé
# CarnetSante_Adrien = CarnetSante(patient = patients[0])  #onetoonefield : un patient a un unique carnet de sante, le carnet de sante n'appartient qu'à un seul patient
# CarnetSante_Adrien.save()

# Ajout des addictions / Foreign key : un seul objet est donné
# Toutes les addictions sont données dans Addiction un seul ensemble est possible
# addiction_Adrien = Addiction(nom_addiction ="alcool" , degre_addiction = "Abstinence")
# addiction_Adrien2 = Addiction(nom_addiction ="tabac" , degre_addiction = "Dépendance")
# addiction_Adrien.save()
# addiction_Adrien2.save()
# patients[0].carnetsante.addiction.add(addiction_Adrien)
# patients[0].carnetsante.addiction.add(addiction_Adrien2)

# Ajout de maladies / manytomanyfield : plusieurs objets possibles
# patients[0].carnetsante.maladie.add(type_maladies[0])
# patients[0].carnetsante.maladie.add(type_maladies[1])
# patients[0].carnetsante.maladie.add(type_maladies[2])
# patients[0].carnetsante.maladie.remove(type_maladies[0])     # suppression d'une  maladie
# CarnetSante_Adrien.maladie.clear() 						# supression de toutes les liaisons d'un many to many field
# print(patients[0].carnetsante.maladie.all())

# Ajout des allergies / manytomanyfield : plusieurs objets possibles
# patients[0].carnetsante.allergie.add(traitements[0]) # manytomanyfield : plusieurs objets possibles
# patients[0].carnetsante.allergie.add(traitements[1]) # manytomanyfield : plusieurs objets possibles
# patients[0].carnetsante.allergie.add(traitements[2]) # manytomanyfield : plusieurs objets possibles

patients[0].carnetsante.save()


maladies_ = [
    {"nom_m": 'grippe',},
    {"nom_m": 'alcoolisme'},
    {"nom_m": 'stress'},
]

# type_maladies = []
# for m in maladies_:
#     type_maladies.append(Maladie(nom_m=m["nom_m"],))
# for m in type_maladies: m.save()
#


for p in patients: p.save()
for m in medecins: m.save()
# for m in type_maladies: m.save()
# for t in traitements: t.save()


m = Maladie(nom_m="fievre")
m.save()

# ------------------------------------------------------------
# Impression de queryset
# ------------------------------------------------------------

# fonctions possibles : all, filter, exclude, order_by ...


# Impression sur une classe
# ------------------------------
print("\n\nAcceder à tous les patients :")
print(Patient.objects.all())  # Acceder à tous les patients

print("\n\nAcceder à certain patient avec filter :")
print(Patient.objects.filter(prenom="Laura"))  # Acceder au patient Laura

print("\n\nAcceder à certain patient avec exclude :")
print(Patient.objects.exclude(prenom="Laura"))  # Acceder a tous les patients sauf Laura

print("\n\nAcceder à tous les patients dont le lieu de naissance 'conneg'")
print(Patient.objects.filter(lieu_naissance__contains="conneg"))  # Acceder à tous les patients dont le lieu de naissance 'conneg'

print("\n\n Acceder à tous les patients né avant le 01 janvier 1989")
print(Patient.objects.filter(date_naissance__lt='1989-01-01'))  # Acceder à tous les patients né avant le 01 janvier 1989

print("\n\n Trier tous les patients en fonction de leur date de naissance")
print(Patient.objects.order_by('date_naissance'))  # Trier tous les patients en fonction de leur date de naissance

# avec une foreign_key
print("\n\nAcceder à tous les patients dont le nom de maladie contient 'stre'")
print(Patient.objects.filter(carnetsante__maladie__nom_m__contains="stre"))  # Acceder à tous les patients dont le nom de maladie contient 'stre' (avec maladie une ManyToManyField)

print("\n\nAccumulation de queryset")
Patient.objects.filter(carnetsante__maladie__nom_m__contains="stre").order_by('nom', 'prenom').reverse()  # Accumulation de queryset



# Impression sur une instance : meme principe
# ------------------------------
# avec un ManyToManyField

# fonctions possibles : all, filter, exclude, order_by ...


# print("Acceder au queryset de toutes les maladies du patient p2")
# print(patients[0].carnetsante.maladie.all())  # Acceder au queryset de toutes les maladies d'un patient

# print("\n\nAcceder au queryset de tous les patients ayant une maladie mal1")
# print(type_maladies[1].carnetsante_set.all())  # Acceder au queryset de tous les patients ayant une maladie