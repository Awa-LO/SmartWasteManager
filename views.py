from django.shortcuts import render
from .models import FillLevel, AirQuality, GasDetection, BinState
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import socket

# Adresse IP et port de l'ESP8266
ESP8266_IP = '192.168.43.193'
ESP8266_PORT = 80

def index(request):
    return render(request, 'index.html', {'stars': []})

def dashboard(request):
    fill_level = FillLevel.objects.latest('timestamp')
    air_quality = AirQuality.objects.latest('timestamp')
    gas_detection = GasDetection.objects.latest('timestamp')
    bin_state = BinState.objects.latest('timestamp')
    return render(request, 'dashboard.html', {
        'fill_level': fill_level,
        'air_quality': air_quality,
        'gas_detection': gas_detection,
        'bin_state': bin_state
    })

@csrf_exempt
def traitement_donnees_qualite_air(request):
    if request.method == 'POST':
        ppm = request.POST.get('ppm')
        qualite = request.POST.get('qualite')
        if ppm and qualite:
            try:
                ppm = float(ppm)
                air_quality = AirQuality(ppm=ppm, qualite=qualite, timestamp=timezone.now())
                air_quality.save()
                return render(request, 'qualite_air.html', {
                    'air_quality': air_quality,
                    'success_message': "Données de qualité de l'air enregistrées avec succès."
                })
            except ValueError:
                return render(request, 'qualite_air.html', {'error_message': "Données de qualité de l'air invalides."})
        else:
            return render(request, 'qualite_air.html', {'error_message': "Données de qualité de l'air manquantes."})
    else:
        air_quality = AirQuality.objects.latest('timestamp')
        return render(request, 'qualite_air.html', {'air_quality': air_quality})

@csrf_exempt
def traitement_donnees_niveau_remplissage(request):
    if request.method == 'POST':
        fill_level = request.POST.get('fill_level')
        if fill_level:
            try:
                fill_level = float(fill_level)
                fill_level_entry = FillLevel(fill_level=fill_level, timestamp=timezone.now())
                fill_level_entry.save()

                if fill_level < 50:
                    fill_level_class = 'low'
                elif fill_level >= 50 and fill_level < 90:
                    fill_level_class = 'medium'
                else:
                    fill_level_class = 'high'

                return render(request, 'niveau_remplissage.html', {
                    'fill_level': fill_level_entry,
                    'fill_level_class': fill_level_class,
                    'success_message': "Données de niveau de remplissage enregistrées avec succès."
                })
            except ValueError:
                return render(request, 'niveau_remplissage.html', {
                    'error_message': "Données de niveau de remplissage invalides."
                })
        else:
            return render(request, 'niveau_remplissage.html', {
                'error_message': "Données de niveau de remplissage manquantes."
            })
    else:
        latest_fill_level = FillLevel.objects.latest('timestamp')

        if latest_fill_level.fill_level < 50:
            fill_level_class = 'low'
        elif latest_fill_level.fill_level >= 50 and latest_fill_level.fill_level < 90:
            fill_level_class = 'medium'
        else:
            fill_level_class = 'high'

        return render(request, 'niveau_remplissage.html', {
            'fill_level': latest_fill_level,
            'fill_level_class': fill_level_class
        })

@csrf_exempt
def traitement_donnees_detection_gaz(request):
    if request.method == 'POST':
        gas_detected = request.POST.get('gas_detected')
        ppm = request.POST.get('ppm')
        nh3 = request.POST.get('nh3')
        ch4 = request.POST.get('ch4')
        h2s = request.POST.get('h2s')

        if gas_detected and ppm and nh3 and ch4 and h2s:
            try:
                gas_detected = int(gas_detected)
                ppm = float(ppm)
                nh3 = float(nh3)
                ch4 = float(ch4)
                h2s = float(h2s)

                air_quality = AirQuality.objects.latest('timestamp')
                gas_detection_entry = GasDetection(gas_detected=gas_detected, ppm=ppm, nh3=nh3, ch4=ch4, h2s=h2s, timestamp=timezone.now())
                gas_detection_entry.save()

                if gas_detected == 10:
                    gas_status = "Gaz détecté !"
                    gas_status_class = "gas-detected"
                    action_message = "Veuillez Vider la poubelle et n'oubliez pas de prendre les mesures nécessaires pour vous protéger."
                    detected_gases = []
                    if nh3 > 10:
                        detected_gases.append("NH3")
                    if ch4 > 14:
                        detected_gases.append("CH4")
                    if h2s > 20:
                        detected_gases.append("H2S")
                else:
                    gas_status = "Gaz non détecté"
                    gas_status_class = "gas-not-detected"
                    action_message = ""
                    detected_gases = []

                return render(request, 'detection_gaz.html', {
                    'gas_detection': gas_detection_entry,
                    'air_quality': air_quality,
                    'gas_status': gas_status,
                    'gas_status_class': gas_status_class,
                    'action_message': action_message,
                    'detected_gases': detected_gases
                })

            except ValueError:
                return render(request, 'detection_gaz.html', {'error_message': "Données de détection de gaz invalides."})

        else:
            return render(request, 'detection_gaz.html', {'error_message': "Données de détection de gaz manquantes."})

    else:
        gas_detection = GasDetection.objects.latest('timestamp')
        air_quality = AirQuality.objects.latest('timestamp')

        if gas_detection.gas_detected == 1:
            gas_status = "Gaz détecté !"
            gas_status_class = "gas-detected"
            action_message = "Veuillez prendre les mesures nécessaires pour protéger votre santé."
            detected_gases = []
            if gas_detection.nh3 > 10:
                detected_gases.append("NH3")
            if gas_detection.ch4 > 14:
                detected_gases.append("CH4")
            if gas_detection.h2s > 20:
                detected_gases.append("H2S")
        else:
            gas_status = "Gaz non détecté"
            gas_status_class = "gas-not-detected"
            action_message = ""
            detected_gases = []

        return render(request, 'detection_gaz.html', {
            'gas_detection': gas_detection,
            'air_quality': air_quality,
            'gas_status': gas_status,
            'gas_status_class': gas_status_class,
            'action_message': action_message,
            'detected_gases': detected_gases
        })

@csrf_exempt
def ouv_et_ferm(request):
    if request.method == 'POST':
        bin_state = request.POST.get('state')
        if bin_state:
            bin_state_entry = BinState(state=bin_state, timestamp=timezone.now())
            bin_state_entry.save()
            if bin_state == 'Ouverte':
                bin_image = 'https://media.istockphoto.com/id/507077524/fr/photo/noir-ouvert-de-poubelle.jpg?s=612x612&w=0&k=20&c=vGwUfXH4vXicpMs3lADPVkG0znuTXR0QosL5QTVcZJo='
                # Envoyer un signal à l'ESP8266 pour ouvrir la poubelle et redémarrer les ultrasons
                send_signal_to_esp8266('open_bin')
            else:
                bin_image = 'https://th.bing.com/th/id/OIP.iA1hOn_LpHwixMrMRDuXRgHaIy?pid=ImgDet&w=199&h=235&c=7&dpr=1,5'
            return render(request, 'ouv_et_ferm.html', {
                'bin_state': bin_state,
                'last_update': bin_state_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'bin_image': bin_image
            })
    else:
        latest_bin_state = BinState.objects.latest('timestamp')
        if latest_bin_state.state == 'Ouverte':
            bin_image = 'https://media.istockphoto.com/id/507077524/fr/photo/noir-ouvert-de-poubelle.jpg?s=612x612&w=0&k=20&c=vGwUfXH4vXicpMs3lADPVkG0znuTXR0QosL5QTVcZJo='
        else:
            bin_image = 'https://th.bing.com/th/id/OIP.iA1hOn_LpHwixMrMRDuXRgHaIy?pid=ImgDet&w=199&h=235&c=7&dpr=1,5'
        return render(request, 'ouv_et_ferm.html', {
            'bin_state': latest_bin_state.state,
            'last_update': latest_bin_state.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'bin_image': bin_image
        })

@csrf_exempt
def get_bin_state(request):
    try:
        bin_state = BinState.objects.latest('timestamp')
        return JsonResponse({'state': bin_state.state, 'timestamp': bin_state.timestamp.isoformat()})
    except BinState.DoesNotExist:
        return JsonResponse({'state': 'Inconnue', 'timestamp': None})

@csrf_exempt
def get_data(request):
    fill_level = FillLevel.objects.latest('timestamp')
    air_quality = AirQuality.objects.latest('timestamp')
    gas_detection = GasDetection.objects.latest('timestamp')
    bin_state = BinState.objects.latest('timestamp')

    data = {
        'fill_level': {
            'timestamp': fill_level.timestamp.isoformat(),
            'fill_level': fill_level.fill_level,
        },
        'air_quality': {
            'timestamp': air_quality.timestamp.isoformat(),
            'ppm': air_quality.ppm,
            'qualite': air_quality.qualite,
        },
        'gas_detection': {
            'timestamp': gas_detection.timestamp.isoformat(),
            'gas_detected': gas_detection.gas_detected,
            'ppm': gas_detection.ppm,
            'nh3': gas_detection.nh3,
            'ch4': gas_detection.ch4,
            'h2s': gas_detection.h2s,
        },
        'bin_state': {
            'timestamp': bin_state.timestamp.isoformat(),
            'state': bin_state.state,
        },
    }
    return JsonResponse(data)


def send_signal_to_esp8266(signal):
    try:
        # Créer un socket et se connecter à l'ESP8266
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ESP8266_IP, ESP8266_PORT))

        # Envoyer le signal à l'ESP8266
        if signal == 'open_bin':
            sock.sendall(b'open_bin')

        # Fermer le socket
        sock.close()
    except Exception as e:
        print(f"Erreur lors de l'envoi du signal à l'ESP8266 : {e}")