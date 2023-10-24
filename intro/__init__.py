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
    stage_payoff = models.CurrencyField()




# PAGES
class Welcome(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1




class RiskPref(Page):
    form_model = 'player'
    form_fields = ['optionA']

    def vars_for_template(player):
        p1 = player.round_number
        p2 = 10 - player.round_number
        return {
            'p1':p1,
            'p2':p2
        }


class Results(Page):

    def is_displayed(player):
        return player.round_number >= 10

    def vars_for_template(player):

        import random
        roundnum = random.randint(1,10)
        paying_round = player.in_round(roundnum)
        pr_decision = paying_round.optionA
        die_roll = random.randint(1, 10)

        if pr_decision == 1 :

            if roundnum < die_roll+1 :
                player.stage_payoff = 2
            else:
                player.stage_payoff = 1.60

        if pr_decision == 0:

            if roundnum < die_roll+1 :
                player.stage_payoff = 3.85
            else:
                player.stage_payoff = 0.10

        return {
            'pr_decision':pr_decision,
            'roundnum':roundnum
        }



page_sequence = [Welcome, RiskPref, Results]
