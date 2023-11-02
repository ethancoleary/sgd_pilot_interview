from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'manager'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.15
    TEAMS = [['Jacob', 'Daniel'], ['Matthew', 'Zoe']]
    TEAMS_SCORE = [[5, 6], [5, 4]]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    t2_mixgroup = models.BooleanField()
    t2_malefirst = models.BooleanField()
    t3_observed = models.BooleanField()
    t4_maleboard = models.BooleanField(initial=0)
    t4_femaleboard = models.BooleanField(initial=0)
    team1 = models.StringField()
    team1_score = models.IntegerField()
    team2 = models.StringField()
    team2_score = models.IntegerField()
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)
    belief_absolute = models.IntegerField()
    belief_relative = models.IntegerField(
        widget=widgets.RadioSelect,
        choices = [1, 2, 3]
    )
    round1_performance_payment = models.CurrencyField()
    belief_absolute_payoff = models.CurrencyField()
    belief_relative_payoff = models.CurrencyField(initial=0)


    workerA_team1 = models.BooleanField()

timer_text = 'Time left in this round'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()

def t2(player):
    import random

    t2 = random.randint(0,1)
    player.t2_mixgroup = t2
    player.participant.t2_mixgroup = player.t2_mixgroup


    malefirst = random.randint(0,1)
    player.t2_malefirst = malefirst
    player.participant.t2_malefirst =  player.t2_malefirst

def t3(player):
    import random
    t3 = random.randint(0,1)
    player.t3_observed = t3
    player.participant.t3_observed = player.t3_observed

def t4(player):
    import random
    t4 = random.randint(0,2)
    if t4 == 1:
        player.t4_maleboard = 1
        player.participant.t4_maleboard = player.t4_maleboard
    if t4 == 2:
        player.t4_femaleboard = 1
        player.participant.t4_femaleboard = player.t4_femaleboard

# PAGES
class TeamWelcome(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1
    def vars_for_template(player):
        t2(player)



        team = C.TEAMS[player.t2_mixgroup]
        player.team1 = team[1-player.t2_malefirst]
        player.team2 = team[player.t2_malefirst]

        participant = player.participant

        participant.team1 = player.team1
        participant.team2 = player.team2



class Round1Intro(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1

    def vars_for_template(player):
        import random
        # Generate a list of 16 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(16)]

        return {
            'grid_numbers': grid_numbers
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 20

class Round1(Page):
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
            player.payoff = C.PAYMENT_PER_CORRECT_ANSWER


class Calculation(Page):
    timeout_seconds = 0.1

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])
        player.round1_performance_payment = sum([p.payoff for p in all_players])

        participant = player.participant
        participant.round1_score = total_score
        player.round1_performance_payment = total_score * C.PAYMENT_PER_CORRECT_ANSWER

        t3(player)
        t4(player)

class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']
    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.round1_score == player.belief_absolute:
            player.belief_absolute_payoff = 1


class Round1Results(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):
        participant = player.participant
        team_score = C.TEAMS_SCORE[participant.t2_mixgroup]
        player.team1_score = team_score[1 - participant.t2_malefirst]
        player.team2_score = team_score[participant.t2_malefirst]
        x=participant.round1_score

        round1_scores = [x, player.team1_score, player.team2_score]
        sorted_round1_score = sorted(round1_scores)
        player_positions = sorted_round1_score.index(x)

        if player_positions != 3 :
            tie = sorted_round1_score[player_positions] == sorted_round1_score[player_positions+1]
        else:
            tie = 0

        if tie == 0 :
            if player_positions == player.belief_relative:
                player.belief_relative_payoff = 1
        if tie == 1 :
            if player_positions == player.belief_relative or player_positions+1 == player.belief_relative:
                player.belief_relative_payoff = 1



page_sequence = [TeamWelcome, Round1Intro, Round1, Calculation, Belief, Round1Results]
