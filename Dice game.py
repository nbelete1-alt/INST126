import numpy as np
import os

target_score = 50
save_file = "scores.txt"

def throw_dice(num=3):
    return [int(x) for x in np.random.randint(low=1, high=7, size=num)]

def got_tuple_out(dice):
    return dice[0] == dice[1] == dice[2]

def find_locked(dice):
    locked_list = []
    for i in range(len(dice)):
        for j in range(i + 1, len(dice)):
            if dice[i] == dice[j]:
                if i not in locked_list:
                    locked_list.append(i)
                if j not in locked_list:
                    locked_list.append(j)
    return locked_list

"""AI helped me with this"""
def print_dice(dice, locked_list):
    """Shows the Dice number"""
    print("\nDice:")
    for i, val in enumerate(dice):
        if i in locked_list:
            print("[" + str(val) + "] LOCKED")
        else:
            print(f"[{val}]")

"""writes to the scires.txt"""
def write_to_file(scores, winner):
    with open(save_file, "a") as f:
        f.write("Winner: " + winner + "\n")
        for p, s in scores.items():
            f.write(p + ": " + str(s) + "\n")
        f.write("\n")

def read_old_games():
    if not os.path.exists(save_file):
        print("No old games found.")
        return
    with open(save_file, "r") as f:
        print(f.read())

"""AI helped me write this"""
def do_turn(player):
    print(f"\n{player}'s turn")
    input("Press enter to roll ")

    dice = throw_dice()
    locked_list = find_locked(dice)
    game_going = True

    while game_going:
        print_dice(dice, locked_list)
        if got_tuple_out(dice):
            print("Tuple out! 0 points.")
            return 0

        total = sum(dice)
        print("Total:", total)
        if len(locked_list) == 3:
            print("All locked. Banking " + str(total) + " points.")
            return total
        try:
            answer = input("Roll again? (y/n): ").lower()
        except EOFError:
            return total
        if answer == "n":
            return total
        elif answer == "y":
            free = []
            for i in range(3):
                if i not in locked_list:
                    free.append(i)
            new_vals = throw_dice(len(free))
            for i, v in zip(free, new_vals):
                dice[i] = v
            locked_list = find_locked(dice)
        else:
            print("Type y or n.")

"""AI helped me write this"""
def start_game():
    """Runs the whole game."""
    read_old_games()

    players = ("Player 1", "Player 2")
    scores = {p: 0 for p in players}
    round_num = 1
    game_done = False

    while not game_done:
        print(f"\n--- Round {round_num} ---")
        for player in players:
            pts = do_turn(player)
            scores[player] += pts
            print(f"{player}: {scores[player]} pts")
            if scores[player] >= target_score:
                print("\n" + player + " wins!")
                write_to_file(scores, player)
                game_done = True
                break
        round_num += 1

if __name__ == "__main__":
    start_game()