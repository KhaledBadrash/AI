# his/config.py

# RabbitMQ server host (local)
RABBITMQ_HOST = 'localhost'

# Direct exchange name
EXCHANGE_NAME = 'student_data_exchange'

# Routing keys for each consumer
ROUTING_KEY_PEREGOS  = 'peregos'
ROUTING_KEY_WYSEFLOW = 'wyseflow'

# Hard-coded programs with start date, total credits and modules
# Each module has a name and credit points
HARD_CODED_PROGRAMS = {
    'Computer Science': {
        'start_date': '2023-10-01',
        'credits':    120,
        'modules': [
            # 1st semester
            {'name': 'Algebra',                 'credits': 5},
            {'name': 'Analysis',                'credits': 5},
            {'name': 'Intro to Computer Science','credits': 5},
            {'name': 'C & OO Basics',           'credits': 15},
            {'name': 'Elective (Eng/Biz)',      'credits': 5},

            # 2nd semester
            {'name': 'Discrete Mathematics',    'credits': 5},
            {'name': 'Computer Architecture',   'credits': 5},
            {'name': 'Algorithms & Data Struct','credits': 5},
            {'name': 'Theory of Computation',   'credits': 5},
            {'name': 'Elective (Eng/Biz II)',   'credits': 5},

            # 3rd semester
            {'name': 'SW Engineering – Analysis','credits': 5},
            {'name': 'Statistics',              'credits': 5},
            {'name': 'OOP in Java',             'credits': 5},
            {'name': 'Databases',               'credits': 5},
            {'name': 'Computer Networks',       'credits': 5},
            {'name': 'Operating Systems',       'credits': 5},

            # 4th semester
            {'name': 'SW Engineering – Design', 'credits': 5},
            {'name': 'Real-Time Systems',       'credits': 5},
            {'name': 'IT Security',             'credits': 5},
            {'name': 'Distributed Systems',     'credits': 5},
            {'name': 'Networks Lab',            'credits': 5},
            {'name': 'Programming Exercises',   'credits': 5},

            # 5th semester
            {'name': 'Law & Data Protection',   'credits': 5},
            {'name': 'Current CS Topics',       'credits': 5},
            {'name': 'CS Project',              'credits': 10},
            {'name': 'Elective Module',         'credits': 5},
            {'name': 'Interdisciplinary Studies','credits': 5},

            # 6th semester
            {'name': 'Industry Placement',      'credits': 18},
            {'name': 'Bachelor Thesis + Viva',  'credits': 12},
        ]
    },

    'Business Information Systems': {
        'start_date': '2024-02-10',
        'credits':    180,
        'modules': [
            # 1st semester
            {'name': 'Algebra',                 'credits': 5},
            {'name': 'Accounting',              'credits': 5},
            {'name': 'Business Administration', 'credits': 5},
            {'name': 'Intro to BIS',            'credits': 5},
            {'name': 'OOP Basics',              'credits': 10},

            # 2nd semester
            {'name': 'Study Skills',            'credits': 5},
            {'name': 'OS & Networks',           'credits': 5},
            {'name': 'Databases',               'credits': 5},
            {'name': 'Commercial Law',          'credits': 5},
            {'name': 'Business English',        'credits': 5},
            {'name': 'Analysis',                'credits': 5},

            # 3rd semester
            {'name': 'Statistics',              'credits': 5},
            {'name': 'Web-App Systems',         'credits': 5},
            {'name': 'Process Mgmt.',           'credits': 5},
            {'name': 'Privacy & Internet Law',  'credits': 5},
            {'name': 'Logistics & Production',  'credits': 5},
            {'name': 'SW Engineering',          'credits': 5},

            # 4th semester
            {'name': 'Architecture & Integration','credits': 5},
            {'name': 'BIS Seminar',             'credits': 5},
            {'name': 'Data Warehousing',        'credits': 5},
            {'name': 'Digital Business',        'credits': 5},
            {'name': 'ERP Systems',             'credits': 5},
            {'name': 'Project Mgmt.',           'credits': 5},

            # 5th semester
            {'name': 'IT Security',             'credits': 5},
            {'name': 'Usability Engineering',   'credits': 5},
            {'name': 'Elective Module',         'credits': 5},
            {'name': 'General Academic Studies','credits': 5},
            {'name': 'BIS Modelling',           'credits': 5},
            {'name': 'IS Management',           'credits': 5},

            # 6th semester
            {'name': 'Practical Training',      'credits': 30},

            # 7th semester
            {'name': 'Project',                 'credits': 18},
            {'name': 'Bachelor Thesis',         'credits': 12},
        ]
    },

    'Business Administration': {
        'start_date': '2024-10-01',
        'credits':    210,
        'modules': [
            # 1st semester
            {'name': 'Intro to BA & HRM',      'credits': 5},
            {'name': 'Accounting I',            'credits': 5},
            {'name': 'Private Law I',           'credits': 5},
            {'name': 'Business Info I',         'credits': 5},
            {'name': 'Math for Econ I',         'credits': 5},
            {'name': 'Core Skills',             'credits': 5},

            # 2nd semester
            {'name': 'Finance & Investment',    'credits': 5},
            {'name': 'Accounting II',           'credits': 5},
            {'name': 'Private Law II',          'credits': 5},
            {'name': 'Econ Statistics',         'credits': 5},
            {'name': 'Math for Econ II',        'credits': 5},
            {'name': 'Microeconomics',          'credits': 5},

            # 3rd semester
            {'name': 'Marketing & Production',  'credits': 5},
            {'name': 'Accounting III',          'credits': 5},
            {'name': 'Corporate Taxation',      'credits': 5},
            {'name': 'Macroeconomics',          'credits': 5},
            {'name': 'Business Info II',        'credits': 5},
            {'name': 'Generale Studies',        'credits': 5},

            # 4th semester
            {'name': 'Major Elective 1',        'credits': 10},
            {'name': 'Major Elective 2',        'credits': 10},
            {'name': 'Minor Elective 1',        'credits': 5},
            {'name': 'Minor Elective 2',        'credits': 5},

            # 5th semester
            {'name': 'Major Elective 3',        'credits': 10},
            {'name': 'Major Elective 4',        'credits': 10},
            {'name': 'Minor Elective 3',        'credits': 5},
            {'name': 'Minor Elective 4',        'credits': 5},

            # 6th semester
            {'name': 'Practical Module',        'credits': 30},

            # 7th semester
            {'name': 'Major Elective 5',        'credits': 10},
            {'name': 'Major Elective 6',        'credits': 10},
            {'name': 'Thesis + Viva',           'credits': 10},
        ]
    },

    'Social Work': {
        'start_date': '2024-02-10',
        'credits':    180,
        'modules': [
            # semesters 1–2
            {'name': 'Foundations of SW',        'credits': 10},
            {'name': 'Social Work Law',          'credits': 10},
            {'name': 'Society & Personality',    'credits': 10},
            {'name': 'Research Methods',         'credits': 5},

            # semesters 3–4
            {'name': 'Advanced Concepts',        'credits': 10},
            {'name': 'Interdisciplinary Cases',  'credits': 5},
            {'name': 'Law II',                   'credits': 5},
            {'name': 'Society II',               'credits': 5},
            {'name': 'Economics II',             'credits': 5},
            {'name': 'Methods & Concepts',       'credits': 10},
            {'name': 'Org & Financing',          'credits': 5},

            # semester 5
            {'name': 'Practicum Prep',          'credits': 5},
            {'name': 'Practicum',               'credits': 20},

            # semesters 6–7
            {'name': 'Diversity & Inclusion I', 'credits': 10},
            {'name': 'Diversity & Inclusion II','credits': 10},
            {'name': 'Generale Studies',        'credits': 5},
            {'name': 'Advanced Seminar',        'credits': 20},
            {'name': 'Project Work',            'credits': 5},
            {'name': 'Bachelor Thesis',         'credits': 10},
        ]
    }
}
