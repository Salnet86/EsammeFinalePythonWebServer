#!/usr/bin/python3
import datetime
import random
import time

def funzioneTemEpoca():
    now = datetime.datetime.now() 
    ts = str(datetime.datetime.timestamp(now))  
    temperatura = str(random.randint(20, 100))  
    umidita = str(random.randint(20, 100))      
    time.sleep(1)  
    print("Content-type:text/html; charset=utf-8\r\n\r\n")
    print(f"""
    <html>
    <head>
        <title>Temperature e umidità</title>
        <style>
            body {{
                background-color: lime;
                color: blue;
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            h1 {{
                color: blue;
                background-color: lightblue; /* Blu chiaro per il background */
                padding: 10px;
            }}
            .lampeggiante {{
                animation: lampeggio 1s infinite;
            }}
            @keyframes lampeggio {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            .button {{
                background-color: lightblue;
                color: black;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
                border-radius: 5px;
            }}
            @media (max-width: 600px) {{
                body {{
                    font-size: 14px;
                }}
                .button {{
                    font-size: 14px;
                    padding: 8px 16px;
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Temperatura: <span class="lampeggiante">{temperatura}°C</span></h1>
        <p>Epoca: <span class="lampeggiante">{ts}</span></p>
        <p>Umidità: <span class="lampeggiante">{umidita}%</span></p>
        <button class="button" onclick="window.location.href='http://127.0.0.1:8010/'">Torna a Index</button>
        <button class="button" onclick="location.reload();">Ricarica Pagina</button>
    </body>
    </html>
    """)

funzioneTemEpoca()
