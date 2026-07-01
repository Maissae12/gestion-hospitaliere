from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import (
    Etudiant, Medecin, DossierMedical,
    RendezVous, Consultation, Medicament,
    Prescription, Vaccination
)
from .serializers import (
    EtudiantSerializer, MedecinSerializer, DossierMedicalSerializer,
    RendezVousSerializer, ConsultationSerializer, MedicamentSerializer,
    PrescriptionSerializer, VaccinationSerializer
)
class EtudiantViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les étudiants.
    GET    /api/etudiants/          -> liste
    POST   /api/etudiants/          -> créer
    GET    /api/etudiants/{id}/     -> détail
    PUT    /api/etudiants/{id}/     -> modifier
    PATCH  /api/etudiants/{id}/     -> modifier partiellement
    DELETE /api/etudiants/{id}/     -> supprimer
    GET    /api/etudiants/search/?q=... -> recherche
    """
    serializer_class = EtudiantSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Etudiant.objects.all()
        q = self.request.query_params.get('q', '').strip()
        ville = self.request.query_params.get('ville', '').strip()
        filiere = self.request.query_params.get('filiere', '').strip()
        niveau = self.request.query_params.get('niveau', '').strip()
        sexe = self.request.query_params.get('sexe', '').strip()
        if q:
            qs = qs.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))
        if ville:
            qs = qs.filter(ville=ville)
        if filiere:
            qs = qs.filter(filiere=filiere)
        if niveau:
            qs = qs.filter(niveau=niveau)
        if sexe:
            qs = qs.filter(sexe=sexe)
        return qs
    def destroy(self, request, *args, **kwargs):
        etudiant = self.get_object()
        etudiant.delete()
        return Response(
            {'message': f"Étudiant {etudiant.nom} {etudiant.prenom} supprimé avec succès."},
            status=status.HTTP_200_OK
        )


class MedecinViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les médecins.
    GET    /api/medecins/        -> liste
    POST   /api/medecins/        -> créer
    GET    /api/medecins/{id}/   -> détail
    PUT    /api/medecins/{id}/   -> modifier
    PATCH  /api/medecins/{id}/   -> modifier partiellement
    DELETE /api/medecins/{id}/   -> supprimer
    """
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Medecin.objects.all()
        q = self.request.query_params.get('q', '').strip()
        specialite = self.request.query_params.get('specialite', '').strip()

        if q:
            qs = qs.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))
        if specialite:
            qs = qs.filter(specialite__icontains=specialite)
        return qs

    def destroy(self, request, *args, **kwargs):
        medecin = self.get_object()
        medecin.delete()
        return Response(
            {'message': f"Médecin Dr {medecin.nom} {medecin.prenom} supprimé avec succès."},
            status=status.HTTP_200_OK
        )


class DossierMedicalViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les dossiers médicaux.
    GET    /api/dossiers/        -> liste
    POST   /api/dossiers/        -> créer
    GET    /api/dossiers/{id}/   -> détail
    PUT    /api/dossiers/{id}/   -> modifier
    PATCH  /api/dossiers/{id}/   -> modifier partiellement
    DELETE /api/dossiers/{id}/   -> supprimer
    """
    serializer_class = DossierMedicalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = DossierMedical.objects.select_related('etudiant').all()
        q = self.request.query_params.get('q', '').strip()
        groupe = self.request.query_params.get('groupe_sanguin', '').strip()

        if q:
            qs = qs.filter(
                Q(etudiant__nom__icontains=q) | Q(etudiant__prenom__icontains=q)
            )
        if groupe:
            qs = qs.filter(groupe_sanguin=groupe)
        return qs

    def destroy(self, request, *args, **kwargs):
        dossier = self.get_object()
        nom = str(dossier)
        dossier.delete()
        return Response(
            {'message': f"{nom} supprimé avec succès."},
            status=status.HTTP_200_OK
        )


class RendezVousViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les rendez-vous.
    GET    /api/rendezvous/        -> liste
    POST   /api/rendezvous/        -> créer
    GET    /api/rendezvous/{id}/   -> détail
    PUT    /api/rendezvous/{id}/   -> modifier
    PATCH  /api/rendezvous/{id}/   -> modifier partiellement
    DELETE /api/rendezvous/{id}/   -> supprimer
    """
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = RendezVous.objects.select_related('etudiant', 'medecin').all()
        q = self.request.query_params.get('q', '').strip()
        statut = self.request.query_params.get('statut', '').strip()
        date_rdv = self.request.query_params.get('date_rdv', '').strip()

        if q:
            qs = qs.filter(
                Q(etudiant__nom__icontains=q) | Q(etudiant__prenom__icontains=q) |
                Q(medecin__nom__icontains=q) | Q(medecin__prenom__icontains=q)
            )
        if statut:
            qs = qs.filter(statut=statut)
        if date_rdv:
            qs = qs.filter(date_rdv=date_rdv)
        return qs.order_by('-date_rdv', '-heure')

    def destroy(self, request, *args, **kwargs):
        rdv = self.get_object()
        rdv.delete()
        return Response(
            {'message': "Rendez-vous supprimé avec succès."},
            status=status.HTTP_200_OK
        )


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les consultations.
    GET    /api/consultations/        -> liste
    POST   /api/consultations/        -> créer
    GET    /api/consultations/{id}/   -> détail
    PUT    /api/consultations/{id}/   -> modifier
    PATCH  /api/consultations/{id}/   -> modifier partiellement
    DELETE /api/consultations/{id}/   -> supprimer
    """
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Consultation.objects.select_related(
            'dossier__etudiant', 'medecin', 'rdv'
        ).all()
        q = self.request.query_params.get('q', '').strip()

        if q:
            qs = qs.filter(
                Q(dossier__etudiant__nom__icontains=q) |
                Q(dossier__etudiant__prenom__icontains=q) |
                Q(medecin__nom__icontains=q) |
                Q(medecin__prenom__icontains=q)
            )
        return qs

    def destroy(self, request, *args, **kwargs):
        consultation = self.get_object()
        consultation.delete()
        return Response(
            {'message': "Consultation supprimée avec succès."},
            status=status.HTTP_200_OK
        )


class MedicamentViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les médicaments.
    GET    /api/medicaments/        -> liste
    POST   /api/medicaments/        -> créer
    GET    /api/medicaments/{id}/   -> détail
    PUT    /api/medicaments/{id}/   -> modifier
    PATCH  /api/medicaments/{id}/   -> modifier partiellement
    DELETE /api/medicaments/{id}/   -> supprimer
    """
    serializer_class = MedicamentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Medicament.objects.all()
        q = self.request.query_params.get('q', '').strip()
        forme = self.request.query_params.get('forme', '').strip()

        if q:
            qs = qs.filter(nom_medicament__icontains=q)
        if forme:
            qs = qs.filter(forme__icontains=forme)
        return qs

    def destroy(self, request, *args, **kwargs):
        medicament = self.get_object()
        from .models import Prescription
        if Prescription.objects.filter(medicament=medicament).exists():
            return Response(
                {'error': "Ce médicament est utilisé dans une prescription et ne peut pas être supprimé."},
                status=status.HTTP_400_BAD_REQUEST
            )
        medicament.delete()
        return Response(
            {'message': f"Médicament {medicament.nom_medicament} supprimé avec succès."},
            status=status.HTTP_200_OK
        )


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les prescriptions.
    GET    /api/prescriptions/        -> liste
    POST   /api/prescriptions/        -> créer
    GET    /api/prescriptions/{id}/   -> détail
    PUT    /api/prescriptions/{id}/   -> modifier
    PATCH  /api/prescriptions/{id}/   -> modifier partiellement
    DELETE /api/prescriptions/{id}/   -> supprimer
    """
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Prescription.objects.select_related(
            'consultation__dossier__etudiant',
            'consultation__medecin',
            'medicament'
        ).all()
        q = self.request.query_params.get('q', '').strip()

        if q:
            qs = qs.filter(
                Q(medicament__nom_medicament__icontains=q) |
                Q(consultation__dossier__etudiant__nom__icontains=q) |
                Q(consultation__dossier__etudiant__prenom__icontains=q)
            )
        return qs

    def destroy(self, request, *args, **kwargs):
        prescription = self.get_object()
        prescription.delete()
        return Response(
            {'message': "Prescription supprimée avec succès."},
            status=status.HTTP_200_OK
        )


class VaccinationViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les vaccinations.
    GET    /api/vaccinations/        -> liste
    POST   /api/vaccinations/        -> créer
    GET    /api/vaccinations/{id}/   -> détail
    PUT    /api/vaccinations/{id}/   -> modifier
    PATCH  /api/vaccinations/{id}/   -> modifier partiellement
    DELETE /api/vaccinations/{id}/   -> supprimer
    """
    serializer_class = VaccinationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Vaccination.objects.select_related('dossier__etudiant').all()
        q = self.request.query_params.get('q', '').strip()

        if q:
            qs = qs.filter(
                Q(nom_vaccin__icontains=q) |
                Q(dossier__etudiant__nom__icontains=q) |
                Q(dossier__etudiant__prenom__icontains=q)
            )
        return qs

    def destroy(self, request, *args, **kwargs):
        vaccination = self.get_object()
        vaccination.delete()
        return Response(
            {'message': "Vaccination supprimée avec succès."},
            status=status.HTTP_200_OK
        )
