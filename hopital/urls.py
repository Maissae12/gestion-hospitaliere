from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('agent/', views.agent_tables, name='agent_tables'),
    path('medecin/', views.medecin_tables, name='medecin_tables'),
    path('home_dashboard/', views.home_dashboard, name='home_dashboard'),
    path('dossier/medecin/',views.dossier_listmedecin,name='dossier_listmedecin'),
    path('', views.home_dashboard, name='dashboard'),
    path('', views.user_login, name='login'),  # page d'accueil = 
    path('dossier/<int:pk>/', views.dossier_detailmedecin, name='dossier_detailmedecin'),
    path('agent/stats-consultations/', views.agent_consultation_stats, name='agent_consultation_stats'),
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('medecin/dashboard/', views.medecin_dashboard, name='medecin_dashboard'),
    path('etudiant/<int:etudiant_id>/', views.etudiant_detail, name='etudiant_detail'),
    path('medecin/<int:pk>/', views.medecin_detail, name='medecin_detail'),
    path('dossier/<int:pk>/', views.dossier_detail, name='dossier_detail'),
    path('rendezvous/<int:pk>/', views.rdv_detail, name='rdv_detail'),
    path('consultations/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('autocomplete/medicament/', views.autocomplete_medicament, name='autocomplete_medicament'),
    path("autocomplete-rdv/", views.autocomplete_rdv, name="autocomplete_rdv"),
    path('login/', auth_views.LoginView.as_view(template_name='hopital/login.html'), name='login'),
   # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path("autocomplete-etudiant-dossier/",views.autocomplete_etudiant_dossier, name="autocomplete_etudiant_dossier"),
    path("autocomplete/consultation/", views.autocomplete_consultation, name="autocomplete_consultation"),
    path("autocomplete-rdv/", views.autocomplete_rdv, name="autocomplete_rdv"),
    path('autocomplete/dossier/', views.autocomplete_dossier, name='autocomplete_dossier'),
    path('autocomplete/etudiant/', views.autocomplete_etudiant, name='autocomplete_etudiant'),
    path('autocomplete/medecin/', views.autocomplete_medecin, name='autocomplete_medecin'),
    path('etudiants/', views.etudiant_list, name='etudiant_list'),
    path('etudiants/ajouter/', views.etudiant_create, name='etudiant_create'),
    path('etudiants/<int:pk>/modifier/', views.etudiant_update, name='etudiant_update'),
    path('etudiants/<int:pk>/supprimer/', views.etudiant_delete, name='etudiant_delete'),
     # DossierMedical
    path('dossiers/', views.dossier_list, name='dossier_list'),
    path('dossiers/ajouter/', views.dossier_create, name='dossier_create'),
    path('dossiers/<int:pk>/modifier/', views.dossier_update, name='dossier_update'),
    path('dossiers/<int:pk>/supprimer/', views.dossier_delete, name='dossier_delete'),
    # Medecin
    path('medecins/', views.medecin_list, name='medecin_list'),
    path('medecins/ajouter/', views.medecin_create, name='medecin_create'),
    path('medecins/<int:pk>/modifier/', views.medecin_update, name='medecin_update'),
    path('medecins/<int:pk>/supprimer/', views.medecin_delete, name='medecin_delete'),
    # RendezVous
    path('rendezvous/', views.rdv_list, name='rdv_list'),
    path('rendezvous/ajouter/', views.rdv_create, name='rdv_create'),
    path('rendezvous/<int:pk>/modifier/', views.rdv_update, name='rdv_update'),
    path('rendezvous/<int:pk>/supprimer/', views.rdv_delete, name='rdv_delete'),
    # Consultation
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('consultations/ajouter/', views.consultation_create, name='consultation_create'),
    path('consultations/<int:pk>/modifier/', views.consultation_update, name='consultation_update'),
    path('consultations/<int:pk>/supprimer/', views.consultation_delete, name='consultation_delete'),
    # Medicament
    path('medicaments/', views.medicament_list, name='medicament_list'),
    path('medicaments/ajouter/', views.medicament_create, name='medicament_create'),
    path('medicaments/<int:pk>/modifier/', views.medicament_update, name='medicament_update'),
    path('medicaments/<int:pk>/supprimer/', views.medicament_delete, name='medicament_delete'),
    # Prescription
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/ajouter/', views.prescription_create, name='prescription_create'),
    path('prescriptions/<int:pk>/modifier/', views.prescription_update, name='prescription_update'),
    path('prescriptions/<int:pk>/supprimer/', views.prescription_delete, name='prescription_delete'),
    # Vaccination
    path('vaccinations/', views.vaccination_list, name='vaccination_list'),
    path('vaccinations/ajouter/', views.vaccination_create, name='vaccination_create'),
    path('vaccinations/<int:pk>/modifier/', views.vaccination_update, name='vaccination_update'),
    path('vaccinations/<int:pk>/supprimer/', views.vaccination_delete, name='vaccination_delete'),
]


