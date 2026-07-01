
# hopital/forms.py
from django import forms
from .models import Etudiant, DossierMedical, Medecin, RendezVous, Consultation, Medicament, Prescription,Vaccination
from django.core.validators import RegexValidator,MinValueValidator  
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.utils import timezone
from django.db.models import Q
import datetime
from django.contrib.auth.forms import AuthenticationForm
class ConnexionForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'required': True,
        'autofocus': True,
        'placeholder': "Nom d'utilisateur"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': True,
        'placeholder': 'Mot de passe'
    }))

# ===== Formulaire Etudiant =====
class EtudiantForm(forms.ModelForm):
    nom = forms.CharField(
        max_length=50,
        required=True,
        validators=[Etudiant.lettres_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    prenom = forms.CharField(
        max_length=50,
        required=True,
        validators=[Etudiant.lettres_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    CIN = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'CIN'}))
    CNE = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'CNE'}))

    date_naissance = forms.DateField(
    required=True,
    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
    input_formats=['%Y-%m-%d']
)

    filiere = forms.ChoiceField(
        choices=[('', '--- Sélectionnez une filiere ---')] +list(Etudiant.FILIERES),
        required=True
    )

    niveau = forms.ChoiceField(
        choices=[('', '--- Sélectionnez un niveau---')] +list(Etudiant.NIVEAUX),
        required=True
    )

    sexe = forms.ChoiceField(
    choices=[('', '--- Sélectionnez un sexe ---'), ('M','M'), ('F','F')],
    required=True
)

    telephone = forms.CharField(
        max_length=20,
        required=True,
        validators=[Etudiant.telephone_regex],
        widget=forms.TextInput(attrs={'placeholder': 'Téléphone'})
    )

    ville = forms.ChoiceField(
        choices=[('', '--- Sélectionnez une ville ---')] +list(Etudiant.VILLES_MAROC),
        required=True
    )

    class Meta:
        model = Etudiant
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # remplir automatiquement le champ date_naissance si instance existe
        if self.instance and self.instance.pk:
            self.fields['date_naissance'].initial = self.instance.date_naissance
    def clean_CIN(self):
        CIN = self.cleaned_data.get('CIN')
    # Récupérer l'ID de l'étudiant en cours si c'est une modification
        etudiant_id = self.instance.id if self.instance else None
    # Vérifier s'il existe un autre étudiant avec le même CIN
        if Etudiant.objects.filter(CIN=CIN).exclude(id=etudiant_id).exists():
           raise ValidationError("CIN déjà utilisé.")
        return CIN
    def clean_CNE(self):
        CNE = self.cleaned_data.get('CNE')
    # Rune modification
        etudiant_id = self.instance.id if self.instance else None
    # Vérifier s'il existe un autre étudiant avec le même CNE
        if Etudiant.objects.filter(CNE=CNE).exclude(id=etudiant_id).exists():
            raise ValidationError("CNE déjà utilisé.")  
        return CNE
COUVERTURE_CHOICES = [
    ('CNSS', 'CNSS'),
    ('AMO', 'AMO'),
    ('RAMED', 'RAMED'),
    ('CNOPS', 'CNOPS'),
    ('Atlanta', 'Atlanta Assurances'),
    ('Wafa Assurance', 'Wafa Assurance'),
    ('RMA', 'RMA Assurances'),
    ('AXA', 'AXA Assurance Maroc'),
    ('Allianz', 'Allianz Maroc'),
    ('Saham', 'Saham Assurance'),
    ('MCMA', 'MCMA Assurances'),
    ('Zurich', 'Zurich Maroc'),
    ('Salama', 'Salama Assurances'),
    ('Autre', 'Autre (à préciser)'),
]

# ===== Formulaire DossierMedical =====
class DossierMedicalForm(forms.ModelForm):
    etudiant = forms.ModelChoiceField(
        queryset=Etudiant.objects.all(),
        required=True,
        label="Étudiant",
        widget=forms.Select(attrs={'class': 'autocomplete'}),
        error_messages={'required': "Veuillez sélectionner un étudiant."})
    couverture_medicale_select = forms.ChoiceField(
        choices=[('', '--- Sélectionnez une couverture medicale ---')] + list(COUVERTURE_CHOICES),
        required=True,
        label="Couverture médicale")
    couverture_medicale_autre = forms.CharField(
        max_length=100,
        required=False,
        label="Autre couverture",
        widget=forms.TextInput(attrs={'placeholder': 'Si autre, précisez ici'}) )
    allergies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Allergies', 'rows': 2})
    )
    maladies_chroniques = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Maladies chroniques', 'rows': 2})
    )
    groupe_sanguin = forms.ChoiceField(
        choices=[('', '--- Sélectionnez un groupe sanguin ---')] + list(DossierMedical.GROUPE_SANGUIN_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = DossierMedical
        fields = ['etudiant', 'groupe_sanguin', 'allergies', 'maladies_chroniques', 'couverture_medicale']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['etudiant'].widget = forms.HiddenInput()
        if not self.instance.pk:
            self.fields['etudiant'].queryset = Etudiant.objects.exclude(
                id__in=DossierMedical.objects.values('etudiant')
            )
        else:
            # garder le même étudiant
            self.fields['etudiant'].queryset = Etudiant.objects.filter(id=self.instance.etudiant.id)
            self.fields['etudiant'].disabled = True
            
            
        # ----- Gestion couverture médicale -----
        if self.instance and self.instance.pk:
            valeur = self.instance.couverture_medicale
            if valeur in dict(COUVERTURE_CHOICES).keys():
                self.fields['couverture_medicale_select'].initial = valeur
            else:
                self.fields['couverture_medicale_select'].initial = 'Autre'
                self.fields['couverture_medicale_autre'].initial = valeur

    # Nettoyage couverture
    def clean(self):
        cleaned_data = super().clean()
        select = cleaned_data.get('couverture_medicale_select')
        autre = cleaned_data.get('couverture_medicale_autre')
        if select == 'Autre' and not autre:
            self.add_error('couverture_medicale_autre', "Merci de préciser votre couverture médicale.")
        if select == 'Autre':
            cleaned_data['couverture_medicale'] = autre
        else:
            cleaned_data['couverture_medicale'] = select
        return cleaned_data

    # Enregistrer correctement
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.couverture_medicale = self.cleaned_data.get("couverture_medicale")
        if commit:
            instance.save()
        return instance

    # Empêcher double dossier
    def clean_etudiant(self):
        etudiant = self.cleaned_data['etudiant']
        if self.instance.pk:
            if self.instance.etudiant == etudiant:
                return etudiant
        if DossierMedical.objects.filter(etudiant=etudiant).exists():
            self.add_error('etudiant', "Cet étudiant a déjà un dossier médical.")
        return etudiant
     

    

# ===== Formulaire Medecin =====
class MedecinForm(forms.ModelForm):
    # Validateur pour le nom et prénom : seulement lettres et espaces
    lettres_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ ]+$',
        message='Ce champ ne peut contenir que des lettres et des espaces.')
    nom = forms.CharField(
        max_length=50,
        validators=[lettres_validator],
        required=True,
        label="Nom")
    prenom = forms.CharField(
        max_length=50,
        validators=[lettres_validator],
        required=True,
        label="Prénom")
    specialite = forms.CharField(
        max_length=50,
        validators=[lettres_validator],
        required=True,
        label="Spécialité")
    telephone_regex = RegexValidator(
        regex=r'^(\+212[ ]?[67]\d{8}|\+33[ ]?6\d{8}|0[67]\d{8})$',
        message="Numéro de téléphone invalide")
    telephone = forms.CharField(
        max_length=20,
        validators=[telephone_regex],
        required=True,
        label="Téléphone")

    # Rendez-vous par jour : nombre positif
    rdv_jr = forms.IntegerField(
        min_value=0,
        required=True,
        label="Nombre de RDV par jour"
    )
    salaire = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,  # > 0
        required=True,
        label="Salaire (DH)"
    )

    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'specialite', 'telephone', 'rdv_jr','salaire']

# ===== Formulaire RendezVous =====

class RendezVousForm(forms.ModelForm):
    # Champs cachés pour stocker les IDs sélectionnés via autocomplete
    etudiant = forms.ModelChoiceField(
    queryset=Etudiant.objects.all(),
    required=True,
    label="Étudiant",
    error_messages={'required': "Étudiant est un champ obligatoire."}  # message personnalisé
    )
    medecin = forms.ModelChoiceField(
        queryset=Medecin.objects.all(),
        required=True,
        label="Médecin",
        error_messages={'required': "Médecin est un champ obligatoire."} )
    date_rdv = forms.DateField(
       widget=forms.DateInput(attrs={'type': 'date', 'value': ''}, format='%Y-%m-%d'),
        required=True,
        label="Date du rendez-vous")
    HEURE_CHOICES = [(h, h) for h in [
    "09:00","09:30","10:00","10:30","11:00","11:30","12:00",
    "14:00","14:30","15:00","15:30","16:00","16:30","17:00"]]
    heure = forms.ChoiceField(
        required=True,
        label="Heure du rendez-vous",)
    STATUT_CHOICES = [
        ('prévu', 'prévu'),
       
        ('effectué', 'effectué'),
        ('raté', 'raté'),]
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=True,
        initial='prévu',
        label="Statut")
    class Meta:
        model = RendezVous
        fields = ['etudiant', 'medecin', 'date_rdv', 'heure', 'statut']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['etudiant'].queryset = Etudiant.objects.all()
        self.fields['medecin'].queryset = Medecin.objects.all()
        HEURE_CHOICES = [(h, h) for h in [
    "09:00","09:30","10:00","10:30","11:00","11:30","12:00",
    "14:00","14:30","15:00","15:30","16:00","16:30","17:00"
]]
        # Ajouter l’option vide uniquement si création
        # Définir les choix
        self.fields['heure'].choices = [('', '--- Sélectionnez heure du rendez-vous ---')] + HEURE_CHOICES
        if self.instance.pk and self.instance.date_rdv:
           self.fields['date_rdv'].initial = self.instance.date_rdv.strftime("%Y-%m-%d")
# Préremplir si modification
        if self.instance.pk and self.instance.heure:
            self.fields['heure'].initial = self.instance.heure.strftime("%H:%M")
    def clean_etudiant(self):
        etudiant = self.cleaned_data.get('etudiant')
        # Vérifie si l’étudiant a un dossier médical
        if not DossierMedical.objects.filter(etudiant=etudiant).exists():
            raise forms.ValidationError("Cet étudiant n'a pas encore de dossier médical. Impossible de prendre rendez-vous.")
        return etudiant
    def clean(self):
        cleaned_data = super().clean()
        date_rdv = cleaned_data.get('date_rdv')
        medecin = cleaned_data.get('medecin')
        etudiant = cleaned_data.get("etudiant")
        heure = cleaned_data.get("heure")
        if etudiant and date_rdv and heure:
          qs = RendezVous.objects.filter(etudiant=etudiant, date_rdv=date_rdv, heure=heure)
          if self.instance.pk:
             qs = qs.exclude(pk=self.instance.pk)
          if qs.exists():
             self.add_error('etudiant', "Cet étudiant a déjà un rendez-vous à cette date et heure.")

        if medecin and date_rdv and heure:
           qs = RendezVous.objects.filter(medecin=medecin, date_rdv=date_rdv, heure=heure)
           if self.instance.pk:  # si modification
              qs = qs.exclude(pk=self.instance.pk)
           if qs.exists():
              self.add_error('medecin', "Ce médecin a déjà un rendez-vous à cette date et heure.")
        # Vérifier le nombre de RDV pour ce médecin ce jour
        # Vérifier la limite RDV par jour pour ce médecin
        if medecin and date_rdv:
            rdv_count = RendezVous.objects.filter(medecin=medecin, date_rdv=date_rdv)
            if self.instance.pk:
                rdv_count = rdv_count.exclude(pk=self.instance.pk)
            if rdv_count.count() >= medecin.rdv_jr:
               self.add_error('medecin', f"Le médecin {medecin.nom} {medecin.prenom} a atteint la limite de RDV pour ce jour.")
        return cleaned_data
    def clean_date_rdv(self):
        date_rdv = self.cleaned_data.get('date_rdv')
        if date_rdv:
            # renvoie 5 pour samedi et 6 pour dimanche
            if date_rdv.weekday() >= 5:
                raise ValidationError("Vous ne pouvez pas prendre de rendez-vous le week-end.")
        return date_rdv
    
    
# ===== Formulaire Consultation =====
class ConsultationForm(forms.ModelForm):
    dossier = forms.ModelChoiceField(
        queryset=DossierMedical.objects.all(),
        required=True,
        label="Dossier médical",
        widget=forms.HiddenInput() ,
         error_messages={
        'required': "Veuillez sélectionner un dossier."} )
    medecin = forms.ModelChoiceField(
        queryset=Medecin.objects.all(),
        required=True,
        label="Médecin",
        widget=forms.HiddenInput(),
        error_messages={
        'required': "Veuillez sélectionner un médecin."}  
    )

    rdv = forms.ModelChoiceField(
        queryset=RendezVous.objects.all(),
        required=True,
        label="Rendez-vous",
    error_messages={
        'required': "Veuillez sélectionner un redez-vous."}
    )

    diagnostic = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Diagnostic"
    )

    class Meta:
        model = Consultation
        fields = ['dossier', 'medecin', 'rdv', 'diagnostic']
        error_messages = {
            'dossier': {'required': "Vous devez sélectionner un dossier médical."},
            'medecin': {'required': "Vous devez sélectionner un médecin."},
            'rdv': {'required': "Vous devez sélectionner un rendez-vous."},
        }
        
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
        
     # RDV disponibles (non encore associés à une consultation)
       rdv_queryset = RendezVous.objects.filter(consultation__isnull=True).order_by('date_rdv', 'heure')

    # On inclut le RDV existant dans le queryset si modification
       if self.instance.pk and self.instance.rdv:
             rdv_queryset = rdv_queryset | RendezVous.objects.filter(pk=self.instance.rdv.pk)
    #  appliquer la queryset dans TOUS les cas (POST & GET & errors)
       self.fields['rdv'].queryset = rdv_queryset

    def clean_rdv(self):
        rdv = self.cleaned_data.get('rdv')
        if not rdv:
           self.add_error('rdv', " Vous devez sélectionner un rendez-vous.")
           return None

        qs = Consultation.objects.filter(rdv=rdv)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            self.add_error('rdv', " Ce rendez-vous est déjà associé à une consultation.")

        return rdv

    def clean_dossier(self):
        dossier = self.cleaned_data.get('dossier')
        if not dossier:
            self.add_error('dossier', " Vous devez sélectionner un dossier médical.")
        return dossier

    def clean_medecin(self):
        medecin = self.cleaned_data.get('medecin')
        if not medecin:
             self.add_error('medecin', " Vous devez sélectionner un médecin.")
        return medecin


# ===== Formulaire Medicament =====
class MedicamentForm(forms.ModelForm):
    nom_medicament = forms.CharField(
        max_length=100,
        required=True,
        label="Nom du médicament"
    )
    FORMES_MEDICAMENT = [
    ("Comprimé", "Comprimé"),
    ("Gélule", "Gélule"),
    ("Solution", "Solution"),
    ("Sirop", "Sirop"),
    ("Suspension", "Suspension"),
    ("Capsule", "Capsule"),
    ("Injection", "Injection"),
    ("Gel", "Gel"),
    ("Crème", "Crème"),
    ("Pommade", "Pommade"),
    ("Suppositoire", "Suppositoire"),
    ("Patch", "Patch"),
    ("Spray", "Spray"),
    ("Émulsion", "Émulsion"),
    ("Poudre", "Poudre")
]
    forme = forms.ChoiceField(
        choices=[('', '--- Sélectionnez un forme ---')] + FORMES_MEDICAMENT,
        widget=forms.Select(attrs={'class':'form-select'}),
        required=True,
        label="Forme"
    )


    class Meta:
      model = Medicament
      fields = ['nom_medicament', 'forme']
      widgets = {
        'forme': forms.Select(attrs={'class':'form-select'})
    }
# ===== Formulaire Prescription =====
class PrescriptionForm(forms.ModelForm):
    consultation = forms.ModelChoiceField(
        queryset=Consultation.objects.select_related('dossier__etudiant', 'medecin', 'rdv').order_by('rdv__date_rdv', 'rdv__heure'),
        required=True,
        label="Consultation",
        error_messages={'required': "Veuillez sélectionner une consultation."}
    )
    medicament = forms.ModelChoiceField(
        queryset=Medicament.objects.all(),
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Prescription
        fields = ['consultation', 'medicament', 'duree']
    def clean_consultation(self):
        consultation = self.cleaned_data.get("consultation")
        if not consultation:
            raise forms.ValidationError("Vous devez sélectionner une consultation avant de créer une prescription.")
        return consultation
#-------------- FORMULAIREDE VACCINATION------------------
class VaccinationForm(forms.ModelForm):
    nom_vaccin = forms.CharField(
        max_length=100,
        required=True,
        label="Nom du vaccin"
    )
    rappel = forms.CharField(
        max_length=50,
        required=False,
        label="Rappel (optionnel)"
    )
    dossier = forms.ModelChoiceField(
        queryset=DossierMedical.objects.all(),
        widget=forms.HiddenInput(),
        required=True,
        label="Dossier Médical",
        error_messages={'required': "Vous devez sélectionner un dossier médical."}
    )
    class Meta:
        model = Vaccination
        fields = ['nom_vaccin', 'rappel', 'dossier']

