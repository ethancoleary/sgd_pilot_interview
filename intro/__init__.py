from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'base'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(initial=0)
    age = models.IntegerField(
        choices=[
            [1, '<20 years'],
            [2, '20-29 years'],
            [3, '30-39 years'],
            [4, '40-49 years'],
            [5, '50-59 years'],
            [6, '60-69 years'],
            [7, '70 years and over']
        ],
        widget=widgets.RadioSelect
    )
    experience = models.IntegerField(
        choices=[
            [1, 'No managerial experience'],
            [2, '0-2 years managerial experience'],
            [3, '3-10 years managerial experience'],
            [4, '>10 years managerial experience']
        ],
        widget=widgets.RadioSelect
    )
    education = models.IntegerField(
        choices=[
            [1, 'Did not graduate high school'],
            [2, 'High school graduate'],
            [3, 'Some college education'],
            [4, 'Undergraduate degree'],
            [5, 'Postgraduate degree']
        ],
        widget=widgets.RadioSelect
    )
    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Other'],
        ],
        widget=widgets.RadioSelect)
    pseudonym = models.StringField(
        widget=widgets.RadioSelect,
        choices=[
            'Zoe',
            'Abbie',
            'Chloe',
            'Grace',
            'Emma',
            'Ella',
            'Viola',
            'Sara',
            'Jacob',
            'Aiden',
            'Matthew',
            'Alexander',
            'Daniel',
            'Joel',
            'Harvey',
            'Mason',
        ]
    )


# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def error_message(player, values):
        solutions = dict(consent=1)
        if values != solutions:
            return "Please consent to participation or withdraw from the experiment by closing your browser."


class GenderElicit(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'experience']

    @staticmethod
    def before_next_page(player, timeout_happened):

        participant = player.participant

        if player.gender == 1:
            participant.male = 0
            participant.female = 1

        if player.gender == 2:
            participant.male = 1
            participant.female = 0

        if player.gender > 2:
            participant.male = 0
            participant.female = 0


class PseudonymElicit(Page):
    form_model = 'player'
    form_fields = ['pseudonym']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.pseudonym = player.pseudonym

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return upcoming_apps[0]


class Results(Page):
    pass


page_sequence = [
    Intro,
    GenderElicit,
    PseudonymElicit
]
