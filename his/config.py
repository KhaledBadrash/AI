# his/config.py

# Hostname RabbitMQ-Servers (lokal)
RABBITMQ_HOST = 'localhost'

# Name des Direct-Exchange
EXCHANGE_NAME = 'student_data_exchange'

# Routing Keys für die beiden Consumer
ROUTING_KEY_PEREGOS  = 'peregos'
ROUTING_KEY_WYSEFLOW = 'wyseflow'

# Hart codierte Studiengänge mit ihrem Startdatum, Gesamt-Credits und Modulen
# Jedes Modul hat einen Namen und eine CP-Angabe
HARD_CODED_PROGRAMS = {
    'Informatik': {
        'start_date': '2023-10-01',
        'credits':    120,
        'modules': [
            # 1. Semester
            {'name': 'Algebra',                                      'credits': 5},
            {'name': 'Analysis',                                     'credits': 5},
            {'name': 'Einführung in die Informatik',                 'credits': 5},
            {'name': 'Programmierung in C & OO-Grundlagen',          'credits': 15},
            {'name': 'English bzw. BWL (Wahl)',                      'credits': 5},

            # 2. Semester
            {'name': 'Diskrete Mathematik',                          'credits': 5},
            {'name': 'Rechnerarchitekturen',                         'credits': 5},
            {'name': 'Algorithmen und Datenstrukturen',              'credits': 5},
            {'name': 'Theoretische Informatik, Automaten & Sprachen','credits': 5},
            {'name': 'English bzw. BWL (Wahl)',                      'credits': 5},

            # 3. Semester
            {'name': 'Software Engineering – Analysis',              'credits': 5},
            {'name': 'Statistics',                                   'credits': 5},
            {'name': 'OOP in Java – Advanced Course',                'credits': 5},
            {'name': 'Databases',                                    'credits': 5},
            {'name': 'Computer Networks (CN)',                       'credits': 5},
            {'name': 'Operating Systems',                            'credits': 5},

            # 4. Semester
            {'name': 'Software Engineering – Design',                'credits': 5},
            {'name': 'Real-Time Systems',                            'credits': 5},
            {'name': 'IT Security',                                  'credits': 5},
            {'name': 'Distributed Systems',                          'credits': 5},
            {'name': 'Practical Computer Networks & Applications',   'credits': 5},
            {'name': 'Programming Exercises',                        'credits': 5},

            # 5. Semester
            {'name': 'Recht und Datenschutz',                        'credits': 5},
            {'name': 'Aktuelle Themen der Informatik',               'credits': 5},
            {'name': 'Informatik Projekt',                           'credits': 10},
            {'name': 'Wahlpflichtmodul',                             'credits': 5},
            {'name': 'Interdisziplinäres Studium Generale',          'credits': 5},

            # 6. Semester
            {'name': 'Praxisphase',                                  'credits': 18},
            {'name': 'Bachelor-Arbeit mit Kolloquium',               'credits': 12},
        ]
    },

    'Wirtschaftsinformatik': {
        'start_date': '2024-02-10',
        'credits':    180,  # Summe aller BIS-Module
        'modules': [
            # Angelehnt an das Business Information Systems – Beispiel
            # 1. Semester
            {'name': 'Algebra',                  'credits': 5},
            {'name': 'Accounting',               'credits': 5},
            {'name': 'Business Administration',  'credits': 5},
            {'name': 'Business Information Sys.', 'credits': 5},
            {'name': 'OOP',                      'credits': 10},

            # 2. Semester
            {'name': 'Study Skills',             'credits': 5},
            {'name': 'OBS & Networks',            'credits': 5},
            {'name': 'Databases',                'credits': 5},
            {'name': 'Private Commercial Law',   'credits': 5},
            {'name': 'Business English',         'credits': 5},
            {'name': 'Analysis',                 'credits': 5},

            # 3. Semester
            {'name': 'Statistics',               'credits': 5},
            {'name': 'Web-based App Systems',    'credits': 5},
            {'name': 'Business Process Mgmt.',   'credits': 5},
            {'name': 'Data Privacy & Internet',  'credits': 5},
            {'name': 'Logistics & Productions',  'credits': 5},
            {'name': 'Software Engineering',     'credits': 5},

            # 4. Semester
            {'name': 'Architecture & Integration','credits': 5},
            {'name': 'Seminar Information Sys.', 'credits': 5},
            {'name': 'Data Warehousing',         'credits': 5},
            {'name': 'Digital Business & E-Commerce','credits': 5},
            {'name': 'ERP',                      'credits': 5},
            {'name': 'IS Project Mgmt.',         'credits': 5},

            # 5. Semester
            {'name': 'IT Security',              'credits': 5},
            {'name': 'Usability Engineering',    'credits': 5},
            {'name': 'Elective Module',          'credits': 5},
            {'name': 'General Academic Studies', 'credits': 5},
            {'name': 'Corp. Inf. Sys. Modelling','credits': 5},
            {'name': 'IS-Management',            'credits': 5},

            # 6. Semester
            {'name': 'Practical Training',       'credits': 30},

            # 7. Semester
            {'name': 'Project',                  'credits': 18},
            {'name': 'Bachelor Thesis',          'credits': 12},
        ]
    },

    'BWL': {
        'start_date': '2024-10-01',
        'credits':    210,
        'modules': [
            # 1. Semester
            {'name': 'Einführung BWL & HRM',     'credits': 5},
            {'name': 'Rechnungswesen I',         'credits': 5},
            {'name': 'Wirtschaftsprivatrecht I', 'credits': 5},
            {'name': 'Wirtschaftsinformatik I',  'credits': 5},
            {'name': 'Wirtschaftsmathematik I',  'credits': 5},
            {'name': 'Schlüsselkompetenzen',     'credits': 5},

            # 2. Semester
            {'name': 'Finanzierung & Investition','credits': 5},
            {'name': 'Rechnungswesen II',        'credits': 5},
            {'name': 'Wirtschaftsprivatrecht II','credits': 5},
            {'name': 'Wirtschaftsstatistik',     'credits': 5},
            {'name': 'Wirtschaftsmathematik II', 'credits': 5},
            {'name': 'Mikroökonomik',           'credits': 5},

            # 3. Semester
            {'name': 'Marketing & Produktion',   'credits': 5},
            {'name': 'Rechnungswesen III',       'credits': 5},
            {'name': 'Betriebliche Steuerlehre', 'credits': 5},
            {'name': 'Makroökonomik',            'credits': 5},
            {'name': 'Wirtschaftsinformatik II', 'credits': 5},
            {'name': 'Studium Generale',         'credits': 5},

            # 4. Semester (Schwerpunkt & Wahlpflicht)
            {'name': 'SP1 Modul1',               'credits': 10},
            {'name': 'SP2 Modul1',               'credits': 10},
            {'name': 'WPM 1',                    'credits': 5},
            {'name': 'WPM 2',                    'credits': 5},

            # 5. Semester
            {'name': 'SP1 Modul2',               'credits': 10},
            {'name': 'SP2 Modul2',               'credits': 10},
            {'name': 'WPM 3',                    'credits': 5},
            {'name': 'WPM 4',                    'credits': 5},

            # 6. Semester
            {'name': 'Praxis­modul',             'credits': 30},

            # 7. Semester
            {'name': 'SP1 Modul3',               'credits': 10},
            {'name': 'SP2 Modul3',               'credits': 10},
            {'name': 'Bachelor-Arbeit + Kolloq.', 'credits': 10},
        ]
    },

    'Soziale Arbeit': {
        'start_date': '2024-02-10',
        'credits':    180,
        'modules': [
            # 1. / 2. Semester
            {'name': 'Grundlagenmodul Pers. & Ges.',        'credits': 10},
            {'name': 'Grundlagenmodul Recht',               'credits': 10},
            {'name': 'Grundlagenmodul Ges., Ökonomie',      'credits': 10},
            {'name': 'Wissenschaftliches Arbeiten',         'credits': 5},

            # 3. / 4. Semester
            {'name': 'Konzeptionelles Vertiefungsmodul',    'credits': 10},
            {'name': 'Interdisziplinäre Fallarbeit',        'credits': 5},
            {'name': 'Aufbaumodul Recht',                   'credits': 5},
            {'name': 'Aufbaumodul Pers. & Ges.',            'credits': 5},
            {'name': 'Aufbaumodul Ges., Ökonomie',          'credits': 5},
            {'name': 'Methoden & Konzepte',                 'credits': 10},
            {'name': 'Organisation & Finanzierung',         'credits': 5},

            # 5. Semester
            {'name': 'Schwerpunktmodul Praxisvorbereitung', 'credits': 5},
            {'name': 'Schwerpunktmodul Praxisphase',        'credits': 20},

            # 6. / 7. Semester
            {'name': 'Diversität & Inklusion I',            'credits': 10},
            {'name': 'Diversität & Inklusion II',           'credits': 10},
            {'name': 'Studium Generale',                    'credits': 5},
            {'name': 'Vertiefung',                          'credits': 20},
            {'name': 'Projektorientierte Arbeiten',         'credits': 5},
            {'name': 'Bachelor-Thesis + Kolloq.',            'credits': 10},
        ]
    }
}
