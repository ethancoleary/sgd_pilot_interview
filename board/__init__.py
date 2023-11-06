from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'board'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    FEMALE_NAMES = [
             'Zoe',  'Abbie',  'Chloe',  'Grace',  'Emma'
        ]
    MALE_NAMES = [
        'Jacob', 'Aiden',  'Matthew',  'Alexander',  'Daniel',
    ]
    TYPE = ['Won', 'Lucky']
    TEAM = ['Mix', 'Male']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    manager1 = models.IntegerField()
    manager1_name = models.StringField()
    manager1_type = models.BooleanField()
    manager1_team = models.BooleanField()

    manager2 = models.IntegerField()
    manager2_name = models.StringField()
    manager2_type = models.BooleanField()
    manager2_team = models.BooleanField()



# PAGES
class Intro(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
