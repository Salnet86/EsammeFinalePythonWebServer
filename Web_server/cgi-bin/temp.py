#!/usr/bin/python3
#dos2unix /home/utente/Scrivania/brezza/cgi-bin/temp.py


import datetime
import random
import matplotlib.pyplot as plt
import base64
import psutil
import io
import time

def TemperatureUmidita():
    print("<html><head><title>Temperature and Humidity</title>")
    print("""
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1, h2 {
            text-align: center;
            color: #333;
        }
        table {
            margin: auto;
            border: 1px solid black;
            border-collapse: collapse;
            width: 90%;
            max-width: 800px;
            background-color: white;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #e2e2e2;
        }
        img {
            display: block;
            margin: auto;
            max-width: 100%;
            height: auto;
        }
    </style>
    """)
    print("</head><body>")
    print("<h1>Dati</h1>")

    print("<table>")
    print("<tr><th>Epoca</th><th>Temperatura</th><th>Umidità</th></tr>")

    for _ in range(10):  
        now = datetime.datetime.now()
        ts = datetime.datetime.timestamp(now)
        temperatura = random.randint(20, 100)
        umidita = random.randint(20, 100)

        print(f"<tr><td>{ts}</td><td>{temperatura}°C</td><td>{umidita}%</td></tr>")
        time.sleep(0.05)

    print("</table>")
    print("</body></html>")

def get_cpu_temperature():
    """Restituisce la temperatura della CPU."""
    try:
        temp = psutil.sensors_temperatures()
        return temp['coretemp'][0].current if 'coretemp' in temp else None
    except Exception:
        return None

def get_disk_usage():
    """Restituisce informazioni sul disco."""
    usage = psutil.disk_usage('/')
    return usage.total, usage.used, usage.free

def get_battery_status():
    """Restituisce la percentuale della batteria."""
    battery = psutil.sensors_battery()
    return battery.percent if battery else None

def generate_random_data(n):
    """Genera dati casuali di temperatura e umidità."""
    data = []
    for _ in range(n):
        data.append((random.randint(20, 100), random.randint(20, 100)))
    return data

def create_plot(data, title, xlabel, ylabel):
    """Crea un grafico a partire dai dati forniti."""
    buffer = io.BytesIO()
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(data)), data, marker='o', label=title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_pie_chart(data, labels, title):
    """Crea un grafico a torta."""
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 8))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title, fontsize=16)
    plt.axis('equal')  # Assicura che il grafico sia un cerchio
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_bar_chart(data, labels, title):
    """Crea un grafico a barre."""
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 6))
    plt.bar(labels, data, color=['green', 'red'])
    plt.title(title, fontsize=16)
    plt.ylabel('Percentuale (%)')
    plt.ylim(0, 100)
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def display_system_info():
    """Visualizza le informazioni sul sistema e i grafici."""
    print("Content-type: text/html; charset=utf-8\r\n")
    print("<html><head><title>Temperature and Humidity</title>")
    print("""
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1, h2 {
            text-align: center;
            color: #333;
        }
        img {
            display: block;
            margin: auto;
            max-width: 100%;
            height: auto;
        }
    </style>
    """)
    print("</head><body>")
    print("<h1>Sito</h1>")

    cpu_temp = get_cpu_temperature()
    disk_total, disk_used, disk_free = get_disk_usage()
    battery_status = get_battery_status()

    print("<h2>Informazioni di Sistema</h2>")
    if cpu_temp is not None:
        print(f"<p>Temperatura CPU: {cpu_temp:.1f}°C</p>")
    else:
        print("<p>Temperatura CPU: Non disponibile</p>")
    
    print(f"<p>Spazio totale disco: {disk_total / (1024 ** 3):.2f} GB</p>")
    print(f"<p>Spazio usato disco: {disk_used / (1024 ** 3):.2f} GB</p>")
    print(f"<p>Spazio libero disco: {disk_free / (1024 ** 3):.2f} GB</p>")
    print(f"<p>Stato batteria: {battery_status:.1f}%</p>" if battery_status is not None else "<p>Stato batteria: Non disponibile</p>")

    random_data = generate_random_data(10)
    temperatures, humidities = zip(*random_data)

    img_base64_random_temp = create_plot(temperatures, 'Temperatura (Dati Random)', 'Tempo', 'Temperatura (°C)')
    img_base64_real_temp = create_plot([cpu_temp]*10, 'Temperatura CPU (Reale)', 'Tempo', 'Temperatura (°C)') if cpu_temp else create_plot([0]*10, 'Temperatura CPU (Reale)', 'Tempo', 'Temperatura (°C)')
    
    # Grafico a barre per lo stato della batteria
    img_base64_battery_bar = create_bar_chart([battery_status, 100 - battery_status], ['Carica', 'Scarica'], 'Stato Batteria') if battery_status is not None else ''
    
    img_base64_disk_pie = create_pie_chart([disk_used, disk_free], ['Usato', 'Libero'], 'Utilizzo Disco')

    print("<h2>Grafico di Temperatura (Dati Random)</h2>")
    print(f'<img src="data:image/png;base64,{img_base64_random_temp}">')
    print("<h2>Grafico di Temperatura CPU (Reale)</h2>")
    print(f'<img src="data:image/png;base64,{img_base64_real_temp}">')
    print("<h2>Grafico Stato Batteria</h2>")
    if battery_status is not None:
        print(f'<img src="data:image/png;base64,{img_base64_battery_bar}">')
    print("<h2>Grafico Utilizzo Disco</h2>")
    print(f'<img src="data:image/png;base64,{img_base64_disk_pie}">')

    print("</body></html>")

# Chiamata alla funzione principale
display_system_info()
TemperatureUmidita()
