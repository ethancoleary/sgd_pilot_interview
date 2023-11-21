from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'board'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    FEMALE_NAMES = [
             'Zoe',  'Abbie',  'Chloe',  'Grace',  'Emma', 'Ella', 'Viola', 'Sara'
        ]
    MALE_NAMES = [
        'Jacob', 'Aiden',  'Matthew',  'Alexander',  'Daniel', 'Joel', 'Harvey', 'Mason'
    ]
    TYPE = ['Won', 'Quota']
    TEAM = ['Male', 'Mix']
    MALE_TEAM = [7, 8]
    MIX_TEAM = [6, 5]
    MANAGER_PERFORMANCE = [12, 14, 11, 16, 15, 12, 13]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    pseudonym_loc = models.IntegerField()

    manager1 = models.IntegerField()
    manager1_name = models.StringField()
    manager1_type = models.BooleanField()
    manager1_team = models.BooleanField()
    manager1_team1 = models.StringField()
    manager1_team2 = models.StringField()
    manager1_workerA = models.StringField()
    manager1_approve = models.BooleanField()

    manager2 = models.IntegerField()
    manager2_name = models.StringField()
    manager2_type = models.BooleanField()
    manager2_team = models.BooleanField()
    manager2_team1 = models.StringField()
    manager2_team2 = models.StringField()
    manager2_workerA = models.StringField()
    manager2_approve = models.BooleanField()



# PAGES
class Intro(Page):


    def vars_for_template(player):

        ##Take out own name
        participant = player.participant

        import random
        participant.female = 1
        participant.pseudonym = "Emma"
        participant.team1 = "Daniel"
        participant.team2 = "Jacob"
        participant.t3_observed = 0
        participant.t2_mixgroup = 0
        participant.compete = 1
        participant.board_payoff = 0

        if participant.female == 1: #Female
            player.pseudonym_loc = C.FEMALE_NAMES.index(participant.pseudonym)
            female_names = [s for s in C.FEMALE_NAMES if s != participant.pseudonym]
            male_names = C.MALE_NAMES
        else: #Male
            player.pseudonym_loc = C.MALE_NAMES.index(participant.pseudonym)
            male_names = [s for s in C.MALE_NAMES if s != participant.pseudonym]
            female_names = C.FEMALE_NAMES

        #Take out names come across
        ## First is own workers
        female_names = [s for s in female_names if s != participant.team1 and s != participant.team2]
        male_names = [s for s in male_names if s != participant.team1 and s != participant.team2]

        ## If was under observation, take out board names
        if participant.t3_observed == 1:
            for x in range(2):
                female_names = [s for s in female_names if s != participant.board_names[x]]
                male_names = [s for s in male_names if s != participant.board_names[x]]

        ## Now take out other options from the iteration that have been encountered
        ## Team composition:
        player.manager1_team = 1-participant.t2_mixgroup
        player.manager2_team = 1-participant.t2_mixgroup
        player.manager1_type = random.randint(0,1)
        player.manager2_type = 1 - player.manager1_type

        names = female_names + male_names
        number_names_left = len(names)-1

        player.manager1 = random.randint(0,number_names_left)
        player.manager1_name = names[player.manager1]

        player.manager2 = random.randint(0,number_names_left)
        while player.manager2 == player.manager1:
            player.manager2 = random.randint(0, number_names_left)

        player.manager2_name = names[player.manager2]

        if player.manager1_team == 0:

            male_names = [s for s in male_names if s != player.manager1_name]
            number_male_names_left = len(male_names) - 1

            player.manager1_team1 = male_names[
                                        random.randint(0, number_male_names_left)
                ]
            player.manager1_team2 = male_names[
                                        random.randint(0, number_male_names_left)
                ]
            while player.manager1_team1 == player.manager1_team2:
                player.manager1_team2 = male_names[
                    random.randint(0, number_male_names_left)
                ]

        else:

            female_names = [s for s in female_names if s != player.manager1_name]
            male_names = [s for s in male_names if s != player.manager1_name]

            number_female_names_left = len(female_names) - 1
            number_male_names_left = len(male_names) - 1

            player.manager1_team1 = female_names[
                random.randint(0, number_female_names_left)
            ]
            player.manager1_team2 = male_names[
                random.randint(0, number_male_names_left)
            ]

        if player.manager2_team == 0:

            male_names = [s for s in male_names if s != player.manager2_name and s!= player.manager1_team1 and s!=player.manager1_team2]

            number_male_names_left = len(male_names) - 1

            player.manager2_team1 = male_names[
                random.randint(0, number_male_names_left)
            ]
            player.manager2_team2 = male_names[
                random.randint(0, number_male_names_left)
            ]
            while player.manager2_team1 == player.manager2_team2:
                player.manager2_team2 = male_names[
                    random.randint(0, number_male_names_left)
                ]

        else:

            female_names = [s for s in female_names if s != player.manager2_name and s!= player.manager1_team1 and s!=player.manager1_team2]
            male_names = [s for s in male_names if s != player.manager2_name and s!= player.manager1_team1 and s!=player.manager1_team2]

            number_female_names_left = len(female_names) - 1
            number_male_names_left = len(male_names) - 1

            player.manager2_team1 = female_names[
                random.randint(0, number_female_names_left)
            ]
            player.manager2_team2 = male_names[
                random.randint(0, number_male_names_left)
            ]


class Manager1(Page):
    form_model = 'player'
    form_fields = ['manager1_approve']

    def vars_for_template(player):
        participant = player.participant

        #Winner or lucky
        type_of_manager = player.manager1_type
        if type_of_manager == True:
            promotion_via = "Competed for position and won."
        else:
            promotion_via = "Obtained position through random draw."

        #Male or mixed?
        team_composition = player.manager1_team

        #Team members
        import random
        workers = [player.manager1_team1, player.manager1_team2]
        worker1 = workers[random.randint(0,1)]
        worker2 = workers[1-workers.index(worker1)]

        worker_performances = [C.MALE_TEAM, C.MIX_TEAM]

        worker1_performance = worker_performances[team_composition][workers.index(worker1)]
        worker2_performance = worker_performances[team_composition][workers.index(worker2)]

        player.manager1_workerA = workers[random.randint(0,1)]
        workerA = player.manager1_workerA

        worker1A = workerA == worker1

        manager_performance = C.MANAGER_PERFORMANCE[random.randint(0,6)]

        return {
            'promotion_via':promotion_via,
            'manager_performance':manager_performance,
            'workerA':workerA,
            'worker1':worker1,
            'worker2':worker2,
            'worker1A':worker1A,
            'worker1_performance':worker1_performance,
            'worker2_performance':worker2_performance,

        }

    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.board_payoff += cu(0.5)

class Manager2(Page):
    form_model = 'player'
    form_fields = ['manager2_approve']

    def vars_for_template(player):
        participant = player.participant

        #Winner or lucky
        type_of_manager = player.manager2_type
        if type_of_manager == True:
            promotion_via = "Competed for position and won."
        else:
            promotion_via = "Obtained position through random draw."

        #Male or mixed?
        team_composition = player.manager2_team

        #Team members
        import random
        workers = [player.manager2_team1, player.manager2_team2]
        worker1 = workers[random.randint(0,1)]
        worker2 = workers[1-workers.index(worker1)]

        worker_performances = [C.MALE_TEAM, C.MIX_TEAM]

        worker1_performance = worker_performances[team_composition][workers.index(worker1)]
        worker2_performance = worker_performances[team_composition][workers.index(worker2)]

        player.manager2_workerA = workers[random.randint(0,1)]
        workerA = player.manager2_workerA

        worker1A = workerA == worker1

        manager_performance = C.MANAGER_PERFORMANCE[random.randint(0,6)]



        return {
            'promotion_via':promotion_via,
            'manager_performance':manager_performance,
            'workerA':workerA,
            'worker1':worker1,
            'worker2':worker2,
            'worker1A':worker1A,
            'worker1_performance':worker1_performance,
            'worker2_performance':worker2_performance,

        }

    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.board_payoff += cu(0.5)




page_sequence = [Intro, Manager1, Manager2]
