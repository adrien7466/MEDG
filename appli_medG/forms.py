#-*- coding: utf-8 -*-
from django import forms
from appli_medG.models import Patient, CarnetSante, Maladie, Addiction

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CreatePatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        # fields = '__all__'
        # fields = ['nom', 'prenom']
        exclude = ['date_premiere_visite','date_derniere_visite','age']

    def clean(self):
        cleaned_data =super(CreatePatientForm,self).clean()
        date_naissance = cleaned_data["date_naissance"]
        numero_secu = cleaned_data["numero_secu"]
        civilite = cleaned_data["civilite"]

        if civilite =="Mr": num = "1{:02d}{:02d}".format(int(str(date_naissance.year)[-2:]), date_naissance.month)
        else:               num=  "2{:02d}{:02d}".format(int(str(date_naissance.year)[-2:]), date_naissance.month)

        if  numero_secu[0:5]!=num:
            raise forms.ValidationError("Le numéro de sécu doit être sous la fome : 1 ou 2 +année + mois ")
        return cleaned_data

    # def __init__(self, *args, **kwargs):
    #     super(CreatePatientForm, self).__init__(*args, **kwargs)
    #
    #     # Modification du style du formulaire
    #     self.fields['adresse'].widget.attrs.update(size=20)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Utilisation de la mise en forme crispy
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'medecin_traitant',

            Row(
                Column('civilite', css_class='form-group col-md-1 mb-0'),
                Column('nom', css_class='form-group col-md-5 mb-0'),
                Column('prenom', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_naissance', css_class='form-group col-md-6 mb-0'),
                Column('lieu_naissance', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('adresse', css_class='form-group col-md-6 mb-0'),
                Column('ville', css_class='form-group col-md-4 mb-0'),
                Column('code_postal', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),

            'numero_secu',
            'mail',
            'telephone',

            Submit('submit', 'Ajoutez')
        )




class CarnetSanteForm(forms.ModelForm):
    poids   = forms.FloatField(label="Poids du patient en [kg]" ,min_value=0.0, max_value=200.0,widget=forms.NumberInput(attrs={'step': "0.1"}))
    taille  = forms.FloatField(label="Taille du patient en [cm]" ,min_value=0.0, max_value=300.0)
    imc     = forms.IntegerField(label= "Indice de masse corporelle", disabled=True, required = False )
    interpretation_imc = forms.CharField(label="Interprétation de l'IMC selon l’OMS", disabled=True, required = False )

    class Meta:
        model = CarnetSante
        fields = '__all__'
        # fields = ['nom', 'prenom']
        # exclude = ['date_premiere_visite','date_derniere_visite','age']
        widgets = {
                    'addictions': forms.CheckboxSelectMultiple(),
        }





class MaladieForm(forms.ModelForm):
    class Meta:
        model = Maladie
        fields = '__all__'


class AddictionForm(forms.ModelForm):
    class Meta:
        model = Addiction
        fields = '__all__'


class PatientSearchForm(forms.Form):
    search_text =  forms.CharField(
                    required = False,
                    label='Recherchez un nom ou prénom de patient',
                    widget=forms.TextInput(attrs={'placeholder': 'nom ou prénom'})
                  )
    search_lieu_naissance_exact = forms.CharField(
                    required = False,
                    label='Recherchez un lieu de naissance'
                  )


class TraitementSearchForm(forms.Form):
    search_text =  forms.CharField(
                    required = False,
                    label='Recherchez un nom de médicament',
                    widget=forms.TextInput(attrs={'placeholder': 'nom'})
                  )


