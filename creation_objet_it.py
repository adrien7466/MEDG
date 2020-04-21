# pour lancer : python manage.py shell
# pour lancer : exec(open("creation_objet.py").read(
from typing import Dict

from italiano.models import Mot, Expression
from datetime import datetime

noms_ = {}
noms_["une question"] = "una domanda"
noms_["la valise"] = "la valigia"
noms_["la liste"] = "l' elenco"
noms_["un tee-shirt"] = "una maglietta"
noms_["le permis de conduire"] = "la patente"
noms_["l'immatriculation"] = "la targa"
noms_["la carte"] = "la scheda"
noms_["un pull"] = "un maglione"
noms_["un tee-shirt manches  longues"] = "una maglia"
noms_["la chemise"] = "la camicia"
noms_["un déménagement"] = "un trasloco"
noms_["le moustique"] = "la zanzara"
noms_["la mouche"] = "la mosca"
noms_["l'abeille"] = "l'ape"
noms_["la guêpe"] = "la vespa"
noms_["l'oiseau"] = "l'uccello"
noms_["le coq"] = "il gallo"
noms_["la poule"] = "la gallina"
noms_["la dinde"] = "il tacchino"
noms_["un sac à dos"] = "un zaino"
noms_["un milier"] = "un migliaio"
noms_["un cousin"] = "un cugino"
noms_["une conséquence"] = "una conseguenza"
noms_["un gros mot"] = "un parolacce"
noms_["amusante"] = "divertente"
noms_["blanc"] = "bianco"
noms_["blanche"] = "bianca"
noms_["noir"] = "nero"
noms_["noire"] = "nera"
noms_["rouge"] = "rosso"
noms_["bleu"] = "azurro"
noms_["bleue"] = "azurra"
noms_["jaune"] = "giallo"
noms_["vert"] = "verde"
noms_["marron"] = "marrone"
noms_["orange"] = "arancione"
noms_["violet"] = "viola"
noms_["rose"] = "rosa"
noms_["âgé"] = "anziano"
noms_["voilà"] = "ecco"
noms_["vraiment"] = "proprio"
noms_["enfin] =  bref"] = "insomma"
noms_["écouter"] = "sentire"
noms_["se déplacer"] = "spostarsi"
noms_["déplacer"] = "spostare"
noms_["danser"] = "ballare"
noms_["skier"] = "sciare"
noms_["patiner"] = "pattinare"
noms_["marcher"] = "camminare"
noms_["courir"] = "correre"
noms_["déménager"] = "traslocare"
noms_["se bouger"] = "muoversi"
noms_["porter (des vêtements)"] = "indossare"
noms_["envoyer"] = "spedire"
noms_["s'envoyer"] = "spedirsi"
noms_["utiliser"] = "utilizzare"
noms_["se trouver"] = "trovarsi"

expressions_ = {}
expressions_["Peu importe / ca ne fait rien"] = "Non importa"
expressions_["oh là là] =  mince"] = "caspita"
expressions_["a lieu / se passe"] = "si svolge"
expressions_["Et ainsi de suite"] = "e cosi via"
expressions_["par exemple"] = "per esempio"
expressions_["pour plus de renseignements"] = "per maggiori informazioni"
expressions_["en moyenne"] = "in media"
expressions_["d'après toi"] = "secondo te"
expressions_["en compensation/en revanche"] = "in compenso"


noms = []
for k,v in noms_.items():    noms.append(Mot(name_fr=k, name_it=v,))
for n in noms: n.save()


expressions = []
for k,v in expressions_.items():    expressions.append(Expression(expr_fr=k, expr_it=v,))
for n in expressions: n.save()