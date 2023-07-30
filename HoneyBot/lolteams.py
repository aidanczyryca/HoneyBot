# for finding good lol teams
import itertools
from tabulate import tabulate

# name (lowercase) : effort values
# EVs in order of Skill, Impact, Communications
effort_values = {
    'sam' : [8.5, 6.5, 1],
    'danny' : [10, 10, 5],
    'matthew' : [8, 8, 2.5],
    'ethan' : [5, 3, 1.5],
    'dan' : [6.5, 4, 3],
    'garret' : [7.5, 6, 1.5],
    'jack' : [4, 5.5, 2.5],
    'dom' : [6, 6.5, 2],
    'robbie' : [4.75, 6, 3],
    'chaan' : [3.5, 5.5, 1.25],
    'xavier' : [2, 4, 2],
    'josh' : [2.25, 1.75, 1.2],
    'gman' : [2, 2, 2.5],
    'jake' : [7, 7, 3.5],
    'aidan' : [6.5, 5, 3.25],
    'pierson' : [3, 3.35, 1.5],
    'kylie' : [1.75, 2.35, 1.4],
    'steven' : [1.2, 2, 2],
    'ravi' : [1.5, 2, 1.25],
    'cole' : [1.2, 2, 2],
    'cas' : [1, 1, 1]
}

skill_W = 1.5
impact_W = 1.2
communications_W = 0.75

def findBest(names):
    allGames = list(itertools.combinations(itertools.combinations(names, 5), 2)) # list of tuple(tuple(str x 5), tuple(str x 5))
    removal_List = [] # list containing invalid games
    
    #(('josh', 'pierson', 'paul', 'matt', 'thinh'), ('josh', 'pierson', 'paul', 'matt', 'dom'))
    # filter out matches that have repeating players
    for match in allGames: # for each match in allGames
        for member in match[0]: # for each player in the first team
            if member in match[1]: # if that player is in the second team
                removal_List.append(match) # add to list containing invalid games
                break # go to the next match

    #print(allGames)
    result = [game for game in allGames if game not in removal_List] # record the game, for every game in allGames, if the game is not in the removal list
    allGames = result

    # find and keep track of the best 5 matches using team score differential
    best_matches = [1000, 1000, 1000, 1000, 1000] # best match differentials
    top_indexes = [0, 0, 0, 0, 0] # indexes of the best differentials of the same index
    for match in allGames: # for each match in allGames
        current_diff = round(abs(teamScore(match[0]) - teamScore(match[1])), 4) # calc the differential for the match
        for i in range(5): # for each best differential, in order of best to worst
            if current_diff < best_matches[i]: # if the current match differential is better than the current top differential
                # replace high_score's spot in both top_indexes and best_matches with current_diff
                best_matches[i] = current_diff # replace the differential that is being iterated through with the current match's differential
                top_indexes[i] = allGames.index(match) # record the index of the current match in allGames to top_indexes at the same position as the diff score 
                break
    
    # create a list of the top 5 matches (list of tuples)
    top5 = []
    for index in top_indexes:
        top5.append(allGames[index])
    
    # return the top 5 games as a string
    return teamScramble(top5)

    
def teamScore(team): # team as a tuple of 5 strings
    total = 0
    for player in team:
        total += playerScore(player)
    return round(total, 4) # return the team's score as a float

def playerScore(player): # player as a string
    score = effort_values[player][0]*skill_W + effort_values[player][1]*impact_W + effort_values[player][2]*communications_W
    return round(score, 4) # return the player's score as a float

def teamScramble(best): # list of the top 5 tuples
    return '```' + 'The top 5 matches for these players are:\n' + \
        tabulate([[i for i in j[0]]+["VS"]+[i for i in j[1]] for j in best]) + '```'

#if __name__ == '__main__':
#    print(findBest(['aidan', 'danny', 'kylie', 'josh', 'pierson', 'paul', 'cole', 'matt', 'ravi', 'jake']))

