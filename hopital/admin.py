from django.contrib import admin
from .models import Etudiant, DossierMedical, Medecin, RendezVous, Consultation, Medicament, Prescription

admin.site.register(Etudiant)
admin.site.register(DossierMedical)
admin.site.register(Medecin)
admin.site.register(RendezVous)
admin.site.register(Consultation)
admin.site.register(Medicament)
admin.site.register(Prescription)

