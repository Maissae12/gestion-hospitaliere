from rest_framework.routers import DefaultRouter
from .api_views import (
    EtudiantViewSet, MedecinViewSet, DossierMedicalViewSet,
    RendezVousViewSet, ConsultationViewSet, MedicamentViewSet,
    PrescriptionViewSet, VaccinationViewSet)
router = DefaultRouter()
router.register(r'etudiants',    EtudiantViewSet,       basename='api-etudiant')
router.register(r'medecins',     MedecinViewSet,        basename='api-medecin')
router.register(r'dossiers',     DossierMedicalViewSet, basename='api-dossier')
router.register(r'rendezvous',   RendezVousViewSet,     basename='api-rdv')
router.register(r'consultations',ConsultationViewSet,   basename='api-consultation')
router.register(r'medicaments',  MedicamentViewSet,     basename='api-medicament')
router.register(r'prescriptions',PrescriptionViewSet,   basename='api-prescription')
router.register(r'vaccinations', VaccinationViewSet,    basename='api-vaccination')

urlpatterns = router.urls
