# Copyright 2021 Softwerks LLC
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

from typing import Tuple
import unittest

from backgammon import position


class TestPosition(unittest.TestCase):
    def test_enter(self):
        # ----19-20-21-22-23-24-+
        # |BAR| O  O  O     O  O |
        # | X | O  O  O     O  O |
        pos: position.Position = position.decode("m20AAAAAAAgAAA")
        self.assertEqual(pos.enter(3), (position.decode("m20AAAAAAAEAAA"), 21))
        self.assertEqual(pos.enter(2), (None, None))

    def test_player_home(self):
        # |             X    |
        # |    X        X  O |
        # | X  X  O     X  O |
        # --6--5--4--3--2--1-+
        pos: position.Position = position.decode("AAAQ41gAAAAAAA")
        self.assertEqual(pos.player_home(), (0, 3, 0, 0, 2, 1))

    def test_off(self):
        # |             X  O |
        # |    X  X     X  O |
        # --6--5--4--3--2--1-+
        pos: position.Position = position.decode("AACAMQUAAAAAAA")
        self.assertEqual(pos.off(1, 2), (position.decode("AACAkQIAAAAAAA"), None))
        self.assertEqual(pos.off(3, 4), (position.decode("AACAMQIAAAAAAA"), None))
        self.assertEqual(pos.off(4, 6), (position.decode("AACAMQEAAAAAAA"), None))
        self.assertEqual(pos.off(3, 2), (position.decode("AACAcQQAAAAAAA"), 1))
        self.assertEqual(pos.off(3, 6), (None, None))

    def test_move(self):
        # -19-20-21-22-23-24-+
        # | O     O  O  O  X |
        # | O        O  O    |
        pos: position.Position = position.decode("tgwAAAAAgAAAAA")
        self.assertEqual(pos.move(23, 3), (position.decode("NgYAQAAAEAAAAA"), 20))
        self.assertEqual(pos.move(23, 4), (position.decode("tgwAAAAACAAAAA"), 19))
        self.assertEqual(pos.move(23, 5), (None, None))

    def test_apply_move(self):
        # -----19-20-21-22-23-24-+
        # |BAR|    X        O  O |
        # | X |                O |
        pos: position.Position = position.decode("CwAAAACAIAAAAA")
        self.assertEqual(pos.apply_move(None, 22), position.decode("AwAABACACAAAAA"))
        self.assertEqual(pos.apply_move(None, 21), position.decode("CwAAAACABAAAAA"))
        self.assertEqual(pos.apply_move(None, 19), position.decode("CwAAAACAAQAAAA"))
        # | X        O       |
        # | X        O  O  X |
        # --6--5--4--3--2--1-+
        pos: position.Position = position.decode("AABgEQwAAAAAAA")
        self.assertEqual(pos.apply_move(5, 3), position.decode("AABgEQkAAAAAAA"))
        self.assertEqual(pos.apply_move(5, 1), position.decode("AABgVAgAAAAAAA"))
        self.assertEqual(pos.apply_move(5, 0), position.decode("AABgMQgAAAAAAA"))
        self.assertEqual(pos.apply_move(5, None), position.decode("AABgEQQAAAAAAA"))

    def test_swap_players(self):
        # +13-14-15-16-17-18------19-20-21-22-23-24-+
        # | O  O     X       |   |       O     O  O |
        # |    O             |   |       O        O |
        # |    O             |   |       O          |
        # |                  |   |                  |
        # |                  |BAR|       X          |
        # |          X       | X |       X          |
        # |          X       | X |       X     O    |
        # +12-11-10--9--8--7-------6--5--4--3--2--1-+
        pos: position.Position = position.decode("ywEXAIGDAQEMAA")
        self.assertEqual(pos.swap_players(), position.decode("OBgQwJYDLgACAA"))

    # fmt: off

    def test_encode(self):
        pos: position.Position = position.Position(
            board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2),
            player_bar=0,
            player_off=0,
            opponent_bar=0,
            opponent_off=0,
        )
        self.assertEqual(pos.encode(), "4HPwATDgc/ABMA")

    def test_unmerge_points(self):
        player: Tuple[int, ...]
        opponent: Tuple[int, ...]

        board_points: Tuple[int, ...] = (-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2)
        player, opponent = position._unmerge_points(board_points)

        self.assertEqual(
            player,
            (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
        )
        self.assertEqual(
            opponent,
            (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
        )

    def test_key_from_checkers(self):
        unmerged_points: Tuple[int, ...] = (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2)
        bar: Tuple[int, ...] = (0,)

        self.assertEqual(
            position._key_from_checkers(unmerged_points + bar + unmerged_points + bar),
            "00000111110011100000111110000000000011000000011111001110000011111000000000001100",
        )

    def test_id_from_key(self):
        self.assertEqual(
            position._id_from_key(
                "00000111110011100000111110000000000011000000011111001110000011111000000000001100"
            ),
            "4HPwATDgc/ABMA",
        )

    def test_decode(self):
        self.assertEqual(
            position.decode("4HPwATDgc/ABMA"),
            position.Position(
                board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2),
                player_bar=0,
                player_off=0,
                opponent_bar=0,
                opponent_off=0,
            ),
        )

    def test_key_from_id(self):
        self.assertEqual(
            position._key_from_id("4HPwATDgc/ABMA"),
            "00000111110011100000111110000000000011000000011111001110000011111000000000001100",
        )

    def test_checkers_from_key(self):
        self.assertEqual(
            position._checkers_from_key(
                "00000111110011100000111110000000000011000000011111001110000011111000000000001100"
            ),
            (
                0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                0,
                0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                0,
            ),
        )

    def test_merge_points(self):
        self.assertEqual(
            position._merge_points(
                (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
                (0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
            ),
            (-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2),
        )

    # fmt: on


if __name__ == "__main__":
    unittest.main()
