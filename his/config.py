# his/config.py

# RabbitMQ server host (lokal)
RABBITMQ_HOST = 'localhost'

# Direct exchange name
EXCHANGE_NAME = 'student_data_exchange'

# Routing keys für jeden Consumer
ROUTING_KEY_PEREGOS  = 'peregos'
ROUTING_KEY_WYSEFLOW = 'wyseflow'

# Fest definierte Studienprogramme mit Startdatum und Gesamt‐Credits
HARD_CODED_PROGRAMS = {
    'Computer Science': {
        'start_date': '2023-10-01',
        'credits':    120
    },
    'Business Information Systems': {
        'start_date': '2024-02-10',
        'credits':    180
    },
    'Business Administration': {
        'start_date': '2024-10-01',
        'credits':    210
    },
    'Social Work': {
        'start_date': '2024-02-10',
        'credits':    180
    },
    # Drei neue Programme
    'Mechanical Engineering': {
        'start_date': '2025-01-15',
        'credits':    240
    },
    'Electrical Engineering': {
        'start_date': '2025-02-01',
        'credits':    210
    },
    'Applied Mathematics': {
        'start_date': '2025-03-01',
        'credits':    180
    }
}