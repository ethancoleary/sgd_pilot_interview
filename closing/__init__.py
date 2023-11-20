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
    instructions = models.LongStringField()
    incentives = models.LongStringField()
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

class ThankYou(Page):

    @staticmethod
    def vars_for_template(player):
        participant = player.participant

        if participant.manager != 1:
            participant.total_earnings = cu(participant.interview_payoff) + cu(1)

        if participant.manager == 1 and participant.board != 1:
            participant.total_earnings = cu(participant.interview_payoff) + cu(participant.total_manager_payoff) + cu(2)

        if participant.manager == 1 and participant.board == 1:
            participant.total_earnings = cu(participant.interview_payoff) + cu(participant.total_manager_payoff) + cu(participant.board_payoff) + cu(2)

page_sequence = [Welcome, RiskPref, Feedback, ThankYou]
