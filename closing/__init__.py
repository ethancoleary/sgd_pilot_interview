from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PARTICIPATION = 2
    PARTICIPATION_WORKER = 1.3


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
    feedback = models.LongStringField(blank=True)


# PAGES

class RiskPref(Page):
    form_model = 'player'
    form_fields = ['riskyness']

    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.manager == 1


class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback']


    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        if participant.manager == 1:
            total_bonus = participant.stage1_payoff + participant.stage2_payoff
            total_pay = cu(total_bonus + C.PARTICIPATION)
        if participant.manager == 0:
            total_bonus = participant.stage1_payoff
            total_pay = cu(total_bonus+C.PARTICIPATION_WORKER)



        return {
            'total_bonus': total_bonus,
            'total_pay': total_pay
        }


class Redirect(Page):
    @staticmethod
    def vars_for_template(player):
        code = player.session.config['completion_code']
        link = f"https://app.prolific.co/submissions/complete?cc={code}"

        return dict(
            link=link,
        )


page_sequence = [
    RiskPref,
    Feedback,
    Redirect
]
