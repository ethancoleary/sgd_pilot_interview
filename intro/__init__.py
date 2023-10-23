from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    optionA= models.BooleanField()


# PAGES
class Welcome(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1




class RiskPref(Page):
    form_model = 'player'
    form_fields = ['optionA']

    def vars_for_template(player):
        round_number = player.round_number
        probability_1 = round_number
        probability_2 = 10 - round_number


class Results(Page):

    def is_displayed(player):
        return player.round_number > 10




page_sequence = [Welcome, RiskPref, Results]
