from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from datetime import date, datetime, time
from django.utils import timezone


# ===== Etudiant =====
class Etudiant(models.Model):
    lettres_validator = RegexValidator(regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ ]+$',
        message='Ce champ ne peut contenir que des lettres et des espaces.')
    nom = models.CharField(max_length=50, validators=[lettres_validator])
    prenom = models.CharField(max_length=50, validators=[lettres_validator])
    CIN = models.CharField(max_length=10, unique=True)
    CNE = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField()
    FILIERES = [('API', 'API'),('GI', 'GI'),('GE', 'GE'), ('IID', 'IID'), ('IRIC', 'IRIC'),('MGSI', 'MGSI'),('GPEE', 'GPEE'),
    ('MASTER', 'MASTER'),]
    filiere = models.CharField(max_length=20, choices=FILIERES)
    NIVEAUX = [
        ('API1', 'API1'), ('API2', 'API2'),
        ('GI1', 'GI1'), ('GI2', 'GI2'), ('GI3', 'GI3'),
        ('GE1', 'GE1'), ('GE2', 'GE2'), ('GE3', 'GE3'),
        ('IID1', 'IID1'), ('IID2', 'IID2'), ('IID3', 'IID3'),
        ('MGSI1', 'MGSI1'), ('MGSI2', 'MGSI2'),
        ('IRIC1', 'IRIC1'), ('IRIC2', 'IRIC2'), ('IRIC3', 'IRIC3'),
        ('GPEE1', 'GPEE1'), ('GPEE2', 'GPEE2'), ('GPEE3', 'GPEE3'),
        ('M1', 'M1'), ('M2', 'M2'),]
    niveau = models.CharField(max_length=10, choices=NIVEAUX)
    sexe = models.CharField(max_length=1, choices=[('M','M'),('F','F')])
    telephone_regex = RegexValidator(
        regex=r'^(\\+212[ ]?[67]\d{8}|\\+33[ ]?6\d{8}|0[67]\d{8})$',
        message="Numéro de téléphone invalide")
    telephone = models.CharField(validators=[telephone_regex], max_length=20)
    VILLES_MAROC = [
    ('Agadir','Agadir'),
    ('Aïn Harrouda','Aïn Harrouda'),
    ('Al Hoceima','Al Hoceima'),
    ('Aït Melloul','Aït Melloul'),
    ('Asilah','Asilah'),
    ('Azrou','Azrou'),
    ('Beni Mellal','Beni Mellal'),
    ('Berrechid','Berrechid'),
    ('Benslimane','Benslimane'),
    ('Berkane','Berkane'),
    ('Boujdour','Boujdour'),
    ('Casablanca','Casablanca'),
    ('Chefchaouen','Chefchaouen'),
    ('Dakhla','Dakhla'),
    ('Dar Bouazza','Dar Bouazza'),
    ('El Jadida','El Jadida'),
    ('Errichidia','Errachidia'),
    ('Essaouira','Essaouira'),
    ('Fès','Fès'),
    ('Guercif','Guercif'),
    ('Guelmim','Guelmim'),
    ('Ifrane','Ifrane'),
    ('Kenitra','Kénitra'),
    ('Khouribga','Khouribga'),
    ('Khemisset','Khemisset'),
    ('Khenifra','Khenifra'),
    ('Ksar El Kebir','Ksar El Kebir'),
    ('Laâyoune','Laâyoune'),
    ('Larache','Larache'),
    ('Marrakech','Marrakech'),
    ('Martil','Martil'),
    ('Meknès','Meknès'),
    ('Mohammedia','Mohammedia'),
    ('Nador','Nador'),
    ('Ouarzazate','Ouarzazate'),
    ('Oujda','Oujda'),
    ('Rabat','Rabat'),
    ('Salé','Salé'),
    ('Safi','Safi'),
    ('Settat','Settat'),
    ('Sidi Slimane','Sidi Slimane'),
    ('Sidi Kacem','Sidi Kacem'),
    ('Tanger','Tanger'),
    ('Taza','Taza'),
    ('Temara','Témara'),
    ('Tétouan','Tétouan'),
    ('Tiznit','Tiznit'),
    ('Youssoufia','Youssoufia'),
    ('Tan-Tan','Tan-Tan'),
    ('Souk El Arbaa','Souk El Arbaa'),
    ('Oued Zem','Oued Zem'),
    ('Taourirt','Taourirt'),
    ('Oulad Teima','Oulad Teima'),
    ('Fquih Ben Salah','Fquih Ben Salah'),
    ('Skhirat','Skhirat'),
    ('Midelt','Midelt'),
]
    ville = models.CharField(max_length=50, choices=VILLES_MAROC)

    def __str__(self):
        return f"{self.nom} {self.prenom}"



# ===== Medecin =====
class Medecin(models.Model):
    lettres_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ ]+$',
        message='Ce champ ne peut contenir que des lettres et des espaces.'
    )
    nom = models.CharField(max_length=50, validators=[lettres_validator])
    prenom = models.CharField(max_length=50, validators=[lettres_validator])
    specialite = models.CharField(max_length=50,validators=[lettres_validator])
    telephone_regex = RegexValidator(
        regex=r'^(\\+212[ ]?[67]\d{8}|\\+33[ ]?6\d{8}|0[67]\d{8})$',
        message="Numéro de téléphone invalide"
    )
    telephone = models.CharField(validators=[telephone_regex], max_length=20)
    rdv_jr = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    salaire = models.DecimalField(
        max_digits=10,       # nombre max de chiffres total
        decimal_places=2,    # 2 chiffres après la virgule
        validators=[MinValueValidator(0.01)],  # > 0
        verbose_name="Salaire (DH)",default=0.00
    )


    def __str__(self):
        return f"{self.nom} {self.prenom}"
# ===== Dossier Medical =====
class DossierMedical(models.Model):
    etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE)  # UNIQUE + FK
    GROUPE_SANGUIN_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    groupe_sanguin = models.CharField(max_length=3,choices=GROUPE_SANGUIN_CHOICES)
    allergies = models.TextField(null=True, blank=True)
    maladies_chroniques = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    couverture_medicale = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"Dossier {self.etudiant.nom}"


# ===== RendezVous =====
class RendezVous(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date_rdv = models.DateField()
    heure = models.TimeField()
    statut = models.CharField(max_length=20, choices=[
        ('prévu','prévu'),
        ('effectué','effectué'),('raté','raté')
    ], default='prévu')

    def __str__(self):
          return f" {self.etudiant} avec {self.medecin} le {self.date_rdv} à {self.heure}"
    
    def update_statut_auto(self, save_model=False):
        today = date.today()

        # Futur
        if self.date_rdv > today:
            self.statut = "prévu"
        else:
            existe_consult = Consultation.objects.filter(rdv=self).exists()
            self.statut = "effectué" if existe_consult else "raté"

        if save_model:
            self.save()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['medecin', 'date_rdv', 'heure'],
                name='unique_medecin_rdv'
            ),
            models.UniqueConstraint(
                fields=['etudiant', 'date_rdv', 'heure'],
                name='unique_etudiant_rdv'
            )
        ]

# ===== Consultation =====
class Consultation(models.Model):
    dossier = models.ForeignKey(DossierMedical, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    rdv = models.OneToOneField(RendezVous, on_delete=models.RESTRICT)
    diagnostic = models.TextField(null=True, blank=True)

    def __str__(self):
        etu = f"{self.dossier.etudiant.nom} {self.dossier.etudiant.prenom}"
        med = f"Dr {self.medecin.nom} {self.medecin.prenom}"
        date = self.rdv.date_rdv.strftime("%Y-%m-%d")
        heure = self.rdv.heure.strftime("%H:%M")
        return f"{etu} avec {med} le {date} à {heure}"
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
# ===== Medicament =====
class Medicament(models.Model):
    nom_medicament = models.CharField(max_length=100)
    forme = models.CharField(
        max_length=50,
        choices=FORMES_MEDICAMENT,
        default='comprime',
        verbose_name="Forme")
    def __str__(self):
        return f"{self.nom_medicament} ({self.get_forme_display()})"
# ===== Prescription =====
class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.RESTRICT)
    duree = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f"{self.medicament.nom_medicament} pour {self.consultation}"
# ===== Vaccination =====
class Vaccination(models.Model):
    nom_vaccin = models.CharField(max_length=100)
    date_vaccin =  models.DateTimeField(auto_now_add=True)
    rappel = models.CharField(max_length=50, null=True, blank=True)
    dossier = models.ForeignKey(DossierMedical, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nom_vaccin} - {self.dossier}"

