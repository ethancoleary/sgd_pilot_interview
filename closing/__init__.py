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
    riskyness = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'Never take risks'],
            [2, 'Rarely take risks'],
            [3, 'Sometimes take risks'],
            [4, 'Often take risks'],
            [5, 'Always take risks']
        ]
    )
    instructions = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'Instructions were not clear at all'],
            [2, 'Instructions could be made slightly more clear'],
            [3, 'I mostly understood what I had to do but the broader concept was confusing'],
            [4, 'I understood completely what I had to do']]
    )
    incentives = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'I did not understand how my decisions affected my earnings'],
            [2, 'I understood how I would earn money but I could not easily compare decisions based on money'],
            [3, 'When making decisions, I always tried to compute my most profitable outcome']]
    )
    feedback = models.LongStringField(blank=True)





# PAGES
class Welcome(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1




class RiskPref(Page):
    form_model = 'player'
    form_fields = ['riskyness']

class Feedback(Page):
    form_model = 'player'
    form_fields = ['instructions', 'incentives', 'feedback']








page_sequence = [Welcome, RiskPref, Feedback]
