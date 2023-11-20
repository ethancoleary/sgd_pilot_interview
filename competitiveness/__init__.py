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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    investment = models.IntegerField(
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
    form_fields = ['investment']

    def is_displayed(subsession):
        return subsession.round_number == 1
    #def vars_for_template(player):
        #quota(player)


    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.investment = player.investment


class Ready(Page):
    form_model = 'player'
    form_fields = ['belief_relative_before']
    def is_displayed(subsession):
        return subsession.round_number == 1

    def vars_for_template(player):
        win = cu(0.15 * player.investment + 0.005 *(10-player.investment))
        lose = cu(0.005 * (10-player.investment))

        return {
            'win': win,
            'lose': lose
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 30

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
        grid_numbers = [random.randint(0, 1) for _ in range(9)]
        player.correct_answer = sum(grid_numbers)

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


        pool = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 1,
            20: 1,
            21: 1,
            23: 1,
            24: 1,
            25: 1,
            26: 1,
            27: 1,
            28: 1,
            29: 1,
            30: 1,
            31: 1,
        }

        import random
        player.competitor, player.competitor_score = random.choice(list(pool.items()))
        participant.competitor = player.competitor
        participant.competitor_score = player.competitor_score

        if participant.compete_score > player.competitor_score:
            participant.win_compete = 1
        if participant.compete_score < player.competitor_score:
            participant.win_compete = 0


        if participant.compete_score == player.competitor_score:
            participant.compete_payoff = cu(0.02 * (10 - participant.investment) * participant.compete_score)
        if participant.compete_score != player.competitor_score:

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






page_sequence = [Structure, Ready, Task, Calculation, Belief]

