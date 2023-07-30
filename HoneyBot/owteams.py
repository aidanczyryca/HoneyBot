# for finding good ow2 teams
import itertools
from tabulate import tabulate

# name (lowercase) : effort values
# EVs in order of Skill, Impact, Communications
effort_values = {
    'aidan' : [6, 6, 7], #
    'danny' : [10, 8, 10], #
    'matthew' : [0, 0, 0],
    'josh' : [5, 6, 2], #
    'pierson' : [5, 6.5, 2], #
    'paul' : [6.5, 7.5, 1.25], #
    'cole' : [5, 3, 3], #
    'matt' : [7, 6.5, 8.5], #
    'thinh' : [0, 0, 0],
    'dom' : [0, 0, 0],
    'ethan' : [5.5, 5, 3], #
    'ryan' : [0, 0, 0],
    'xavier' : [6, 4, 6], #
    'ravi' : [6.5, 6, 8], #
    'jake' : [7,5, 8, 7], #
    'dan' : [2, 1, 1], #
    'sam' : [7, 8, 2], # 
    'kylie' : [2, 1, 5], #
    'chaan' : [3, 4, 3], #
    'garret' : [8, 9, 6], #
    'martin' : [4, 5, 4], #
    'alex' : [0, 0, 0],
    'sgui' : [0, 0, 0],
    'jack' : [0, 0, 0],
    'steven' : [0, 0, 0],
    'robbie' : [2, 1, 5], # 
    'gman' : [5, 4, 6], #
    'lucas' : [3, 4, 3], #
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

