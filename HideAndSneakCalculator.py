import random

LOWER = 1
UPPER = 4

class TeamMember:
    def __init__(self):
        self.choice = 0
        self.is_out = False

class SoloMember:
    def __init__(self):
        self.choice = 0

class SimulationStats:
    def __init__(self):
        self.team_wins = 0
        self.solo_wins = 0
        self.turn_1_solo_wins = 0
        self.turn_2_solo_wins = 0
        self.turn_3_solo_wins = 0

    def team_percent(self):
        return self.round_to_n_digits(self.team_wins / (self.team_wins + self.solo_wins))
    
    def solo_percent(self):
        return self.round_to_n_digits(self.solo_wins / (self.team_wins + self.solo_wins))
    
    def percent_of_total_solo_wins(self, turn_num):
        if (turn_num == 1):
            return self.round_to_n_digits(self.turn_1_solo_wins / (self.team_wins + self.solo_wins))
        if (turn_num == 2):
            return self.round_to_n_digits((self.turn_1_solo_wins + self.turn_2_solo_wins) / (self.team_wins + self.solo_wins))
        if (turn_num == 3):
            return self.round_to_n_digits((self.turn_1_solo_wins + self.turn_2_solo_wins + self.turn_3_solo_wins) / (self.team_wins + self.solo_wins))

    def round_to_n_digits(self, num):
        return float('%.3g' % (num * 100))

def get_random_with_exclusions(lower, upper, excluded_choices_set):
    rand = None
    while rand is None or rand in excluded_choices_set:
        rand = random.randint(lower, upper)
    return rand

def simulate_hide_and_sneak(simulation_stats, is_team, debug):
    # Define basic settings
    print_if_debug(debug, "---------------------")
    excluded_choices = set()
    team_members = [TeamMember(), TeamMember(), TeamMember()]
    solo_member = SoloMember()

    # Turn 1
    if simulate_turn(team_members, solo_member, excluded_choices, debug, 1):
        simulation_stats.solo_wins += 1
        simulation_stats.turn_1_solo_wins += 1
        print_if_debug(debug, "Solo Wins!")
        return
    
    # Turn 2 
    if simulate_turn(team_members, solo_member, excluded_choices, debug, 2):
        simulation_stats.solo_wins += 1
        simulation_stats.turn_2_solo_wins += 1
        print_if_debug(debug, "Solo Wins!")
        return
    
    # Turn 3
    if simulate_turn(team_members, solo_member, excluded_choices, debug, 3):
        simulation_stats.solo_wins += 1
        simulation_stats.turn_3_solo_wins += 1
        print_if_debug(debug, "Solo Wins!")
        return
    
    # Team survived! Congrats.
    simulation_stats.team_wins += 1
    print_if_debug(debug, "Team Wins!")
    return

def print_if_debug(debug, string):
    if (debug):
        print(string)

def simulate_turn(team_members, solo_member, excluded_choices, debug, turn_num):
    print_if_debug(debug, f'Starting Turn {turn_num}. Previously Chosen: {"None" if len(excluded_choices) == 0 else excluded_choices}')
    # Team members choose a value
    result_string = "Team Members chose: ["
    num_processed = 0
    for team_member in team_members:
        if (not team_member.is_out):
            team_member.choice = get_random_with_exclusions(LOWER, UPPER, excluded_choices)
            if num_processed == 2:
                result_string += "" + str(team_member.choice) + "]"
            else:
                result_string += "" + str(team_member.choice) + ", "
        else:
            if num_processed == 2:
                result_string += "out]"
            else:
                result_string += "out, "
        num_processed += 1
    
    print_if_debug(debug, result_string)

    # Solo member chooses a value
    solo_member.choice = get_random_with_exclusions(LOWER, UPPER, excluded_choices)
    print_if_debug(debug, f'Solo chose {solo_member.choice}')

    # Compare choices
    for team_member in team_members:
        if (not team_member.is_out):
            if solo_member.choice == team_member.choice:
                team_member.is_out = True
                print_if_debug(debug, "LOSER!")
    
    # Update exclusions 
    excluded_choices.add(solo_member.choice)
    
    # returns if the game is over
    if (all_team_members_out(team_members)):
        return True # true means we lose
    return False

def all_team_members_out(team_members):
    for team_member in team_members:
        if (not team_member.is_out):
            return False
    return True

print("SIMULATING MARIO PARTY SUPERSTARS MINIGAME: Hide and Sneak")
num_simulations = 1000000
simulations_stats = SimulationStats()
for i in range(num_simulations):
    # TODO: keep tally and then print results
    if i % (round(num_simulations / 10)) == 0:
        print(f'Processing Simulation Number {i}')
    simulate_hide_and_sneak(simulations_stats, True, False)

print(f'Solo Wins: {simulations_stats.solo_wins}. Odds: {simulations_stats.solo_percent()}% \nTeam Wins: {simulations_stats.team_wins}. Odds: {simulations_stats.team_percent()}%')
print(f'Turn 1 Solo Wins: {simulations_stats.turn_1_solo_wins}. Odds Solo wins by Turn 1: {simulations_stats.percent_of_total_solo_wins(1)}%')
print(f'Turn 2 Solo Wins: {simulations_stats.turn_2_solo_wins}. Odds Solo wins by Turn 2: {simulations_stats.percent_of_total_solo_wins(2)}%')
print(f'Turn 3 Solo Wins: {simulations_stats.turn_3_solo_wins}. Odds Solo wins by Turn 3: {simulations_stats.percent_of_total_solo_wins(3)}%')

print("CONCLUSION: Choose Team to win most of the time; choose Solo for an unlikely gamble on winning early.")