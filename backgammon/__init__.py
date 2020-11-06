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

from typing import List, Tuple

from backgammon import position

STARTING_POSITION_ID = "4HPwATDgc/ABMA"


class Backgammon:
    def __init__(self, position_id: str = STARTING_POSITION_ID):
        position_key: str = position.decode(position_id)
        self.position: List[int] = position.position_from_key(position_key)
        self.dice_owner: int = 0

    def __str__(self):
        def checkers(top: List[int], bottom: List[int]):
            combined: List[List[str]] = [
                ["   " for j in range(len(top))] for i in range(11)
            ]
            for half in (top, bottom):
                for i, checkers in enumerate(half):
                    row: int = 0 if half is top else 10
                    ascii_checker: str = " X " if checkers > 0 else " O "
                    count: int = 0
                    while count < abs(checkers):
                        if checkers > 5 and count == 4:
                            combined[row][i] = f" {checkers} "
                            break
                        else:
                            combined[row][i] = ascii_checker
                            count += 1
                            row += 1 if half is top else -1
            return combined

        def split_position(position: List[int]) -> Tuple[List[int], List[int]]:
            def invert(position: List[int]) -> List[int]:
                return list(map(lambda n: -n, position[::-1]))

            if self.dice_owner == 0:
                position = invert(position)

            half_len: int = int(len(position) / 2)
            top: List[int] = position[half_len:]
            bottom: List[int] = position[:half_len][::-1]

            return top, bottom

        board: List[List[str]] = checkers(*split_position(self.position[1:25]))
        bar: List[List[str]] = checkers(
            *split_position([self.position[25], self.position[0]])
        )

        ascii_board: str = ""
        position_id: str = position.encode(position.key_from_position(self.position))
        ascii_board += f"Position ID: {position_id}\n"
        ascii_board += " +13-14-15-16-17-18------19-20-21-22-23-24-+\n"
        for i in range(len(board)):
            ascii_board += ("^|" if self.dice_owner == 0 else "v|") if i == 5 else " |"
            ascii_board += "".join(board[i][:6])
            ascii_board += "|"
            ascii_board += "BAR" if i == 5 else bar[i][0]
            ascii_board += "|"
            ascii_board += "".join(board[i][6:])
            ascii_board += "|"
            ascii_board += "\n"
        ascii_board += " +12-11-10--9--8--7-------6--5--4--3--2--1-+\n"

        return ascii_board
