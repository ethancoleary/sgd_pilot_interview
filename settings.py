from os import environ

SESSION_CONFIGS = [
     dict(
         name='interview',
         #app_sequence = ['intro', 'interview', 'closing'],
         app_sequence=['board'],
         num_demo_participants=5,
     ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['blind', 'risk_preference', 'interview_score',  'expiry', 'compete', 'interview_score', 'interview_payoff', 'worker_id', 'worker_score', 'die_roll', 'manager',
                      't2_mixgroup', 't2_malefirst', 't3_observed', 't4_maleboard', 't4_femaleboard', 'male', 'female', 'pseudonym', 'team1', 'team2', 'round1_score', 'total_round1_payoff', 'board_names']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7093968416517'
