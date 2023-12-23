from os import environ

SESSION_CONFIGS = [
    dict(
        name='Main',
        app_sequence=[
            'intro',
            'ability',
            'competitiveness',
            'interview',
            'manager',
            # 'board',
            'closing'
        ],
        num_demo_participants=5
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    completion_code='CAI22CMG',
    participation_fee=0.00,
    doc=""
)

PARTICIPANT_FIELDS = [
    'quota',
    'risk_preference',
    'interview_score',
    'expiry',
    'compete',
    'ability_score',
    'ability_belief',
    'ability_payoff',
    'compete_score',
    'compete_payoff',
    'investment',
    'belief_absolute_comp',
    'competitor',
    'competitor_score',
    'interview_score',
    'interview_payoff',
    'interview_competitor1',
    'interview_competitor2',
    'interview_competitor3',
    'interview_type',
    'interview_competitor1_score',
    'interview_competitor2_score',
    'interview_competitor3_score',
    'manager',
    'combined_payoff',
    'stage1_payoff',
    'win_compete',
    't2_type',
    't2_malefirst',
    't3_observed',
    't4_maleboard',
    't4_femaleboard',
    'male',
    'total_round2_payoff',
    'stage2_payoff',
    'female',
    'gender',
    'pseudonym',
    'team',
    'team1',
    'team2',
    'round1_score',
    'total_round1_payoff',
    'total_manager_payoff',
    'board',
    'board_names',
    'board_payoff',
    'total_earnings'
]

SESSION_FIELDS = []
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = """ """
ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
SECRET_KEY = environ.get('OTREE_SECRET_KEY')

#ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


#SECRET_KEY = '7093968416517'