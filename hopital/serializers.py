from rest_framework import serializers
from .models import (
    Etudiant, Medecin, DossierMedical,
    RendezVous, Consultation, Medicament,
    Prescription, Vaccination
)


# ===== Etudiant =====
class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'

    def validate_CIN(self, value):
        instance = self.instance
        qs = Etudiant.objects.filter(CIN=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Un étudiant avec ce CIN existe déjà.")
        return value

    def validate_CNE(self, value):
        instance = self.instance
        qs = Etudiant.objects.filter(CNE=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Un étudiant avec ce CNE existe déjà.")
        return value


# ===== Medecin =====
class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = '__all__'

    def validate_salaire(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le salaire doit être supérieur à 0.")
        return value

    def validate_rdv_jr(self, value):
        if value < 0:
            raise serializers.ValidationError("Le nombre de RDV/jour ne peut pas être négatif.")
        return value


# ===== DossierMedical =====
class DossierMedicalSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DossierMedical
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return f"{obj.etudiant.nom} {obj.etudiant.prenom}"

    def validate_etudiant(self, value):
        instance = self.instance
        qs = DossierMedical.objects.filter(etudiant=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Cet étudiant possède déjà un dossier médical.")
        return value


# ===== RendezVous =====
class RendezVousSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField(read_only=True)
    medecin_nom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RendezVous
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return f"{obj.etudiant.nom} {obj.etudiant.prenom}"

    def get_medecin_nom(self, obj):
        return f"Dr {obj.medecin.nom} {obj.medecin.prenom}"

    def validate(self, data):
        medecin = data.get('medecin', getattr(self.instance, 'medecin', None))
        date_rdv = data.get('date_rdv', getattr(self.instance, 'date_rdv', None))
        heure = data.get('heure', getattr(self.instance, 'heure', None))
        etudiant = data.get('etudiant', getattr(self.instance, 'etudiant', None))

        # Vérifier unicité médecin/date/heure
        qs_medecin = RendezVous.objects.filter(medecin=medecin, date_rdv=date_rdv, heure=heure)
        if self.instance:
            qs_medecin = qs_medecin.exclude(pk=self.instance.pk)
        if qs_medecin.exists():
            raise serializers.ValidationError(
                "Ce médecin a déjà un rendez-vous à cette date et cette heure."
            )

        # Vérifier unicité étudiant/date/heure
        qs_etudiant = RendezVous.objects.filter(etudiant=etudiant, date_rdv=date_rdv, heure=heure)
        if self.instance:
            qs_etudiant = qs_etudiant.exclude(pk=self.instance.pk)
        if qs_etudiant.exists():
            raise serializers.ValidationError(
                "Cet étudiant a déjà un rendez-vous à cette date et cette heure."
            )
        return data


# ===== Consultation =====
class ConsultationSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField(read_only=True)
    medecin_nom = serializers.SerializerMethodField(read_only=True)
    date_rdv = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return f"{obj.dossier.etudiant.nom} {obj.dossier.etudiant.prenom}"

    def get_medecin_nom(self, obj):
        return f"Dr {obj.medecin.nom} {obj.medecin.prenom}"

    def get_date_rdv(self, obj):
        if obj.rdv:
            return obj.rdv.date_rdv
        return None


# ===== Medicament =====
class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = '__all__'

    def validate_nom_medicament(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le nom du médicament doit contenir au moins 2 caractères."
            )
        return value


# ===== Prescription =====
class PrescriptionSerializer(serializers.ModelSerializer):
    medicament_nom = serializers.SerializerMethodField(read_only=True)
    etudiant_nom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'

    def get_medicament_nom(self, obj):
        return obj.medicament.nom_medicament

    def get_etudiant_nom(self, obj):
        etu = obj.consultation.dossier.etudiant
        return f"{etu.nom} {etu.prenom}"


# ===== Vaccination =====
class VaccinationSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vaccination
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return f"{obj.dossier.etudiant.nom} {obj.dossier.etudiant.prenom}"
