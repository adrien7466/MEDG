from django.db import models


class Mot(models.Model):
    ''''Définition de la classe mot'''
    name_fr = models.CharField('Nom francais', max_length=120)
    name_it = models.CharField('Nom italien', max_length=120)

    def __str__(self):
        return ("{} <-> {}".format(self.name_fr,self.name_it))


class Expression(Mot):
    '''Définition d'une expression'''
    expr_fr = models.CharField('Expression francaise', max_length=120)
    expr_it = models.CharField('Expression italienne', max_length=120)

    def __str__(self):
        return ("{} <-> {}".format(self.expr_fr,self.expr_it))
