# Generated by Django 2.0.5 on 2020-04-17 17:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addiction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_addiction', models.CharField(choices=[('tabac', 'tabac'), ('alcool', 'alcool'), ('drogue', 'drogue')], max_length=120, verbose_name="Nom de l'addiction")),
                ('degre_addiction', models.CharField(choices=[('Abstinence', 'Abstinence'), ('Usage simple', 'Usage simple'), ('Usage nocif', 'Usage nocif'), ('Dépendance', 'Dépendance')], max_length=120, verbose_name="Degré de l'addiction")),
            ],
        ),
        migrations.CreateModel(
            name='CarnetSante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antecedant', models.TextField(blank=True, null=True, verbose_name='Antecedant')),
                ('poids', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(250)], verbose_name='Poids du patient en [kg]')),
                ('taille', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(300)], verbose_name='Taille du patient en [cm]')),
                ('imc', models.IntegerField(blank=True, null=True, verbose_name='Indice de masse corporelle')),
                ('interpretation_imc', models.CharField(blank=True, max_length=120, null=True, verbose_name="Interprétation de l'IMC selon l’OMS")),
                ('ta_systolique', models.FloatField(blank=True, null=True, verbose_name='TA systolique')),
                ('ta_diastolique', models.FloatField(blank=True, null=True, verbose_name='TA diastolique')),
                ('analyse_biologique', models.CharField(blank=True, max_length=120, null=True, verbose_name='Analyses biologiques')),
                ('depistage', models.CharField(blank=True, max_length=120, null=True, verbose_name='Dépistage')),
                ('addiction', models.ManyToManyField(blank=True, null=True, to='appli_medG.Addiction')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=120, verbose_name='Titre du document')),
                ('auteur', models.CharField(max_length=120, verbose_name='Auteur du document')),
                ('date_doc', models.DateTimeField(verbose_name='Date du document')),
                ('contenu', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=120, verbose_name="Type d'examen")),
                ('date_examen', models.DateTimeField(verbose_name="Date de l'examen")),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appli_medG.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Maladie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_m', models.CharField(max_length=120, verbose_name='Nom de la maladie')),
                ('date_diagnostique', models.DateTimeField(auto_now_add=True, verbose_name='Date du diagnostique de la maladie')),
                ('statut', models.CharField(choices=[('en cours', 'En cours'), ('terminée', 'Terminée')], default='en cours', max_length=20, verbose_name='Statut')),
                ('carnet_sante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appli_medG.CarnetSante')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('civilite', models.CharField(choices=[('Mme', 'Mme'), ('Mlle', 'Mlle'), ('Mr', 'Mr')], max_length=6, verbose_name='Civilité')),
                ('nom', models.CharField(max_length=120, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=120, verbose_name='Prénom')),
                ('adresse', models.CharField(blank=True, max_length=120, null=True)),
                ('ville', models.CharField(blank=True, max_length=120, null=True)),
                ('code_postal', models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator(message='Le code postal doit comporter 5 chiffres).', regex='^\\d{5}$')])),
                ('mail', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Mail')),
                ('telephone', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Un numéro de téléphone doit être entré au format : '0999999999' (10 chiffres).", regex='^0?\\d{9}$')], verbose_name='Téléphone')),
            ],
        ),
        migrations.CreateModel(
            name='Traitement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CIS_code', models.IntegerField(max_length=120, verbose_name='CIS code')),
                ('medicament', models.CharField(max_length=120, verbose_name='Nom du médicament')),
                ('forme', models.CharField(max_length=120, verbose_name='Forme pharmaceutique')),
                ('voie_admi', models.CharField(max_length=120, verbose_name="Voies d'administration")),
                ('taux_remboursement', models.CharField(max_length=120, verbose_name='Taux de remboursement du médicament')),
                ('prix', models.FloatField(verbose_name='Prix du médiacment')),
            ],
        ),
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('personne_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appli_medG.Personne')),
                ('specialite', models.CharField(max_length=120, verbose_name='Spécialité du médecin')),
            ],
            bases=('appli_medG.personne',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('personne_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appli_medG.Personne')),
                ('numero_secu', models.CharField(max_length=120, unique=True, validators=[django.core.validators.RegexValidator(message='Le numéro de sécu doit comporter 13 chiffres.', regex='^\\d{13}$')], verbose_name='Numéro de sécurité sociale')),
                ('date_naissance', models.DateField(verbose_name='Date naissance')),
                ('lieu_naissance', models.CharField(max_length=120, verbose_name='lieu de naissance')),
                ('age', models.IntegerField()),
                ('date_premiere_visite', models.DateTimeField(auto_now_add=True, verbose_name='Date de la première visite')),
                ('date_derniere_visite', models.DateTimeField(auto_now=True, verbose_name='Date de la dernière visite')),
                ('medecin_traitant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appli_medG.Medecin')),
            ],
            bases=('appli_medG.personne',),
        ),
        migrations.AlterUniqueTogether(
            name='personne',
            unique_together={('nom', 'prenom')},
        ),
        migrations.AddField(
            model_name='maladie',
            name='traitement',
            field=models.ManyToManyField(to='appli_medG.Traitement'),
        ),
        migrations.AddField(
            model_name='carnetsante',
            name='allergie',
            field=models.ManyToManyField(blank=True, null=True, to='appli_medG.Traitement'),
        ),
        migrations.AddField(
            model_name='examen',
            name='medecin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appli_medG.Medecin'),
        ),
        migrations.AddField(
            model_name='carnetsante',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appli_medG.Patient'),
        ),
    ]
