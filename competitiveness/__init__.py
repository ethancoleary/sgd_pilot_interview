import random
import time

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'comp'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.1
    USE_POINTS = True
    COMPETITORS = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9
    ]
    COMPETITOR_NAMES = [
        "Zoe",
        "Chloe",
        "Chloe",
        "Emma",
        "Alexander",
        "Daniel",
        "Jacob",
        "Jacob",
        "Harvey"]
    COMPETITOR_SCORES = [
        3,
        4,
        5,
        7,
        8,
        5,
        3,
        6,
        4,
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    investment = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6'],
            [7, '7'],
            [8, '8'],
            [9, '9'],
            [10, '10']]
    )
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)
    belief_relative_before = models.IntegerField()
    belief_relative = models.IntegerField()
    belief_absolute = models.IntegerField(initial=0)
    combined_payoff = models.CurrencyField(initial=0)
    belief_absolute_payoff = models.CurrencyField(initial=0)
    interview_total_payoff = models.CurrencyField(initial=0)
    competitor = models.IntegerField()
    competitor_score = models.IntegerField()
    position = models.IntegerField()
    win = models.IntegerField(initial=0)


# PAGES
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()


def competitor(player):
    competitor = random.randint(0, 8)
    participant = player.participant

    participant.competitor = C.COMPETITOR_NAMES[competitor]
    participant.competitor_score = C.COMPETITOR_SCORES[competitor]


class Structure(Page):
    form_model = 'player'
    form_fields = ['investment']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        competitor(player)
        participant = player.participant
        participant.investment = player.investment


class Ready(Page):
    form_model = 'player'
    form_fields = ['belief_relative_before']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        win = cu(0.15 * player.investment + 0.005 * (10 - player.investment))
        lose = cu(0.005 * (10 - player.investment))

        return {
            'win': win,
            'lose': lose
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 20


class Task(Page):
    form_model = 'player'
    form_fields = ['number_entered']
    timer_text = 'Time left in interview task'
    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) >= 0

    @staticmethod
    def vars_for_template(player):
        # Generate a list of 25 random integers, each either 0 or 1
        ones = random.randint(1, 9)
        grid_numbers = [0, 0, 0,
                        0, 0, 0,
                        0, 0, 0]
        for i in range(9):
            if i < ones:
                grid_numbers[i] = 1
        random.shuffle(grid_numbers)
        player.correct_answer = ones

        return {
            'grid_numbers': grid_numbers
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.correct_answer == player.number_entered:
            player.score = 1


class Calculation(Page):
    timeout_seconds = 0.1

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    @staticmethod
    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum(p.score for p in all_players)

        participant = player.participant
        participant.compete_score = total_score

        if participant.compete_score > participant.competitor_score:
            participant.win_compete = 1
        if participant.compete_score < participant.competitor_score:
            participant.win_compete = 0

        if participant.compete_score == participant.competitor_score:
            participant.compete_payoff = cu(0.02 * (10 - participant.investment) * participant.compete_score)
        if participant.compete_score != participant.competitor_score:

            if participant.win_compete == 1:
                participant.compete_payoff = cu(0.03 * participant.investment * participant.compete_score) + cu(
                    0.01 * (10 - participant.investment) * participant.compete_score)

            if participant.win_compete == 0:
                participant.compete_payoff = cu(0.01 * (10 - participant.investment) * participant.compete_score)


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.compete_score == player.belief_absolute:
            player.belief_absolute_payoff = 0.5
        participant.belief_absolute_comp = player.belief_absolute
        participant.compete_payoff += player.belief_absolute_payoff

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if get_timeout_seconds(player) <= 0:
            return upcoming_apps[0]


page_sequence = [
    Structure,
    Ready,
    Task,
    Calculation,
    Belief
]
