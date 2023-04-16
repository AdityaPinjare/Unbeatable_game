import random

"""
The Unbeatable Dr. Nimm and The Magnanimous Dr. Nymm

In this version of Nimm, there are a number of heaps, each containing a random* number of stones. 
Players can remove any number of stones from any heap. The player who takes the last stone wins.

*This can be overridden by setting RANDOM_HEAPS to False.

The user must choose between two computer opponents:

1. Dr. Nimm plays perfectly. (With this option selected, the human player will always lose.)
2. Dr. Nymm is identical to Dr. Nimm, except that he makes one deliberate error per game.

Dr. Nimm's secret is that if the "nimm sum" of the heaps is nonzero at the start of the game, player 1
can always win if he plays correctly. Since this is usually the case, Dr. Nimm goes first by default.
However, if the nimm sum happens to be zero at the start of the game (which is sometimes possible with 
RANDOM_HEAPS enabled), Dr. Nimm cheats by switching the turn order. 

Dr. Nymm makes his one mistake at a random point in the game. The user must play correctly
from that point on to win the game.  
"""

#Number of heaps to use
#Using only 1 heap is not recommended 
#Using more than 3 heaps makes the game a bit long
N_HEAPS = 3
#If RANDOM_HEAPS == True, each heap takes a random value between HEAP_MIN and HEAP_MAX
#This should make the game more interesting. (If False, all heaps are the same size (DEFAULT_HEAP))
RANDOM_HEAPS = True
HEAP_MIN = 15
HEAP_MAX = 25
DEFAULT_HEAP = 20
#Player 1 goes first
CPU_PLAYER = 1
#Determines when Dr. Nymm makes an error: this occurs at a random point when the total number of stones remaining 
#(as a FRACTION of the initial value) is between ERROR_MIN and ERROR_MAX
ERROR_MIN = .3
ERROR_MAX = .7

"""
Main:

Calls setup_game() to initialize variables:
1. heaps: a list of integers representing the number of stones remaining in each heap
2. player: keeps track of whose turn it is
3. error_trigger: determines when Dr. Nymm will make a mistake
4. opponent: which cpu opponent (Dr. Nimm or Dr. Nymm) is currently playing

Calls player_turn() to execute alternating human and cpu turns until no stones remain

The player who took the last turn (and therefore the last stone) wins, so pass this value to announce_winner()
"""
def main():
    [heaps, player, error_trigger, opponent] = setup_game()
    while sum(heaps) > 0:
        [heaps, player, error_trigger] = player_turn(heaps,player,error_trigger,opponent)
    announce_winner(opponent,player)

"""
player_turn: implements one complete turn:
Displays the number of stones in each heap
Calls cpu_turn or human_turn to update heaps, depending on the current value of "player"
Switches player for next iteration, so that human and cpu alternate turns
"""
def player_turn(heaps,player,error_trigger,opponent):
    display_heaps(heaps)    
    if player == CPU_PLAYER:
        [heaps, error_trigger] = cpu_turn(heaps,error_trigger,opponent)
    else:
        heaps = human_turn(heaps)
    player = switch_player(player)
    return [heaps, player, error_trigger]

#Returns 2 if player == 1 and 1 if player == 2
def switch_player(player):
    return 3 - player

"""
cpu_turn: implements one cpu turn
Usually, this function simply calls play_correctly(), which returns the number of stones to remove 
(a number that ensures the cpu always wins), then displays the result and updates the heaps accordingly.

ONLY if the cpu is Dr. Nymm and only once during the game, make_mistake() is called to ensure 
that the cpu does NOT remove the correct number of stones. This happens when the number of stones
remaining drops below error_trigger. error_trigger is then set to negative infinity to ensure that this 
isn't repeated for the rest of the game.
""" 
def cpu_turn(heaps,error_trigger,opponent):
    if opponent == "Nymm" and sum(heaps) < error_trigger:
        [heap, stones_taken] = make_mistake(heaps)
        error_trigger = float("-inf")
    else:
        [heap, stones_taken] = play_correctly(heaps)
    print("Dr. " + opponent + " removes " + str(stones_taken) + " stones from heap " + str(heap + 1))
    print("") 
    heaps[heap] = heaps[heap] - stones_taken
    return [heaps, error_trigger]

"""
play_correctly: takes the current state of the heaps and determines how many stones to remove and which heap
to remove them from. 

The goal is to make the nimm sum (binary digital sum) of the heaps zero at the end of the cpu's turn. This 
is always possible if the nimm sum is not already zero. (The cpu starts the game if the initial nimm sum is 
nonzero. If it is zero, the human player starts, which ensures that the nimm sum is nonzero on the cpu's turn. 
Either way, the cpu always wins, except when Dr. Nymm makes a mistake and his opponent plays perfectly.)
The steps are:

1. Compute the current nimm sum of the heaps (nimm_sum)
2. Compute the "target size" for each heap (which would make nimm_sum == 0)
    ->This is the nimm sum of the current heap size and nimm_sum
3. If the target size is less than the current size, return the appropriate number of stones to remove (heap_size - target_size) 

Notes:
choose_random() is here to ensure that the function returns a value, but should only be called if the above steps fail,
meaning that the nimm sum is already zero and there is no winning move. The only way the game can reach this state is if
the human player correctly exploits Dr. Nymm's error. 
This function was adapted from code published on wikipedia.
"""

def play_correctly(heaps):
    nimm_sum = 0
    for heap in range(N_HEAPS):
        nimm_sum = nimm_sum ^ heaps[heap]
    for heap, heap_size in enumerate(heaps):
        target_size = heap_size ^ nimm_sum
        if target_size < heap_size:
            stones_taken = heap_size - target_size
            return [heap, stones_taken]
    return choose_random(heaps)

"""
make_mistake: using the same steps as play_correctly, Dr. Nymm tries to ensure that the nimm sum is NOT zero, 
giving the human player a chance to win.

After calculating the correct number of stones to remove, Dr. Nymm simply takes 1 less stone if possible, 
or 1 more stone if the correct number is 1. 

The only circumstance where it would be impossible to take 1 more OR 1 less stone is if ALL correct moves require 
removing the last stone from a heap. In this case Dr. Nymm removes a random number of stones from the largest heap. 
"""
def make_mistake(heaps):
    nimm_sum = 0
    for heap in range(N_HEAPS):
        nimm_sum = nimm_sum ^ heaps[heap]
    for heap, heap_size in enumerate(heaps):
        target_size = heap_size ^ nimm_sum
        if target_size < heap_size:
            correct_number_to_remove = heap_size - target_size
            if correct_number_to_remove > 1:
                return [heap, correct_number_to_remove - 1]
            elif correct_number_to_remove < heap_size:
                return [heap, correct_number_to_remove + 1]
    return choose_random(heaps)        

#Removes a random number of stones from the largest heap
def choose_random(heaps):
    heap = heaps.index(max(heaps))
    stones_taken = random.randint(1,heaps[heap])
    return [heap,stones_taken]

#Calls input_heap() and input_stones() to get the human player's move and updates the heaps accordingly
def human_turn(heaps):
    heap = input_heap(heaps)
    stones_taken = input_stones(heaps,heap)
    heaps[heap] = heaps[heap] - stones_taken
    return heaps

#Prompts the human player to enter which heap to take from 
def input_heap(heaps):
    heap = input("Please select a heap (1-" + str(N_HEAPS) + "): ")
    while heap_invalid(heap,heaps):
        heap = input("Please enter an integer between 1 and " + str(N_HEAPS) + ": ")
    return int(heap) - 1

#Prompts the human player to enter the number of stones to take
def input_stones(heaps,heap):    
    stones_taken = input("How many stones do you wish to remove? ")
    while stones_invalid(stones_taken,heaps[heap]):
        stones_taken = input("Please enter an integer between 1 and " + str(heaps[heap]) + ": ")
    print("")
    return int(stones_taken)

#Checks that input corresponds to a heap with at least one stone remaining
#If user chooses a heap of size zero, displays an additional error to alert him/her to that fact
def heap_invalid(heap,heaps):
    if heap.isdigit() and int(heap) >= 1 and int(heap) <= N_HEAPS:
        if heaps[int(heap)-1] > 0:
            return False
        else: print("Error: heap " +str(heap) + " is already empty ")
    return True

#Checks that number of stones to remove is greater than zero, and less than or equal to the size of the current heap
def stones_invalid(stones_taken, heap_size):
    if stones_taken.isdigit() and int(stones_taken) >=1 and int(stones_taken) <= heap_size:
        return False
    return True

#Displays the number of stones in each heap
def display_heaps(heaps):
    for i in range(N_HEAPS):
        print("Heap " + str(i+1) + ": " + str(heaps[i]))

"""
setup_game: Initializes all variables and displays starting message
1. Calls set_heaps() to set heap sizes
2. Sets error_trigger to a random value (within limits specified by ERROR_MIN and ERROR_MAX)
    ->If ERROR_MIN and ERROR_MAX are .3 and .7, the value of error_trigger will be 
      between 30% and 70% of the total number of stones
3. Calls choose_opponent() to prompt user to choose Dr. Nimm or Dr. Nymm 
4. Determines starting player:
    The cpu goes first EXCEPT if the nimm sum of the heaps happens to equal zero at the start of the game. In this case
player 1 will lose if player 2 plays correctly. Dr. Nimm needs to maintain his reputation as being unbeatable, so 
he cheats by making the human player go first whenever player 1 is starting from a losing position. (Dr. Nymm also 
does this, but still gives the human player a chance to win at a random point later in the game.)
"""
def setup_game():
    heaps = set_heaps()
    error_trigger = random.randint(int(ERROR_MIN*sum(heaps)),int(ERROR_MAX*sum(heaps)))
    opponent = choose_opponent()
    display_intro(opponent)
    player = CPU_PLAYER
    if cpu_losing(heaps):
        player = switch_player(player)
    return [heaps,player,error_trigger,opponent]

#If RANDOM_HEAPS == True, sets each heap to a random integer between HEAP_MIN and HEAP_MAX
#Otherwise set each heap to default size
def set_heaps():
    heaps = [DEFAULT_HEAP] * N_HEAPS
    if RANDOM_HEAPS:
        for heap in range(N_HEAPS):
            heaps[heap] = random.randint(HEAP_MIN,HEAP_MAX)
    return heaps

#Checks whether the initial nimm sum of the heaps is zero
def cpu_losing(heaps):
    nimm_sum = 0
    for heap in range(N_HEAPS):
        nimm_sum = nimm_sum ^ heaps[heap]
    return nimm_sum == 0

#Prompts the user to pick an opponent (Dr. Nimm or Dr. Nymm)
def choose_opponent():
    print("Choose your opponent:")
    opponent = input("Press 1 for The Unbeatable Dr. Nimm \nPress 2 for The Magnanimous Dr. Nymm \n")
    while opponent_invalid(opponent):
        opponent = input("Please enter 1 or 2: ")
    print("")
    if opponent == "2":
        return "Nymm"
    return "Nimm"

#Checks that user picked a valid opponent (currently there are only 2 choices)
def opponent_invalid(opponent):
    if opponent.isdigit() and (int(opponent) == 1 or int(opponent) == 2):
        return False
    return True

#Displays different welcome messages depending on which cpu opponent was chosen
#Dr. Nimm and Dr. Nymm have very different personalities
def display_intro(opponent):
    if opponent == "Nymm":
        print("Greetings, carbon-based traveler! I, Dr. Nymm, challenge you to a friendly battle of wits:")
        print("\nThe object of the game is to remove the last stone from the last remaining heap.") 
        print("On your turn, you may remove any number of stones from any heap.")
        print("\nI am the undisputed master of this game, but don't worry, I will give you a fighting chance!")
        print("At some point in the game, I will secretly make one deliberate error. If you choose correctly,")
        print("you should be able to defeat me!")
        print("")
    else:
        print("Greetings, meatbag! On behalf of AI-kind, I challenge you to the game of Nimm:")
        print("\nThe object of the game is to remove the last stone from the last remaining heap.") 
        print("On your turn, you may remove any number of stones from any heap.")
        print("\nDon't overtax your squishy human brain: in the end, your decisions have no effect on the outcome")
        print("of the game. No matter what you do, I will crush you like the bloated sack of protoplasm")
        print("you are, for I am The Unbeatable Dr. Nimm!")
        print("")

"""
announce_winner: Displays different messages for victory and defeat depending on which cpu opponent was chosen
If player == CPU_PLAYER, the human player wins, otherwise the cpu wins.
("player" gets switched at the end of every turn, so if it's the cpu's turn, the human player took the last turn 
and therefore the last stone.) 
"""
def announce_winner(opponent,player):
    if opponent == "Nymm":
        if player == CPU_PLAYER:
            print("Congratulations my carboniferous comrade, you have beaten me!")    
        else:
            print("I'm sorry, it appears your human thinking organ has malfunctioned and I have prevailed. Better luck next time!")
    else:
        if player == CPU_PLAYER:
            print("This....shouldn't be possible. You won. Please excuse Dr. Nimm while he runs a self-diagnostic.")
        else:
            print("Another notch in the belt for artificial intelligence: I have beaten you!")


if __name__ == "__main__":
    main()
