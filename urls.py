from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('qualite_air/', views.traitement_donnees_qualite_air, name='qualite_air'),
    path('niveau_remplissage/', views.traitement_donnees_niveau_remplissage, name='niveau_remplissage'),
    path('detection_gaz/', views.traitement_donnees_detection_gaz, name='detection_gaz'),
    path('ouv_et_ferm/', views.ouv_et_ferm, name='ouv_et_ferm'),
    path('bin-state/', views.get_bin_state, name='get_bin_state'),
    path('get-data/', views.get_data, name='get_data'),
    path('open_bin/', views.send_signal_to_esp8266, name='send_signal_to_esp8266'),

]