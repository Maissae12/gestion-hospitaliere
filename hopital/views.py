from django.shortcuts import render, redirect, get_object_or_404
from .models import (Etudiant, DossierMedical, Medecin, RendezVous, Consultation,Medicament, Prescription, Vaccination)
from django.utils.timezone import datetime
from .forms import (EtudiantForm, DossierMedicalForm, MedecinForm, RendezVousForm,ConsultationForm, MedicamentForm, PrescriptionForm, VaccinationForm)
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from datetime import date, timedelta,time
from django.utils import timezone
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import ConnexionForm
from django.db.models import Count


from datetime import datetime ,date 
import datetime
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')

def home_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'hopital/home_dashboard.html')

def agent_tables(request):
    # Vérifie que l'utilisateur est agent
    
    # Passe toutes les tables nécessaires pour l'agent
    context = {
        'etudiants': Etudiant.objects.all(),
        'medecins': Medecin.objects.all(),
        'dossiers': DossierMedical.objects.all(),
        'rdvs': RendezVous.objects.all(),
        'vaccinations': Vaccination.objects.all(),
    }
    return render(request, 'hopital/agent_tables.html', context)
def agent_dashboard(request):
    return render(request, 'agent_dashboard.html', {
        'etudiants': Etudiant.objects.all(),
        'medecins': Medecin.objects.all(),
        'dossiers': DossierMedical.objects.all(),
        'rdvs': RendezVous.objects.select_related('etudiant','medecin').order_by('-date_rdv'),
        'vaccinations': Vaccination.objects.all(),
    })
def medecin_dashboard(request):
    medecin = request.user.medecin  # adapte selon ton modèle
    return render(request, 'medecin_dashboard.html', {
        'dossiers': DossierMedical.objects.filter(medecin=medecin),
        'consultations': Consultation.objects.filter(
            dossier__medecin=medecin
        ).order_by('-date_consultation'),
        'prescriptions': Prescription.objects.filter(
            consultation__dossier__medecin=medecin
        ).order_by('-consultation__date_consultation'),
    })
def medecin_tables(request):
    # Vérifie que l'utilisateur est médecin
   
    # Passe toutes les tables nécessaires pour le médecin
    context = {
       
        'dossiers': DossierMedical.objects.all(),
        'consultations': Consultation.objects.all(),
        'medicaments': Medicament.objects.all(),
        'prescriptions': Prescription.objects.all(),
        'vaccinations': Vaccination.objects.all(),
    }
    return render(request, 'hopital/medecin_tables.html', context)





def user_login(request):
    form = ConnexionForm(request, data=request.POST or None)
    error = None
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_dashboard')
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect"
    return render(request, 'hopital/login.html', {'form': form, 'error': error})

@login_required(login_url='login') 
def dashboard(request):
    return render(request, 'hopital/dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def autocomplete_etudiant(request):
    term = request.GET.get('term', '')
    if term:
        qs = Etudiant.objects.filter(Q(nom__istartswith=term) | Q(prenom__istartswith=term))
    else:
        qs = Etudiant.objects.all()  # afficher tous les étudiants au clic
    results = []
    for e in qs:
        results.append({
            'id': e.id,
            'label': f"{e.nom} {e.prenom}"})
    return JsonResponse(results, safe=False)

def autocomplete_medecin(request):
    term = request.GET.get('term', '') 
    if term:
        # filtrage dynamique : nom ou prénom commence par ce qui est tapé
        qs = Medecin.objects.filter(Q(nom__istartswith=term) | Q(prenom__istartswith=term))
    else:
        qs = Medecin.objects.all()  # afficher tous les médecins au clic

    results = []
    for m in qs:
        results.append({
            'id': m.id,
            'label': f"{m.nom} {m.prenom}"
        })

    return JsonResponse(results, safe=False)

def dashboard(request):
    context = {
        'etudiants': Etudiant.objects.all(),
        'medecins': Medecin.objects.all(),
        'dossiers': DossierMedical.objects.all(),
        'rdvs': RendezVous.objects.all(),
        'consultations': Consultation.objects.all(),
        'medicaments': Medicament.objects.all(),
        'prescriptions': Prescription.objects.all(),
        'vaccinations': Vaccination.objects.all(),
    }
    return render(request, 'hopital/dashboard.html', context)
# ====== ETUDIANT ======
def etudiant_detail(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, pk=etudiant_id)
    return render(request, 'hopital/etudiant_detail.html', {'etudiant': etudiant})

# ====== ETUDIANT ======
def etudiant_list(request):
    nom_query = request.GET.get("nom")
    prenom_query = request.GET.get("prenom")
    search = request.GET.get('search', '')
    ville = request.GET.get('ville', '')
    niveau = request.GET.get('niveau', '')
    filiere = request.GET.get('filiere', '')
    sexe = request.GET.get('sexe', '') 
    qs = Etudiant.objects.all()
    id_qs = request.GET.get('id', '').strip()
    if id_qs:
        qs = qs.filter(id=id_qs)
    # Filtrer par nom
    if nom_query:
        qs = qs.filter(nom__icontains=nom_query)
    # Filtrer par prénom
    if prenom_query:
       qs = qs.filter(prenom__icontains=prenom_query)
    if search:
        qs = qs.filter(Q(nom__icontains=search) | Q(prenom__icontains=search))
    if ville:
        qs = qs.filter(ville=ville)
    if niveau:
        qs = qs.filter(niveau=niveau)
    if filiere:
        qs = qs.filter(filiere=filiere)
    if sexe:
        qs = qs.filter(sexe=sexe) 

    # Générer les options pour les filtres
    villes = Etudiant.objects.values_list('ville', flat=True).distinct().order_by('ville')
    niveaux = Etudiant.objects.values_list('niveau', flat=True).distinct().order_by('niveau')
    filieres = Etudiant.objects.values_list('filiere', flat=True).distinct().order_by('filiere')
    sexes = ['M', 'F'] 
    return render(request, 'hopital/etudiant_list.html', {
        'etudiants': qs,
        "nom_query": nom_query,
        "prenom_query": prenom_query,
        'villes': villes,
        'niveaux': niveaux,
        'filieres': filieres,
        'sexes': sexes,
    })

def etudiant_create(request):
    form = EtudiantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('etudiant_list')
    return render(request, 'hopital/etudiant_form.html', {'form': form})

def etudiant_update(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    form = EtudiantForm(request.POST or None, instance=etudiant)
    if form.is_valid():
        form.save()
        return redirect('etudiant_list')
    return render(request, 'hopital/etudiant_form.html', {'form': form})

def etudiant_delete(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        etudiant.delete()
        return redirect('etudiant_list')
    return render(request, 'hopital/etudiant_confirm_delete.html', {'etudiant': etudiant})

# ====== DOSSIER MEDICAL ======

def dossier_detail(request, pk):
    dossier = get_object_or_404(DossierMedical, pk=pk)

    # Récupérer toutes les consultations liées au dossier
    consultations = Consultation.objects.filter(dossier=dossier).select_related('medecin', 'rdv')

    # Récupérer toutes les prescriptions liées aux consultations
    prescriptions = Prescription.objects.filter(consultation__dossier=dossier).select_related('consultation', 'medicament')

    # Récupérer toutes les vaccinations liées à ce dossier
    vaccinations = Vaccination.objects.filter(dossier=dossier)

    context = {
        'dossier': dossier,
        'consultations': consultations,
        'prescriptions': prescriptions,
        'vaccinations': vaccinations,
    }

    return render(request, 'hopital/dossier_detail.html', context)

def dossier_detailmedecin(request, pk):
    dossier = get_object_or_404(DossierMedical, pk=pk)

    # Récupérer toutes les consultations liées au dossier
    consultations = Consultation.objects.filter(dossier=dossier).select_related('medecin', 'rdv')

    # Récupérer toutes les prescriptions liées aux consultations
    prescriptions = Prescription.objects.filter(consultation__dossier=dossier).select_related('consultation', 'medicament')

    # Récupérer toutes les vaccinations liées à ce dossier
    vaccinations = Vaccination.objects.filter(dossier=dossier)

    context = {
        'dossier': dossier,
        'consultations': consultations,
        'prescriptions': prescriptions,
        'vaccinations': vaccinations,
    }

    return render(request, 'hopital/dossier_detailmedecin.html', context)



def dossier_list(request):
    etudiant_query = request.GET.get('etudiant', '').strip()
    groupe_filter = request.GET.get('groupe_sanguin', '')
    couverture_filter = request.GET.get('couverture', '')

    qs = DossierMedical.objects.select_related('etudiant').all()
    id_qs = request.GET.get('id', '').strip()
    
    if id_qs:
        qs= qs.filter(id=id_qs)
    # Appliquer les filtres si ils existent
    if etudiant_query:
        qs = qs.filter(
            Q(etudiant__nom__icontains=etudiant_query) |
            Q(etudiant__prenom__icontains=etudiant_query))
    if groupe_filter:
        qs = qs.filter(groupe_sanguin=groupe_filter)
    if couverture_filter:
        qs = qs.filter(couverture_medicale__icontains=couverture_filter)

    # Options pour les filtres
    groupes = [g[0] for g in DossierMedical.GROUPE_SANGUIN_CHOICES]
    couvertures = DossierMedical.objects.values_list('couverture_medicale', flat=True).distinct()
    etudiants = Etudiant.objects.all()

    return render(request, 'hopital/dossier_list.html', {
        'dossiers': qs,
        'groupes': groupes,
        'couvertures': couvertures,
        'etudiants': etudiants,
    })
    
    
def dossier_listmedecin(request):
    etudiant_query = request.GET.get('etudiant', '').strip()
    groupe_filter = request.GET.get('groupe_sanguin', '')
    couverture_filter = request.GET.get('couverture', '')

    qs = DossierMedical.objects.select_related('etudiant').all()
    id_qs = request.GET.get('id', '').strip()
    
    if id_qs:
        qs= qs.filter(id=id_qs)
    # Appliquer les filtres si ils existent
    if etudiant_query:
        qs = qs.filter(
            Q(etudiant__nom__icontains=etudiant_query) |
            Q(etudiant__prenom__icontains=etudiant_query))
    if groupe_filter:
        qs = qs.filter(groupe_sanguin=groupe_filter)
    if couverture_filter:
        qs = qs.filter(couverture_medicale__icontains=couverture_filter)

    # Options pour les filtres
    groupes = [g[0] for g in DossierMedical.GROUPE_SANGUIN_CHOICES]
    couvertures = DossierMedical.objects.values_list('couverture_medicale', flat=True).distinct()
    etudiants = Etudiant.objects.all()

    return render(request, 'hopital/dossier_listmedecin.html', {
        'dossiers': qs,
        'groupes': groupes,
        'couvertures': couvertures,
        'etudiants': etudiants,
    })

#  Création d'un dossier médical
def dossier_create(request):
    if request.method == "POST":
        data = request.POST.copy()

        if "etudiant_id" in data:
            data["etudiant"] = data["etudiant_id"]

        form = DossierMedicalForm(data)
        if form.is_valid():
            form.save()
            return redirect('dossier_list')

    else:
        form = DossierMedicalForm()

    return render(request, 'hopital/dossier_form.html', {'form': form, "edit": False})
    
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
#  Modification d'un dossier
def dossier_update(request, pk):
    dossier = get_object_or_404(DossierMedical, pk=pk)

    #  Pré-remplissage couverture médicale
    initial = {}
    couverture_values = dict(COUVERTURE_CHOICES)

    if dossier.couverture_medicale in couverture_values:
        initial['couverture_medicale_select'] = dossier.couverture_medicale
    else:
        initial['couverture_medicale_select'] = 'Autre'
        initial['couverture_medicale_autre'] = dossier.couverture_medicale

    if request.method == "POST":
        data = request.POST.copy()

        #  récupérer id étudiant caché
        if "etudiant_id" in data:
            data["etudiant"] = data["etudiant_id"]

        form = DossierMedicalForm(data, instance=dossier)
        if form.is_valid():
            form.save()
            return redirect('dossier_list')

    else:
        form = DossierMedicalForm(instance=dossier, initial=initial)

    return render(request, 'hopital/dossier_form.html', {
        "form": form,
        "dossier": dossier,
        "edit": True
    })


#  Suppression
def dossier_delete(request, pk):
    dossier = get_object_or_404(DossierMedical, pk=pk)
    if request.method == 'POST':
        dossier.delete()
        return redirect('dossier_list')
    return render(request, 'hopital/dossier_confirm_delete.html', {'dossier': dossier})

# ====== MEDECIN ======
def medecin_detail(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    return render(request, 'hopital/medecin_detail.html', {'medecin': medecin})
def medecin_list(request):
    medecins = Medecin.objects.all()
    nom_query = request.GET.get("nom")
    prenom_query = request.GET.get("prenom")
    id_medecins = request.GET.get('id', '').strip()
    
    if id_medecins:
        medecins = medecins.filter(id=id_medecins)
    # Filtrer par nom
    if nom_query:
        medecins = medecins.filter(nom__icontains=nom_query)

    # Filtrer par prénom
    if prenom_query:
        medecins = medecins.filter(prenom__icontains=prenom_query)
    # Récupérer les filtres depuis la requête GET
    rdv_jr = request.GET.get('rdv_jr', '')
    specialite = request.GET.get('specialite', '').strip()
    salaire = request.GET.get('salaire', '').strip()
    if specialite:
       medecins = medecins.filter(specialite__icontains=specialite)
   
    if salaire:
        salaire = salaire.replace(',', '.')
        medecins = medecins.filter(salaire__icontains=salaire)

    
    if rdv_jr:
        try:
            medecins = medecins.filter(rdv_jr=int(rdv_jr))
        except ValueError:
            pass

    # Récupérer toutes les spécialités uniques pour le select
    specialites = Medecin.objects.values_list('specialite', flat=True).distinct().order_by('specialite')

    # Récupérer tous les salaires existants pour le select
    salaires = Medecin.objects.values_list('salaire', flat=True).distinct().order_by('salaire')

    # Récupérer tous les RDV/jour existants pour le select
    rdvs = Medecin.objects.values_list('rdv_jr', flat=True).distinct().order_by('rdv_jr')

    return render(request, 'hopital/medecin_list.html', {
        'medecins': medecins,
        "nom_query": nom_query,
        "prenom_query": prenom_query,
        'specialites': specialites,
        'salaires': salaires,
        'rdvs': rdvs,
        'filters': {
            'specialite': specialite,
            'salaire': salaire,
            'rdv_jr': rdv_jr,
        }
    })

def medecin_create(request):
    form = MedecinForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('medecin_list')
    return render(request, 'hopital/medecin_form.html', {'form': form})

def medecin_update(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    form = MedecinForm(request.POST or None, instance=medecin)
    if form.is_valid():
        form.save()
        return redirect('medecin_list')
    return render(request, 'hopital/medecin_form.html', {'form': form})

def medecin_delete(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    if request.method == 'POST':
        medecin.delete()
        return redirect('medecin_list')
    return render(request, 'hopital/medecin_confirm_delete.html', {'medecin': medecin})

# ====== RENDEZ-VOUS ======
def rdv_detail(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    return render(request, 'hopital/rdv_detail.html', {'rdv': rdv})
HEURE_CHOICES = [(h, h) for h in [
    "09:00","09:30","10:00","10:30","11:00","11:30","12:00",
    "14:00","14:30","15:00","15:30","16:00","16:30","17:00"
]]

def rdv_list(request):
    # Récupérer les filtres depuis GET
    etudiant_query = request.GET.get('etudiant', '').strip()
    medecin_query = request.GET.get('medecin', '').strip()
    date_filter = request.GET.get('date_rdv', '').strip()
    statut_filter = request.GET.get('statut', '').strip()
    heure_filter = request.GET.get('heure', '').strip()
    
    # Récupérer tous les RDV
    rdvs = RendezVous.objects.select_related('etudiant', 'medecin').all()

    # Filtrer par étudiant (nom ou prénom)
    if etudiant_query:
        rdvs = rdvs.filter(
            Q(etudiant__nom__icontains=etudiant_query) |
            Q(etudiant__prenom__icontains=etudiant_query))

    # Filtrer par médecin (nom ou prénom)
    if medecin_query:
        rdvs = rdvs.filter(
            Q(medecin__nom__icontains=medecin_query) |
            Q(medecin__prenom__icontains=medecin_query))

    # Filtrer par date
    if date_filter:
        rdvs = rdvs.filter(date_rdv=date_filter)
    # Filtrer par statut
    if statut_filter:
        rdvs = rdvs.filter(statut=statut_filter)
    # Filtrer par heure
    if heure_filter:
        rdvs = rdvs.filter(heure=heure_filter)
    # Tri par date puis heure
    rdvs = rdvs.order_by('-date_rdv', '-heure')
    # Mise à jour automatique des statuts pour tous les RDV
    for rdv in rdvs:
        rdv.update_statut_auto(save_model=True)

    etudiants = Etudiant.objects.all()
    medecins = Medecin.objects.all()
    statuts = ['prévu' ,'effectué', 'raté']

    return render(request, "hopital/rdv_list.html", {
        "rdvs": rdvs,
        "etudiants": etudiants,
        "medecins": medecins,
        "statuts": statuts,
        "etudiant_query": etudiant_query,
        "medecin_query": medecin_query,
        "date_filter": date_filter,
        "statut_filter": statut_filter,
        'heure_choices': HEURE_CHOICES,
    })
def rdv_create(request):
    if request.method == "POST":
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save()
            return redirect('rdv_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RendezVousForm()
    return render(request, 'hopital/rdv_form.html', {'form': form})


def rdv_update(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    form = RendezVousForm(request.POST or None, instance=rdv)
    if form.is_valid():
        form.save()
        return redirect('rdv_list')
    return render(request, 'hopital/rdv_form.html', {'form': form, 'rdv_instance': rdv  })


def rdv_delete(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)

    if request.method == "POST":
        rdv.delete()
        return redirect('rdv_list')

    return render(request, 'hopital/rdv_confirm_delete.html', {
        'rdv': rdv
    })
# ====== CONSULTATION ======
def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'hopital/consultation_detail.html', {'consultation': consultation})
def agent_consultation_stats(request):
    # Statistiques par filière
    stats_filiere = Consultation.objects.values(
        'dossier__etudiant__filiere'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    # Statistiques par niveau
    stats_niveau = Consultation.objects.values(
        'dossier__etudiant__niveau'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    context = {
        'stats_filiere': stats_filiere,
        'stats_niveau': stats_niveau,
    }
    return render(request, 'hopital/agent_consultation_stats.html', context)
def consultation_list(request):
    etudiant_query = request.GET.get('etudiant', '').strip()
    medecin_query = request.GET.get('medecin', '').strip()
    date_query = request.GET.get('date_rdv', '').strip()    
    heure_filter = request.GET.get('heure', '').strip()
    id_consultations= request.GET.get('id', '').strip()
    # ====== STATISTIQUES ======
    consultations = Consultation.objects.select_related(
        'dossier__etudiant', 'medecin', 'rdv'
    ).order_by('rdv__date_rdv', 'rdv__heure')  
    if id_consultations:
        consultations = consultations.filter(id=id_consultations)
    # Filtrer par étudiant (nom ou prénom)
    if etudiant_query:
        consultations = consultations.filter(
            Q(dossier__etudiant__nom__icontains=etudiant_query) |
            Q(dossier__etudiant__prenom__icontains=etudiant_query)
        )

    # Filtrer par médecin (nom ou prénom)
    if medecin_query:
        consultations = consultations.filter(
            Q(medecin__nom__icontains=medecin_query) |
            Q(medecin__prenom__icontains=medecin_query)
        )
    # Filtrer par date du rendez-vous
    if date_query:
        consultations = consultations.filter(rdv__date_rdv__icontains=date_query)
    
    if heure_filter:
        consultations = consultations.filter(rdv__heure=heure_filter)

    context = {
        'consultations': consultations,
        'request': request, 
         'heure_choices': HEURE_CHOICES,
    }
    

    return render(request, 'hopital/consultation_list.html', context)

def autocomplete_rdv(request):
    term = request.GET.get('term', '').strip()
    today = datetime.date.today()    
    rdvs = RendezVous.objects.filter(date_rdv__lte=today, consultation__isnull=True)
    if term:
        rdvs = rdvs.filter(
            Q(etudiant__nom__icontains=term) |
            Q(etudiant__prenom__icontains=term) |
            Q(medecin__nom__icontains=term) |
            Q(medecin__prenom__icontains=term) |
            Q(date_rdv__icontains=term)
        )

    results = []

    for r in rdvs:
        results.append({
            "id": r.id,
            "label": f"RDV {r.date_rdv} à {r.heure} — {r.etudiant.nom} {r.etudiant.prenom} avec Dr {r.medecin.nom}"
        })

    return JsonResponse(results, safe=False)
# Création d'une consultation

def consultation_create(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)

        if form.is_valid():
            # Vérifier la date et l'heure du RDV associé
            rdv = form.cleaned_data['rdv']
            now = datetime.datetime.now()  
            rdv_datetime = datetime.datetime.combine(rdv.date_rdv, rdv.heure)
            if rdv_datetime > now:
                messages.error(request, "Impossible de créer une consultation pour un rendez-vous futur !")
            else:
                form.save()
                return redirect('consultation_list')
        else:
            print("ERREURS FORM :", form.errors)
    else:
        form = ConsultationForm()
    
    return render(request, 'hopital/consultation_form.html', {'form': form, 'consultation': None})

# Modification d'une consultation

def consultation_update(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            return redirect('consultation_list')
    else:
        form = ConsultationForm(instance=consultation)

    return render(request, 'hopital/consultation_form.html', {'form': form, 'consultation': consultation})

# Suppression d'une consultation
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        consultation.delete()
        return redirect('consultation_list')
    return render(request, 'hopital/consultation_confirm_delete.html', {'consultation': consultation})

# Autocomplete Dossier
def autocomplete_dossier(request):
    term = request.GET.get('term', '').strip()

    if term.isdigit():
        dossiers = DossierMedical.objects.filter(id=int(term))[:10]
    else:
        dossiers = DossierMedical.objects.filter(
            Q(etudiant__nom__icontains=term) | Q(etudiant__prenom__icontains=term)
        )[:10]

    results = [
        {
            'id': d.id,
            'label': f"[ID: {d.id}] {d.etudiant.nom} {d.etudiant.prenom}"  # affiche ID + Nom Prénom
        }
        for d in dossiers
    ]
    return JsonResponse(results, safe=False)

#pour dans dossier médicale dans create 
def autocomplete_etudiant_dossier(request):
    term = request.GET.get("term", "")
    etudiants = Etudiant.objects.exclude(
        id__in=DossierMedical.objects.values('etudiant')
    ).filter(
        Q(nom__icontains=term) | Q(prenom__icontains=term)
    )

    results = []
    for e in etudiants:
        results.append({
            "id": e.id,
            "label": f"{e.nom} {e.prenom}",
            "value": f"{e.nom} {e.prenom}",
        })
    return JsonResponse(results, safe=False)

# ====== MEDICAMENT ======
def medicament_list(request):
    # Récupération des filtres GET
    id_m = request.GET.get('id', '').strip()
    nom_m = request.GET.get('nom', '').strip()
    forme = request.GET.get('forme', '').strip()

    # Toujours initialiser queryset AVANT filtrage
    medicaments = Medicament.objects.all()

    # Filtrage
    if id_m:
        medicaments = medicaments.filter(id=id_m)

    if nom_m:
        medicaments = medicaments.filter(nom_medicament__icontains=nom_m)

    if forme:
        medicaments = medicaments.filter(forme__icontains=forme)
    formes = Medicament.objects.values_list('forme', flat=True).distinct()

    return render(request, 'hopital/medicament_list.html', {
        'medicaments': medicaments,
        'formes': formes,
    })
    
    
    
def medicament_create(request):
    form = MedicamentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('medicament_list')
    return render(request, 'hopital/medicament_form.html', {'form': form})

def medicament_update(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    form = MedicamentForm(request.POST or None, instance=medicament)
    if form.is_valid():
        form.save()
        return redirect('medicament_list')
    return render(request, 'hopital/medicament_form.html', {'form': form})

def medicament_delete(request, pk):
    # Récupérer le médicament
    medicament = get_object_or_404(Medicament, pk=pk)

    # Vérifier s'il est utilisé dans une prescription
    is_used = Prescription.objects.filter(medicament=medicament).exists()

    # Si formulaire soumis et pas utilisé → supprimer
    if request.method == "POST":
        if not is_used:
            medicament.delete()
            return redirect('medicament_list')
        # Si utilisé, on ne supprime pas et on reste sur la page

    # Toujours envoyer is_used au template
    return render(request, 'hopital/medicament_confirm_delete.html', {
        'medicament': medicament,
        'is_used': is_used
    })
# ====== PRESCRIPTION ======
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'hopital/prescription_detail.html', {'prescription': prescription})
def autocomplete_consultation(request):
    term = request.GET.get('term', '').strip()
    
    # On récupère toutes les consultations avec leurs relations pour éviter les requêtes supplémentaires
    consultations = Consultation.objects.select_related(
    'dossier__etudiant', 'medecin', 'rdv'
).filter(rdv__isnull=False)
    if term:
        consultations = consultations.filter(
            Q(dossier__etudiant__nom__icontains=term) |
            Q(dossier__etudiant__prenom__icontains=term) |
            Q(medecin__nom__icontains=term) |
            Q(medecin__prenom__icontains=term) |
            Q(rdv__date_rdv__icontains=term)
        )

    results = []
    for c in consultations:
        results.append({
            'id': c.id,
            'label': f"{c.dossier.etudiant.nom} {c.dossier.etudiant.prenom} "
                     f"avec Dr {c.medecin.nom} {c.medecin.prenom} "
                     f"le {c.rdv.date_rdv.strftime('%Y-%m-%d')} à {c.rdv.heure.strftime('%H:%M')}"
        })

    return JsonResponse(results, safe=False)
from django.shortcuts import render
from .models import Prescription

def prescription_list(request):
    # Récupérer toutes les prescriptions avec les relations nécessaires
    prescriptions = Prescription.objects.select_related(
        'consultation__dossier__etudiant',
        'consultation__medecin',
        'consultation__rdv',
        'medicament'
    ).all()

    # Récupération des filtres depuis GET
    consultation_query = request.GET.get('consultation', '').strip()
    etudiant_query = request.GET.get('etudiant', '').strip()
    medicament_query = request.GET.get('medicament', '').strip()
    id_query = request.GET.get('id', '').strip()

    # Application des filtres
    if consultation_query:
        parts = consultation_query.split()
        q = Q()
        for part in parts:
            q &= (
        Q(consultation__medecin__nom__icontains=part) |
        Q(consultation__medecin__prenom__icontains=part) 
    )
        prescriptions = prescriptions.filter(q)
    if etudiant_query:
        parts = etudiant_query.split()  # pour gérer Nom et/ou Prénom
        q = Q()
        for part in parts:
           q &= (
            Q(consultation__dossier__etudiant__nom__icontains=part) |
            Q(consultation__dossier__etudiant__prenom__icontains=part)
        )
        prescriptions = prescriptions.filter(q)
    if medicament_query:
        prescriptions = prescriptions.filter(
        medicament__nom_medicament__icontains=medicament_query
    )
    if id_query:
        prescriptions = prescriptions.filter(id=id_query)

    # Ajouter des attributs dynamiques pour le template
    for p in prescriptions:
        # Consultation
        if p.consultation and p.consultation.rdv and p.consultation.medecin:
            date_str = p.consultation.rdv.date_rdv.strftime('%Y-%m-%d')  # date
            heure_str = p.consultation.rdv.heure.strftime('%H:%M')       # heure
            p.consultation_str = f"{date_str} à {heure_str} - Dr {p.consultation.medecin.nom} {p.consultation.medecin.prenom}"
        else:
            p.consultation_str = "-"
        # Étudiant
        if p.consultation and p.consultation.dossier and p.consultation.dossier.etudiant:
            etu = p.consultation.dossier.etudiant
            p.etudiant_str = f"{etu.nom} {etu.prenom}"
        else:
            p.etudiant_str = "-"

        # Médicament et durée
        p.medicament_str = p.medicament.nom_medicament if p.medicament else "-"
        p.duree_str = p.duree or "-"

    context = {
        'prescriptions': prescriptions,
        'request': request 
    }

    return render(request, 'hopital/prescription_list.html', context)
def autocomplete_medicament(request):
    term = request.GET.get('term', '')
    medicaments = Medicament.objects.filter(nom_medicament__istartswith=term)[:10]
    results = []
    for m in medicaments:
        results.append({'id': m.id, 'nom_medicament': m.nom_medicament, 'forme': m.forme})
    return JsonResponse(results, safe=False)
def prescription_create(request):
    form = PrescriptionForm(request.POST or None)
    
    if form.is_valid():
        prescription = form.save(commit=False)
        prescription.save()

        messages.success(request, "Prescription créée avec succès !")
        return redirect('prescription_list')

    return render(request, 'hopital/prescription_form.html', {'form': form})


def prescription_update(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    form = PrescriptionForm(request.POST or None, instance=prescription)
    if form.is_valid():
        form.save()
        return redirect('prescription_list')
    return render(request, 'hopital/prescription_form.html', {'form': form})

def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        prescription.delete()
        return redirect('prescription_list')
    return render(request, 'hopital/prescription_confirm_delete.html', {'prescription': prescription})

# ====== VACCINATION ======

def vaccination_list(request):
    vaccinations = Vaccination.objects.select_related('dossier__etudiant').all()

    id_vaccin = request.GET.get('id', '').strip()
    nom_vaccin_query = request.GET.get('nom_vaccin', '').strip()
    date_vaccin = request.GET.get('date_vaccin', '').strip()
    etudiant_query = request.GET.get('etudiant', '').strip()

    # Application des filtres
    if id_vaccin:
        vaccinations = vaccinations.filter(id=id_vaccin)
    if nom_vaccin_query:
        vaccinations = vaccinations.filter(
            Q(nom_vaccin__icontains=nom_vaccin_query)
        )
    if etudiant_query:
        vaccinations = vaccinations.filter(
            Q(dossier__etudiant__nom__icontains=etudiant_query) |
            Q(dossier__etudiant__prenom__icontains=etudiant_query)
        )
    if date_vaccin:
        vaccinations = vaccinations.filter(date_vaccin__date=date_vaccin)
    vaccinations = vaccinations.order_by('id')

    vaccins_list = Vaccination.objects.values_list('nom_vaccin', flat=True).distinct()
    etudiant_list = Etudiant.objects.values_list('nom', 'prenom').distinct()

    return render(request, 'hopital/vaccination_list.html', {
        'vaccinations': vaccinations,
        'vaccins_list': vaccins_list,
        'etudiant_list': etudiant_list
    })
    
    
    
def vaccination_create(request):
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            form.save()  # la date est automatiquement remplie
            return redirect('vaccination_list')
    else:
        form = VaccinationForm()
    return render(request, 'hopital/vaccination_form.html', {'form': form})
def vaccination_update(request, pk):
    vaccination = get_object_or_404(Vaccination, pk=pk)
    form = VaccinationForm(request.POST or None, instance=vaccination)
    if form.is_valid():
        form.save()
        return redirect('vaccination_list')
    return render(request, 'hopital/vaccination_form.html', {'form': form})

def vaccination_delete(request, pk):
    vaccination = get_object_or_404(Vaccination, pk=pk)
    if request.method == 'POST':
        vaccination.delete()
        return redirect('vaccination_list')
    return render(request, 'hopital/vaccination_confirm_delete.html', {'vaccination': vaccination})


# ===== Vue SPA =====
def vue_spa(request):
    """Point d'entrée pour l'interface Vue.js SPA."""
    return render(request, 'hopital/vue_spa.html')
