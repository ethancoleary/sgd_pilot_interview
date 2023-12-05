from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ability'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.1
    USE_POINTS = True


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trial_answer1 = models.IntegerField()
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)
    belief_relative = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, '1st place'],
            [2, '2nd place'],
            [3, '3rd place'],
            [4, '4th place'],
        ],
        initial=1
    )
    belief_absolute = models.IntegerField(initial = 0)
    combined_payoff = models.CurrencyField(initial=0)
    belief_absolute_payoff = models.CurrencyField(initial=0)
    belief_relative_payoff = models.CurrencyField(initial=0)
    interview_total_payoff = models.CurrencyField(initial=0)



timer_text = 'Time left in interview task'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()

# PAGES
class Structure(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1


class TrialTask1(Page):
    form_model = 'player'
    form_fields = ['trial_answer1']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test_grid = [1, 0, 1,
                     0, 0, 0,
                     1, 0, 0]

        return {
            'test_grid': test_grid,
        }

    @staticmethod
    def error_message(player: Player, values):
        if values['trial_answer1'] != 3:
            return "Answer is incorrect"


class Ready(Page):
    def is_displayed(subsession):
        return subsession.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 20




class Task(Page):
    form_model = 'player'
    form_fields = ['number_entered']


    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) >= 0

    def vars_for_template(player):
        import random
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
            player.payoff = C.PAYMENT_PER_CORRECT_ANSWER
            player.score = 1



class Calculation(Page):
    timeout_seconds = 0.1

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])

        participant = player.participant
        participant.ability_score = total_score


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute']
    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.ability_score == player.belief_absolute:
            player.belief_absolute_payoff = 0.5

        participant.ability_belief = player.belief_absolute

        participant.ability_payoff = cu(
            player.belief_absolute_payoff + participant.ability_score * C.PAYMENT_PER_CORRECT_ANSWER)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        participant = player.participant
        if get_timeout_seconds(player) <= 0:
            return upcoming_apps[0]


page_sequence = [Structure, TrialTask1, Ready, Task, Calculation, Belief]

