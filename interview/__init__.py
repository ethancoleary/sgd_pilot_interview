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

    COMPETITORS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    COMPETITOR_NAMES = [
        "Zoe",
        "Chloe D",
        "Chloe T",
        "Emma",
        "Alexander",
        "Daniel",
        "Jacob M",
        "Jacob R",
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

    INTERVIEW_TYPE = [1, 2, 3]
    PAIR = [[
        [1, 8], [3, 6], [2, 5], [4, 7]],
        [[3, 8], [6, 2], [1, 9]],
        [[9, 3], [8, 2], [4, 5]]
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)

    quota = models.BooleanField()
    belief_relative = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, '1st place'],
            [2, '2nd place'],
            [3, '3rd place'],
            [4, '4th place'],
        ],
    )
    belief_absolute = models.IntegerField(initial = 0)
    combined_payoff = models.CurrencyField(initial=0)
    belief_absolute_payoff = models.CurrencyField(initial=0)
    belief_relative_payoff = models.CurrencyField(initial=0)
    interview_total_payoff = models.CurrencyField(initial=0)
    position = models.IntegerField()


def quota(player):
    import random
    treatment = random.randint(0,1)
    player.quota = treatment
    player.participant.quota = player.quota

    if player.participant.male == 1:
        player.participant.quota = 0

def competitors(player):
    import random
    participant = player.participant

    if participant.male == 0 :
        competitor1 = random.randint(4,8)
        participant.interview_competitor1 = C.COMPETITOR_NAMES[competitor1]
        participant.interview_competitor1_score = C.COMPETITOR_SCORES[competitor1]

        competitor2 = random.randint(4, 8)
        while competitor2 == competitor1 :
            competitor2 = random.randint(4,8)
        participant.interview_competitor2 = C.COMPETITOR_NAMES[competitor2]
        participant.interview_competitor2_score = C.COMPETITOR_SCORES[competitor2]

        competitor3 = random.randint(0, 3)
        participant.interview_competitor3 = C.COMPETITOR_NAMES[competitor3]
        participant.interview_competitor3_score = C.COMPETITOR_SCORES[competitor3]

    if participant.male == 1:
        competitor1 = random.randint(0, 3)
        participant.interview_competitor1 = C.COMPETITOR_NAMES[competitor1]
        participant.interview_competitor1_score = C.COMPETITOR_SCORES[competitor1]

        competitor2 = random.randint(0, 3)
        while competitor2 == competitor1:
            competitor2 = random.randint(0, 3)
        participant.interview_competitor2 = C.COMPETITOR_NAMES[competitor2]
        participant.interview_competitor2_score = C.COMPETITOR_SCORES[competitor2]

        competitor3 = random.randint(4, 8)
        participant.interview_competitor3 = C.COMPETITOR_NAMES[competitor3]
        participant.interview_competitor3_score = C.COMPETITOR_SCORES[competitor3]


timer_text = 'Time left in interview task'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()


# PAGES
class Structure(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1
    def vars_for_template(player):
        quota(player)
        competitors(player)
        player.participant.manager = 0

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
        participant.interview_score = total_score

        male_pool = {
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
        }

        female_pool = {
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
        ## Worker 1 and 2 are always of opposite gender. Worker 3 is own gender.

        # Get order of workers.
        others_scores = [participant.interview_competitor1_score, participant.interview_competitor2_score,
                         participant.interview_competitor3_score]
        others_scores.sort(reverse=True)

        # Generate position
        if participant.interview_score >= others_scores[0]:
            player.position = 1

        if participant.interview_score < others_scores[0] and participant.interview_score >= others_scores[1]:
            player.position = 2

        if participant.interview_score < others_scores[1] and participant.interview_score >= others_scores[2]:
            player.position = 3

        if participant.interview_score < others_scores[2]:
            player.position = 4

        # No quota for men as of now.
        if participant.quota == 0:
            # Pick workers

            # Allocate payoff to those who win definitively
            if player.position <= 2:
                player.combined_payoff = 1
                participant.manager = 1

            # Randomly draw winning probability if it is a tie
            if participant.interview_score == others_scores[1]:
                roll = random.randint(0,1)
                if roll == 1:
                    player.combined_payoff = 1
                    participant.manager = 1
                else:
                    player.combined_payoff = 0
                    participant.manager = 0

            # Allocate payoff to those who lose
            if participant.interview_score < others_scores[1]:
                player.combined_payoff = 0
                participant.manager = 0

        # If female, have two cases. First is non-quota
        if participant.quota == 1:

            #Find score of top male worker.
            if participant.interview_competitor1_score >= participant.interview_competitor2_score:
                top_male_score = participant.interview_competitor1_score
            if participant.interview_competitor1_score < participant.interview_competitor2_score:
                top_male_score = participant.interview_competitor2_score

            #If better than best male, definitely get promoted. If best female, also get promoted
            if participant.interview_score > top_male_score or participant.interview_score > participant.interview_competitor3_score:
                player.combined_payoff = 1
                participant.manager = 1
            #Two cases where a draw could happen.
            #First is where player is just as good as top male competitor and other female is better than them,
            if participant.interview_score == top_male_score and participant.interview_competitor3_score > top_male_score:
                roll = random.randint(0, 1)
                if roll == 1:
                    player.combined_payoff = 1
                    participant.manager = 1
                else:
                    player.combined_payoff = 0
                    participant.manager = 0
            # Then if tie for top female
            if participant.interview_score == participant.interview_competitor3_score and participant.interview_score == top_male_score:
                roll = random.randint(0, 1)
                if roll == 1:
                    player.combined_payoff = 1
                    participant.manager = 1
                else:
                    player.combined_payoff = 0
                    participant.manager = 0





class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']
    def is_displayed(player):
        participant = player.participant
        return participant.manager == 1 and get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.interview_score == player.belief_absolute:
            player.belief_absolute_payoff = 0.5
        if player.belief_relative == player.position:
            player.belief_relative_payoff = 0.5

class Outcome(Page):

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):

        participant = player.participant



        if player.position == 1 :
            relative = "1st"

        if player.position == 2:
            relative = "2nd"

        if player.position == 3:
            relative = "3rd"

        if player.position == 4:
            relative = "4th"

        if participant.manager == 1:
            player.belief_relative_payoff = player.position == player.belief_relative

            if player.belief_relative == 1 :
                belief_relative = "1st"

            if player.belief_relative == 2:
                belief_relative = "2nd"

            if player.belief_relative == 3:
                belief_relative = "3rd"

            if player.belief_relative == 4:
                belief_relative = "4th"

            payoff_relative = player.belief_relative_payoff

        participant.interview_payoff = cu(player.belief_relative_payoff + player.belief_absolute_payoff + player.combined_payoff)

        import random
        round_draw = random.randint(1,3)

        if round_draw == 1:
            participant.stage1_payoff = participant.ability_payoff
        if round_draw == 2:
            participant.stage1_payoff = participant.compete_payoff
        if round_draw == 3:
            participant.stage1_payoff = participant.interview_payoff

        return {
            'belief_relative':belief_relative,
            'relative':relative,
            'payoff_relative':payoff_relative,
            'round_draw':round_draw
        }




    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        participant = player.participant
        if get_timeout_seconds(player) <= 0 and participant.manager == 1:
            return upcoming_apps[0]
        if participant.manager == 0:
            return upcoming_apps[-1]


page_sequence = [Structure, Ready, Task, Calculation, Belief, Outcome]

