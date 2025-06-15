# AI

ai_rabbitmq_architektur/
│
├── his/                         # HIS-GUI + Publisher
│   ├── config.py                # RabbitMQ-Konfiguration
│   ├── publisher.py             # Versendet Nachrichten
│   └── his_gui.py               # Tkinter-GUI
│
├── peregos/                     # Consumer für Peregos
│   └── consumer_peregos.py
│
├── wyseflow/                    # Consumer für WyseFlow
│   └── consumer_wyseflow.py
│
├── utils/                       # Hilfsfunktionen
│   └── validation.py            # Validierung der Eingaben
│
├── start_all.py                 # Startet alle drei Komponenten parallel
└── requirements.txt             # Abhängigkeiten