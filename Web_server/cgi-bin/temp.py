#!/usr/bin/python3
#dos2unix /home/utente/Scrivania/brezza/cgi-bin/temp.py

import datetime
import random
import matplotlib.pyplot as plt
import base64
import psutil
import io
import time
import urllib.parse

def TemperatureUmidita():
    data = []  # Lista per memorizzare i dati
    for _ in range(10):  
        now = datetime.datetime.now()
        ts = datetime.datetime.timestamp(now)
        temperatura = random.randint(20, 100)
        umidita = random.randint(20, 100)
        data.append((ts, temperatura, umidita))  # Aggiungi i dati alla lista
        time.sleep(0.05)  # Simula un ritardo
    return data  # Restituisci i dati raccolti

def get_cpu_temperature():
    try:
        temp = psutil.sensors_temperatures()
        return temp['coretemp'][0].current if 'coretemp' in temp else None
    except Exception:
        return None

def get_disk_usage():
    usage = psutil.disk_usage('/')
    return usage.total, usage.used, usage.free

def get_battery_status():
    battery = psutil.sensors_battery()
    return battery.percent if battery else None

def create_plot(data, title, xlabel, ylabel):
    buffer = io.BytesIO()
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(data)), data, marker='o', label=title, color='blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_pie_chart(data, labels, title):
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 8))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    plt.title(title, fontsize=16)
    plt.axis('equal')
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_bar_chart(data, labels, title):
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

def download_csv(data):
    output = io.StringIO()
    output.write("Epoca,Temperatura,Umidità\n")
    for timestamp, temp, hum in data:
        output.write(f"{timestamp},{temp},{hum}\n")
    output.seek(0)
    return output.getvalue()

def display_system_info(random_data):
    print("Content-type: text/html; charset=utf-8\r\n")
    print("<html><head><title>Temperature and Humidity</title>")
    print("""
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: limegreen;
            color: white;
        }
        h1, h2 {
            text-align: center;
            color: blue;
        }
        .container {
            max-width: 1200px;
            margin: auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .card {
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            margin: 10px;
            padding: 20px;
            flex: 1 1 300px;
            min-width: 300px;
            text-align: center;
            color: black;
        }
        img {
            display: block;
            margin: auto;
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        a {
            display: inline-block;
            text-align: center;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: blue;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        a:hover {
            background-color: darkblue;
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

    temperatures, humidities = zip(*[(temp, hum) for _, temp, hum in random_data])

    # Sezione dati con layout responsive
    print("<h2>Dati di Temperatura e Umidità</h2>")
    print('<div class="container">')
    for timestamp, temp, hum in random_data:
        print(f"""
        <div class="card">
            <p><strong>Epoca:</strong> {timestamp}</p>
            <p><strong>Temperatura:</strong> {temp}°C</p>
            <p><strong>Umidità:</strong> {hum}%</p>
        </div>
        """)
    print('</div>')

    img_base64_random_temp = create_plot(temperatures, 'Temperatura (Dati Random)', 'Tempo', 'Temperatura (°C)')
    img_base64_real_temp = create_plot([cpu_temp]*10, 'Temperatura CPU (Reale)', 'Tempo', 'Temperatura (°C)') if cpu_temp else create_plot([0]*10, 'Temperatura CPU (Reale)', 'Tempo', 'Temperatura (°C)')
    
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

    # Link per scaricare i dati in formato CSV
    print('<a href="data:text/csv;charset=utf-8,' + urllib.parse.quote(download_csv(random_data)) + '" download="dati.csv">Scarica Dati CSV</a>')

    print("</body></html>")

def main():
    random_data = TemperatureUmidita()
    display_system_info(random_data)

if __name__ == "__main__":
    main()
