from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'interview'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.1
    USE_POINTS = True


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trial_task = models.IntegerField()
    trial_answer = models.IntegerField()
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)

    blind = models.BooleanField()
    compete = models.BooleanField()
    belief_relative = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [0, 'Lower Quartile: 0-25%'],
            [25, 'Lower-Mid Quartile: 26-50%'],
            [50, 'Upper-Mid Quartile: 51-75%'],
            [75, 'Upper Quartile: 76-100%'],
        ],
        initial = 0
    )
    belief_absolute = models.IntegerField(initial = 0)
    combined_payoff = models.CurrencyField(initial=0)
    belief_absolute_payoff = models.CurrencyField(initial=0)
    belief_relative_payoff = models.CurrencyField(initial=0)
    interview_total_payoff = models.CurrencyField(initial=0)


def blind(player):
    import random
    treatment = random.randint(0,1)
    player.blind = treatment
    player.participant.blind = player.blind


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

    def is_displayed(subsession):
        return subsession.round_number == 1
    def vars_for_template(player):
        blind(player)

class IntroToInterview(Page):
    def is_displayed(subsession):
        return subsession.round_number == 1

class TrialTask(Page):
    form_model = 'player'
    form_fields = ['trial_task']

    def is_displayed(subsession):
        return subsession.round_number == 1


    def vars_for_template(player):
        import random
        # Generate a list of 16 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(16)]
        player.trial_answer = sum(grid_numbers)

        return {
            'grid_numbers': grid_numbers
        }

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(trial_task = player.trial_answer)

        if values != solutions:
            return "Answer is incorrect, try again."


class Decision(Page):
    form_model = 'player'
    form_fields = ['compete']

    def is_displayed(subsession):
        return subsession.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.compete = player.compete
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
        participant = player.participant

        import random
        # Generate a list of 25 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(16)]
        player.correct_answer = sum(grid_numbers)

        return {
            'grid_numbers': grid_numbers
        }

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.correct_answer == player.number_entered:
            player.score = 1
            if participant.compete == 0:
                player.payoff = C.PAYMENT_PER_CORRECT_ANSWER
        else:
            player.score = 0
        participant.manager = 0


class Calculation(Page):
    timeout_seconds = 0.1

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])

        participant = player.participant
        participant.interview_score = total_score


        if participant.compete == 0:
            player.combined_payoff = participant.interview_score * C.PAYMENT_PER_CORRECT_ANSWER
            participant.combined_payoff = player.combined_payoff

        worker_pool = {
            "A": 1,
            "B": 1,
            "C": 1,
            "D": 1,
            "E": 1,
            "F": 1,
            "G": 1,
            "H": 1,
            "I": 1,
            "J": 1,
            "K": 1,
        }

        import random
        participant.worker_id, participant.worker_score = random.choice(list(worker_pool.items()))

        if participant.compete == 1:
            if participant.interview_score > participant.worker_score:
                player.combined_payoff = 2

        participant.die_roll = random.randint(1, 6)

        if participant.compete == 1:
            if participant.interview_score > participant.worker_score:
                participant.manager = 1
            else:
                participant.manager = 0

        if participant.compete == 0:
            if participant.die_roll <3:
                participant.manager = 1
            else:
                participant.manager = 0

class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']
    def is_displayed(player):
        participant = player.participant
        return participant.manager == 1 and participant.compete == 1 and get_timeout_seconds(player) <= 0


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.interview_score == player.belief_absolute:
            player.belief_absolute_payoff = 1


class Belief_die(Page):
    form_model = 'player'
    form_fields = ['belief_absolute']
    def is_displayed(player):
        participant = player.participant
        return participant.manager == 1 and participant.compete == 0 and get_timeout_seconds(player) <= 0


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.interview_score == player.belief_absolute:
            player.belief_absolute_payoff = 1

class Outcome(Page):

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):

        import random

        ball_pull = random.randint(1,10)
        red_balls = player.belief_relative / 10
        blue_balls = 10-red_balls

        participant = player.participant

        if ball_pull <= red_balls:
            if participant.compete == 1 and participant.manager ==1 :
                player.belief_relative_payoff = 1

        if ball_pull > red_balls:
            if participant.compete == 1 and participant.manager == 0:
                player.belief_relative_payoff = 0


        return {
            "red_balls": red_balls,
            "blue_balls": blue_balls,
            "ball_pull": ball_pull,
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        participant = player.participant
        if get_timeout_seconds(player) <= 0 and participant.manager == 1:
            return upcoming_apps[0]
        if participant.manager == 0:
            return upcoming_apps[-1]


page_sequence = [Structure, IntroToInterview, TrialTask, Decision, Task, Calculation, Belief, Belief_die, Outcome]

