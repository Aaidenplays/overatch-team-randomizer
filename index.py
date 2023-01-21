import json
from random import randint
import ipdb
import sys

# all the heroes and roles
roles = ["tank", "damage", "support"]
tank = ["Reinhardt", "Doomfist", "DVa", "Winston", "Orisa", "Roadhog", "Sigma", "WreckingBall", "Zarya", "JunkerQueen", "Ramattra"]
damage = ["Hanzo", "Widowmaker", "Sombra", "Soldier76", "Torbjorn", "Reaper", "Ashe", "Sojourn", "Pharah", "Mei", "Cassidy", "Junkrat", "Tracer", "Symmetra", "Genji", "Echo", "Bastion"]
support = ["Mercy", "Moira", "Lucio", "Briggitte", "Baptiste", "Ana", "Kiriko", "Zenyatta"]

# player teams top filled in function team_comp_analysis()
team1_players = []
team2_players = []

# Final teams to be filled in functions handle_balanced_team() and handle_unbalanced_team()
team1 = []
team2 = []

# flag for which handler to utilize whether team is balanced or not
balanced = True

# will eventually contain the file data. defining at global scope to be populated in main function
data = {}


# separates players into their appropriate team array
# takes a count of the players to be used in validation step
# globals() returns an object whos keys are variables declared at the global scope
player_count = 0
def team_comp_analysis() -> None: 
    global player_count

    for team in data:
        for player in data[team]:
            player_name = data[team][player]
            if(type(player_name) == str and len(player_name) > 0):
                globals()[team+'_players'].append(player_name)
                player_count += 1

# function name self explanatory here
# globals() returns an object whos keys are variables declared at the global scope
# randint(start, end) returns a random integer between start and end arguments
# returning as a dictionary player -> hero
def randomly_generate_hero(player, role):
    hero = globals()[role][randint(0, len(globals()[role])-1)]
    return {player: hero}


# Custom exception to throw validation error
class AaidensException(Exception):
    pass
# Validates to make sure role composition numbers match the number of player values
def validate_player_count_to_role_composition():
    global balanced
    if(balanced):
        role_counts = data["balanced_role_composition"]
        total_role_count = (role_counts["tank"] + role_counts["damage"] + role_counts["support"]) * 2
    else:
        team1_role_counts = data["team1"]["role_composition"]
        team2_role_counts = data["team2"]["role_composition"]
        total_role_count = team1_role_counts["tank"] + team1_role_counts["damage"] + team1_role_counts["support"] + team2_role_counts["tank"] + team2_role_counts["damage"] + team2_role_counts["support"]
    # ipdb.set_trace()
    if(total_role_count != player_count):
        raise AaidensException('role composition does NOT match player count')

# Handles logic for unbalanced teams
# TODO: Consider alternative looping strategy. some variables are declared in loop and not used. UGLY...
def handle_balanced_team():
    validate_player_count_to_role_composition()
    global team1_players
    global team2_players

    for role in roles:
        role_count = data["balanced_role_composition"][role]
        role_range = range(0, role_count)
        team_index_decrementer = len(team1_players)-1
        for a in role_range:
            random_player_index = randint(0, team_index_decrementer)
            random_player = team1_players[random_player_index]
            team1.append(randomly_generate_hero(random_player, role))
            del team1_players[random_player_index]

            random_player_index = randint(0, team_index_decrementer)
            random_player = team2_players[random_player_index]
            team2.append(randomly_generate_hero(random_player, role))
            del team2_players[random_player_index]
            
            team_index_decrementer -= 1

# Handles logic for unbalanced teams
# TODO: Consider refactoring to reduce code smell of duplicated looping logic
# TODO: Consider alternative looping strategy. some variables are declared in loop and not used. UGLY...
def handle_unbalanced_team():
    global balanced
    balanced = False
    validate_player_count_to_role_composition()
    global team1_players
    global team2_players
    
    for role in roles:
        role_count = data["team1"]["role_composition"][role]
        role_range = range(0, role_count)
        team_index_decrementer = len(team1_players)-1
        for a in role_range:
            random_player_index = randint(0, team_index_decrementer)
            random_player = team1_players[random_player_index]
            team1.append(randomly_generate_hero(random_player, role))
            del team1_players[random_player_index]

            team_index_decrementer -= 1

        role_count = data["team2"]["role_composition"][role]
        role_range = range(0, role_count)
        team_index_decrementer = len(team2_players)-1
        for a in role_range:
            random_player_index = randint(0, team_index_decrementer)
            random_player = team2_players[random_player_index]
            team2.append(randomly_generate_hero(random_player, role))
            del team2_players[random_player_index]

            team_index_decrementer -= 1

# Defining main function
def main():
    global data
 
    # Check if balanced argument was passed in command line 
    # Conditionally check which file to use based on whether 
    # team is balanced or not. decided by aforementioned arg
    balance_ind = 'b'
    if(len(sys.argv) > 1):
        balance_ind = sys.argv[1]
    if(balance_ind != 'b'):
        team_file = 'team_comp_unbalanced.json'
    else:
        team_file = 'team_comp_balanced.json'

    # Open the appropriate file 
    with open(team_file) as file:
        data = json.load(file)
    
    # run analysis on data and handle balanced vs unbalanced logic
    team_comp_analysis()
    if(player_count % 2 == 0):
        handle_balanced_team()
    else:
        handle_unbalanced_team()


    # PRINT final results to the terminal
    # TEAM 1 RESULTS
    print(":::::::TEAM 1 COMPOSITION randomly generated B):::::::")
    for player in team1:
        for name in player:
            print(name + " - " + player[name])
    # TEAM 2 RESULTS
    print(":::::::TEAM 2 COMPOSITION randomly generated B):::::::")
    for player in team2:
        for name in player:
            print(name + " - " + player[name])
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()