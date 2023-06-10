# Copyright 2020 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cmd
from typing import cast, List, Optional, Tuple

try:
    import readline
except ImportError:
    pass

from backgammon.backgammon import Backgammon, BackgammonError
from backgammon.match import GameState, Player


class BackgammonShell(cmd.Cmd):
    intro: str = "Type 'help' or '?' to list commands."
    prompt: str = "backgammon> "
    game: Backgammon

    def do_new(self, arg: str) -> None:
        """Start a new game."""
        die_1: int
        die_2: int

        if (
            hasattr(self, "game")
            and self.game.match.game_state is not GameState.NOT_STARTED
        ):
            print("Game already started.")
            return

        self.game = Backgammon()
        die_1, die_2 = self.game.first_roll()
        self.game.match.game_state = GameState.PLAYING

        print(f"Rolled {die_1} {die_2}")
        print(self.game)

    def do_move(self, arg: str) -> None:
        """Make a backgammon move: move <from> <to> ..."""
        Moves = Tuple[Tuple[Optional[int], Optional[int]], ...]

        def parse_arg(arg: str) -> Moves:
            arg_ints: List[Optional[int]] = list(
                map(lambda n: int(n) - 1 if n.isdigit() else None, arg.split())
            )

            if len(arg_ints) % 2 == 1:
                raise ValueError("Incomplete move.")
            if len(arg_ints) > 8:
                raise ValueError("Too many moves.")

            return cast(
                Moves,
                tuple(tuple(arg_ints[i : i + 2]) for i in range(0, len(arg_ints), 2)),
            )

        if (
            not hasattr(self, "game")
            or self.game.match.game_state is not GameState.PLAYING
        ):
            print("Game not in progress.")
            return

        try:
            moves: Moves = parse_arg(arg)
        except ValueError as e:
            print(e)
            return

        try:
            self.game.play(moves)
        except BackgammonError:
            print("Illegal move.")
            return

        if self.game.match.game_state is GameState.GAME_OVER:
            print(f"P{1 if self.game.match.player is Player.ZERO else 2} wins")
            print(self.game)
            del self.game
        else:
            die_1, die_2 = self.game.roll()
            print(f"Rolled {die_1} {die_2}")
            print(self.game)

    def do_quit(self, arg: str) -> bool:
        """Exit the program."""
        return True


if __name__ == "__main__":
    try:
        BackgammonShell().cmdloop()
    except KeyboardInterrupt:
        print("^C")
