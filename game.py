#This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
#If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

#Copyright (C) 2020 Mikhail Khelik, All rights reserved.

import random
import sys


class TicTacToe(object):
    def __init__(self, bot_type="X"):
        self.lines = {"horis": [["-"] * 3, ["-"] * 3, ["-"] * 3],
                      "vert": [["-"] * 3, ["-"] * 3, ["-"] * 3],
                      "diag": [["-"] * 3, ["-"] * 3]}
        if bot_type == "X":
            self.bot_type = "X"
            self.player_type = "0"
            self.turn_x = self._bot_turn
            self.turn_o = self._player_turn
        else:
            self.bot_type = "0"
            self.player_type = "X"
            self.turn_x = self._player_turn
            self.turn_o = self._bot_turn

        self.bot_turn_cnt = 0
        self.vert_lookup = {(0, 0): (0, 0), (0, 1): (1, 1), (0, 2): (2, 2), (1, 0): (2, 0), (1, 1): (1, 1),
                            (1, 2): (0, 2)}

    def _draw_board(self):
        print("- 0 1 2")
        for i in range(3):
            print(i, end=" ")
            for j in self.lines["horis"][i]:
                print(j, end=" ")
            print("")

    def _is_valid_turn(self, x, y):
        if self.lines["horis"][x][y] == "-":
            return True
        else:
            return False

    def _new_turn(self, x, y, player):

        if not self._is_valid_turn(x, y):
            return False

        self.lines["horis"][x][y] = player
        self.lines["vert"][y][x] = player

        if x == 1 and y == 1:
            self.lines["diag"][0][1] = self.lines["diag"][1][1] = player

        if x == 0 and y == 0:
            self.lines["diag"][0][0] = player

        if x == 2 and y == 2:
            self.lines["diag"][0][2] = player

        if x == 2 and y == 0:
            self.lines["diag"][1][0] = player

        if x == 0 and y == 2:
            self.lines["diag"][1][2] = player

        return True

    def _is_win(self):
        """Returns (False, None) if no one won, returns (True, X or 0) if corresponding player won"""
        for key in self.lines:
            for line in self.lines[key]:
                if line.count("X") == 3:
                    return True, "X"
                elif line.count("0") == 3:
                    return True, "0"
        return False, None

    def _is_game_over(self):
        """Returns (False, None) if game should continue, returns (True, "End of game string")"""
        res, winner = self._is_win()
        if res:
            return True, f"{winner} is Winner!!!"

        for i in range(3):
            if "-" in self.lines["horis"][i]:
                return False, None

        return True, "Draw!!!"

    def _will_win(self, player):
        """Returns (False, None) if player can't win next turn or (True, (x,y)) if can win where x,y position to win"""
        for key in self.lines:
            for line in self.lines[key]:
                if line.count(player) == 2 and "-" in line:
                    xp = self.lines[key].index(line)
                    yp = line.index("-")

                    if key == "horis":
                        return True, (xp, yp)
                    if key == "vert":
                        return True, (yp, xp)
                    if key == "diag":
                        return True, self.vert_lookup[(xp, yp)]
        return False, None

    def _bot_turn(self):
        print(f"Bot's turn {self.bot_turn_cnt}:")

        def find_1st_turn(spiller_type):
            for i in range(3):
                for j in range(3):
                    if self.lines["horis"][i][j] == spiller_type:
                        return i, j

        def find_turn():
            """ """
            winning_lines = {}
            for key in self.lines:
                for line in self.lines[key]:
                    if self.player_type not in line and "-" in line and line.count("-") >= 2:
                        if key not in winning_lines:
                            winning_lines[key] = []
                        winning_lines[key].append(self.lines[key].index(line))

            # No chance to win thus return any coordinates available
            if not winning_lines:
                for i in range(3):
                    for j in range(3):
                        if self.lines["horis"][i][j] == "-":
                            return i, j
            # Take first potential winning line
            else:
                key = list(winning_lines.keys())[0]
                x = winning_lines[key][0]
                y = self.lines[key][x].index("-")

                if key == "horis":
                    return x, y
                if key == "vert":
                    return y, x
                if key == "diag":
                    return self.vert_lookup[x, y]

        def try_to_win():
            # Will immediately if we can
            wil_win, win_turn = self._will_win(self.bot_type)
            if wil_win:
                self._new_turn(*win_turn, self.bot_type)
                return

            # Do not allow competitor to win next turn
            wil_win, win_turn = self._will_win(self.player_type)
            if wil_win:
                self._new_turn(*win_turn, self.bot_type)
                return
            self._new_turn(*find_turn(), self.bot_type)

        if self.bot_type == "X":

            if self.bot_turn_cnt == 0:
                self._new_turn(1, 1, self.bot_type)
                self.bot_turn_cnt += 1
                return

            if self.bot_turn_cnt == 1:
                corner = {(0, 0): (2, 2), (0, 2): (2, 0), (2, 0): (0, 2), (2, 2): (0, 0)}
                side = {(0, 1): (2, 2), (1, 0): (0, 2), (1, 2): (0, 0), (2, 1): (0, 0)}
                competitor = find_1st_turn("0")
                if competitor in corner:
                    turn = corner[competitor]
                else:
                    turn = side[competitor]
                self._new_turn(*turn, self.bot_type)
                self.bot_turn_cnt += 1
                return

            if self.bot_turn_cnt > 1:
                try_to_win()
                self.bot_turn_cnt += 1
                return

        # Bot is 0
        else:
            if self.bot_turn_cnt == 0:
                if self.lines["horis"][1][1] == "-":
                    self._new_turn(1, 1, self.bot_type)
                else:
                    self._new_turn(0, 0, self.bot_type)
                self.bot_turn_cnt += 1
                return

            if self.bot_turn_cnt == 1:
                wil_win, win_turn = self._will_win(self.player_type)

                # Do not allow competitor to win next turn
                if wil_win:
                    self._new_turn(*win_turn, self.bot_type)
                    self.bot_turn_cnt += 1
                    return

                # Handle special case 0
                if self.lines["horis"][1][1] == self.bot_type:
                    if self.lines["horis"][0][1] == self.player_type and self.lines["horis"][1][0] == self.player_type:
                        self._new_turn(0, 0, self.bot_type)
                        self.bot_turn_cnt += 1
                        return
                    elif self.lines["horis"][0][1] == self.player_type and self.lines["horis"][1][2] == self.player_type:
                        self._new_turn(0, 2, self.bot_type)
                        self.bot_turn_cnt += 1
                        return
                    elif self.lines["horis"][1][2] == self.player_type and self.lines["horis"][2][1] == self.player_type:
                        self._new_turn(2, 2, self.bot_type)
                        self.bot_turn_cnt += 1
                        return
                    elif self.lines["horis"][1][0] == self.player_type and self.lines["horis"][2][1] == self.player_type:
                        self._new_turn(2, 0, self.bot_type)
                        self.bot_turn_cnt += 1
                        return

                # Handle special case 1
                if self.lines["horis"][0][0] == self.bot_type and \
                   self.lines["horis"][1][1] == self.player_type and \
                   self.lines["horis"][2][2]:
                    self._new_turn(2, 0, self.bot_type)
                    self.bot_turn_cnt += 1
                    return

                try_to_win()
                self.bot_turn_cnt += 1
                return

            if self.bot_turn_cnt > 1:
                try_to_win()
                self.bot_turn_cnt += 1
                return

    def _player_turn(self):
        while True:
            x = input("Please input row for new turn [0;2]:?>")
            y = input("Please input column for new turn [0;2]:?>")
            try:
                x = int(x)
                y = int(y)
                if x > 2 or y > 2 or x < 0 or y < 0:
                    print("Integer in range [0,2] is expected, please try one more time")
                    continue
            except ValueError:
                print("Integer in range [0,2] is expected, please try one more time")
                continue

            if not self._is_valid_turn(x, y):
                print("This turn is not valid, please input other coordinates")
                continue
            else:
                break

        self._new_turn(x, y, self.player_type)
        print("Player turn:")

    def play(self):
        self._draw_board()
        while True:
            self.turn_x()
            self._draw_board()
            res, win_str = self._is_game_over()
            if res:
                break
            self.turn_o()
            self._draw_board()
            res, win_str = self._is_game_over()
            if res:
                break
        print(win_str)
        sys.exit(0)


def main():
    a = input("Please enter 1 to play for X or 2 to play for 0 or Enter for random selection:?>")

    if a == "":
        a = random.randint(1, 2)
    try:
        a = int(a)
        if a not in [1,2]:
            raise ValueError
    except ValueError:
        print("Only 1 2 or Enter are accepted")
        sys.exit(1)

    if a == 1:
        print("You will play for X")
        pc_is_x = False
    elif a == 2:
        print("You will play for 0")
        pc_is_x = True

    game = TicTacToe(bot_type="X" if pc_is_x else "0")
    game.play()


if __name__ == '__main__':
    main()
