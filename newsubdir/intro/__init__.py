from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    risk = models.FloatField()


# PAGES
class Welcome(Page):
    pass


class RiskPref(Page):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
