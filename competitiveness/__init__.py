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
    COMPETITORS = [1,2,3,4,5,6,7,8,9]
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
    comprehension1 = models.IntegerField(
        choices=[
            [1, '$0.00'],
            [2, '$0.02'],
            [3, '$0.05'],
            [4, '$0.10'],
            [5, '$0.25']
        ],
        widget=widgets.RadioSelect
    )
    comprehension2 = models.IntegerField(
        choices=[
            [1, 'The payment scheme was fixed.'],
            [2, 'The payment scheme depended on how my performance compared to that of others.']
        ],
        widget=widgets.RadioSelect
    )
    comprehension3 = models.IntegerField(
        choices = [
            [1, '$0.00'],
            [2, '$0.02'],
            [3, '$0.10'],
            [4, '$0.25'],
            [5, 'It depends on my investment and how my performance compares to that of another participant']
        ],
        widget=widgets.RadioSelect
    )
    comprehension4 = models.IntegerField(
        choices = [
            [1, 'The more tokens I invest, the higher my payment per correct answer'],
            [2, 'The more tokens I invest, the higher the payment I receive if I have a lower score than my opponent & lower the payment I receive if I have a higher score than them'],
            [3, 'The more tokens I invest, the higher the payment I receive if I have a higher score than my opponent & lower the payment I receive if I have a lower score than them']
        ],
    )

    investment = models.IntegerField(
        widget=widgets.RadioSelect,
        choices= [
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
    belief_absolute = models.IntegerField(initial = 0)
    combined_payoff = models.CurrencyField(initial=0)
    belief_absolute_payoff = models.CurrencyField(initial=0)
    interview_total_payoff = models.CurrencyField(initial=0)
    competitor = models.IntegerField()
    competitor_score = models.IntegerField()
    position = models.IntegerField()
    win = models.IntegerField(initial = 0)


#def quota(player):
 #   import random
    #  treatment = random.randint(0,1)
    #   player.quota = treatment
    #player.participant.quota = player.quota

    #if player.participant.male == 1:
#   player.participant.quota = 0

def competitor(player):
    import random
    competitor = random.randint(0,8)
    participant = player.participant

    participant.competitor = C.COMPETITOR_NAMES[competitor]
    participant.competitor_score = C.COMPETITOR_SCORES[competitor]



timer_text = 'Time left in interview task'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()

def is_displayed1(player: Player):
    """only returns True if there is time left."""
    return get_timeout_seconds1(player) > 0

# PAGES
class Structure(Page):
    form_model = 'player'
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4']

    def is_displayed(subsession):
        return subsession.round_number == 1
    #def vars_for_template(player):
        #quota(player)


    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension1'] != 4:
            return "Answer to question 1 is wrong"
        if values['comprehension2'] != 1:
            return "Answer to question 2 is wrong"
        if values['comprehension3'] != 5:
            return "Answer to question 3 is wrong"
        if values['comprehension4'] != 3:
            return "Answer to question 4 is wrong"

class Decision(Page):
    form_model = 'player'
    form_fields = ['investment']

    def is_displayed(subsession):
        return subsession.round_number == 1
    #def vars_for_template(player):
        #quota(player)


    def before_next_page(player, timeout_happened):
        competitor(player)
        participant = player.participant
        participant.investment = player.investment

    @staticmethod
    def error_message(player: Player, values):
        if values['investment'] > 10:
            return "Investment is invalid"
        if values['investment'] < 0:
            return "Investment is invalid"


class Ready(Page):
    form_model = 'player'
    form_fields = ['belief_relative_before']
    def is_displayed(subsession):
        return subsession.round_number == 1

    def vars_for_template(player):
        participant = player.participant
        win = cu(0.03 * participant.investment + 0.01 *(10-participant.investment))
        lose = cu(0.01 * (10-participant.investment))

        return {
            'win': win,
            'lose': lose
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 20

class Task(Page):
    form_model = 'player'
    form_fields = ['number_entered']
    import random

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

    def before_next_page(player, timeout_happened):

        if player.correct_answer == player.number_entered:
            player.score = 1



class Calculation(Page):
    timeout_seconds = 0.1

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])

        participant = player.participant
        participant.compete_score = total_score

        if participant.compete_score > participant.competitor_score:
            participant.win_compete = 1
        if participant.compete_score < participant.competitor_score:
            participant.win_compete = 0


        if participant.compete_score == participant.competitor_score:
            participant.compete_payoff = cu(0.02 * (10 - participant.investment) * participant.compete_score)
        if participant.compete_score != participant.competitor_score:

            if participant.win_compete == 1 :
                participant.compete_payoff = cu(0.03* participant.investment * participant.compete_score) + cu(0.01 * (10-participant.investment)*participant.compete_score)

            if participant.win_compete == 0:
                participant.compete_payoff = cu(0.01 * (10-participant.investment)*participant.compete_score)


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.compete_score == player.belief_absolute:
            player.belief_absolute_payoff = 0.5
        participant.belief_absolute_comp = player.belief_absolute
        participant.compete_payoff += player.belief_absolute_payoff

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        participant = player.participant
        if get_timeout_seconds(player) <= 0:
            return upcoming_apps[0]






page_sequence = [Structure, Decision, Ready, Task, Calculation, Belief]

