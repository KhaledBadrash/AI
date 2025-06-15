# his/config.py

# Hostname RabbitMQ-Servers (lokal)
RABBITMQ_HOST = 'localhost'

# Name des Direct-Exchange
EXCHANGE_NAME = 'student_data_exchange'

# Routing Keys für die beiden Consumer
ROUTING_KEY_PEREGOS  = 'peregos'
ROUTING_KEY_WYSEFLOW = 'wyseflow'

# Hart codierte Studiengänge mit ihrem Startdatum und Credit Points
HARD_CODED_PROGRAMS = {
    'Informatik': {
        'start_date': '2023-10-01',
        'credits':    120
    },
    'Wirtschaft': {
        'start_date': '2023-04-01',
        'credits':     90
    }
}