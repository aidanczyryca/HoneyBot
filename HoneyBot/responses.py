# Responses to user messages in a guild. Not commands.
# Imports
import random
from colorama import init, Fore, Back, Style
import owteams
import lolteams
import main
from tabulate import tabulate

def handle_response(message) -> str:
    
    # processing the extra info. guild id and author name
    guild_id = int(message[0:message.find('|')])
    message = message[message.find('|')+1:]

    guild_name = str(message[0:message.find('|')])
    message = message[message.find('|')+1:]

    author_name = message[0:message.find('|')]
    message = message[message.find('|')+1:]

    p_message = message.lower()

    # lottery for fun on every message
    if random.randrange(1, 1_000_001) == 370_964:
        return 'Congratulations, you just rolled a 1/1,000,000 chance!'

    # uptime
    if p_message == '!uptime':
        return 'HoneyBot has been running since ' + main.startTime

    # coinflip
    if p_message == '!coinflip' or p_message == '!flip a coin':
        return random.choice(['Heads', 'Tails'])

    # roll x sided die
    if p_message.startswith('!roll'):
        request = (p_message.split())[1]
        dice = int(request[0:request.find('d')])
        sides = int(request[request.find('d')+1:])
        rnumbers = [random.randrange(1, sides + 1) for x in range(dice)]
        return rnumbers

    # to do list
    if p_message.startswith('!todo '):

        idea = p_message[len('!todo '):]

        if idea.startswith('remove '):
            remove = int(idea[len('remove'):]) - 1
            # try except to account for the different locations ubuntu and windows are running this from
            # ubuntu runs from the honeybot/honeybot/main.py
            # windows runs from honeybot/
            try:
                idea_file = open('HoneyBot/Logs/idea_list.txt', 'r')
            except:
                idea_file = open('/home/aidan/Documents/GitHub/HoneyBot/HoneyBot/Logs/idea_list.txt', 'r')
            idea_text = idea_file.readlines()
            idea_file.close()
            idea_text.pop(remove)
            try:
                idea_file = open('HoneyBot/Logs/idea_list.txt', 'w')
            except:
                idea_file = open('/home/aidan/Documents/GitHub/HoneyBot/HoneyBot/Logs/idea_list.txt', 'w')
            if remove == len(idea_text):
                idea_text[-1] = idea_text[-1][:-1]
            idea_file.writelines(idea_text)
            idea_file.close()
            return ('Idea #' + str(remove + 1) + ' Removed.')

        if idea.startswith('list'):
            try:
                idea_file_read = open('HoneyBot/Logs/idea_list.txt', 'r')
            except:
                idea_file_read = open('/home/aidan/Documents/GitHub/HoneyBot/HoneyBot/Logs/idea_list.txt', 'r')
            idea_text = idea_file_read.read()
            idea_file_read.close()
            return str('Idea List:\n' + '\n'.join([x+y for x,y in zip([str(i+1)+") " for i in range(len(idea_text))],idea_text.split('\n'))]))
        
        try:
            idea_file = open('HoneyBot/Logs/idea_list.txt', 'a')
        except:
            idea_file = open('/home/aidan/Documents/GitHub/HoneyBot/HoneyBot/Logs/idea_list.txt', 'a')
        idea_file.write('\n' + author_name + ' from ' + guild_name + ': ' + idea)
        idea_file.close()
        return 'Idea Added'

    # wikipedia
    if p_message.startswith('!wiki '):
        if p_message == '!wiki today':
            return 'https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today'
        
        search = (p_message[len('!wiki '):]).replace(' ', '_')
        return str(('https://en.wikipedia.org/wiki/' + search))

    # base !help
    help_text = [["'!coinflip' and '!flip a coin'", "'Heads' or 'Tails'"], 
        ["'!roll [number of dice]d[sides]'", "Result of dice with [sides] sides [number of dice] times."],
        ["'!todo [idea]'", "Adds to the todo list for this bot. Please be specific."],
        ["'!todo list'", "View the current idea list."],
        ["'!wiki [topic]'", "Wikipedia article or search for the [topic]."],
        ["'!wiki today'", "Wikipedia article for this day in history."]]


    # if guild is valley
    if guild_id == 310228470229893121:

        #total_hv_help = "```"
        hv_help = [["Any message with 'testme'", "Will return 'test detected'"],
            ["'!freemancheck [user ID]'", "How many times this user has Freeman Pointed."],
            ["'!freemancheck all'", "How many times every user has Freeman Pointed."]]

        if p_message == '!help':
            #return total_help_text + total_hv_help
            return '```' + tabulate(help_text, headers = ['Current Global Commands', 'Description'])\
                + '\n\n' + tabulate(hv_help, headers = ['Current Valley Commands', 'Description']) + '```'

        if 'testme' in p_message:
            return 'test detected'


        if p_message.startswith('!freemancheck'):
            user_id = str((p_message.split())[1])
            try:
                freeman_file = open('HoneyBot/Logs/freeman_tracker.txt', 'r')
            except:
                freeman_file = open('/home/aidan/Documents/GitHub/HoneyBot/HoneyBot/Logs/freeman_tracker.txt', 'r')
            text = freeman_file.read()
            count = str(text.count(user_id))
            hv_userids = {
                '223927273600974848' : 'Martin',
                '156079234043871232' : 'Danny',
                '193152197377130497' : 'Aidan',
                '264515808133120010' : 'Pierson',
                '253676502506274816' : 'Jack',
                '195226652203155456' : 'Thinh',
                '290623797521022978' : 'Paul',
                '283306317534199808' : 'Matt',
                '83381935610527744' : 'Chaan',
                '183274629626855425' : 'Garret',
                '354736112360751108' : 'Xavier',
                '175762517035974665' : 'Dom',
                '152871991706255360' : 'Adam',
                '372953817622249496' : 'Matt RM',
                '430451497923510273' : 'Art',
                '421834042443431936' : 'Sam',
                '432268933316476928' : 'Guise',
                '416745233284595722' : 'Tomas',
                '192748814870773762' : 'Bailey',
                '552184759326081044' : 'Aidan V'
            }
            
            if user_id == 'all':
                return ('```' + tabulate([[hv_userids[i]] + [str(text.count(i))] for i in hv_userids], \
                    headers = ['Names', 'Occurrences']) + '```')

            if user_id in hv_userids:
                return str(hv_userids[user_id] + ' has Freeman Pointed ' + str(text.count(user_id)) + ' times.\n')
            return 'User ID not recognized.'
                    

    # if guild is league of monkeys
    if guild_id == 368115567002910723:

        # help for this guild
        lom_help = [["'!owteams' followed by 10 registered names", "Returns the top 5 matches in order.'"],
        ["'!owplayers'", "Returns the current scores for all registered OW2 players.'"],
        ["'!lolteams' followed by 10 registered names", "Returns the top 5 matches in order.'"],
        ["'!lolplayers' followed by 10 registered names", "Returns the current scores for all registered LOL players.'"]]

        if p_message == '!help':
            return '```' + tabulate(help_text, headers = ['Current Global Commands', 'Description']) + '\n\n' \
                + tabulate(lom_help, headers = ['Current League of Monkey Commands', 'Description']) + '```'

        # give ow2 teams given list of 10 player names
        # !owteams name name name name name name name name name name 
        if p_message.startswith('!owteams'):
            players = p_message.split(' ')
            players.remove('!owteams')
            return owteams.findBest(players)

        # give list of all player effort values
        if p_message.startswith('!owplayers'):
            return '```' + (tabulate([[i]+[j for j in owteams.effort_values[i]] for i in owteams.effort_values], \
                headers = ['Player', 'Skill', 'Impact', 'Communcations'])) + '```'

        # give lol teams given list of 10 player names
        # !owteams name name name name name name name name name name 
        if p_message.startswith('!lolteams'):
            players = p_message.split(' ')
            players.remove('!lolteams')
            return lolteams.findBest(players)

        # give list of all player effort values
        if p_message.startswith('!lolplayers'):
            return '```' + (tabulate([[i]+[j for j in lolteams.effort_values[i]] for i in lolteams.effort_values], \
                headers = ['Player', 'Skill', 'Impact', 'Communcations'])) + '```'


    # after guild checks
    # default 'help'
    if p_message == '!help':
        return '```' + tabulate(help_text, headers = ['Current Global Commands', 'Description']) + '```'
