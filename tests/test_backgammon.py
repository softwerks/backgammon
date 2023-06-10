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

import unittest
from unittest import mock

from backgammon import backgammon
from backgammon.backgammon import Play, Move
from backgammon.position import Position


class TestBackgammon(unittest.TestCase):
    # fmt: off
    def test_enter(self):
        # -----19-20-21-22-23-24-+
        # |   | O  O  O  O  O  O |
        # |   | O  O  O  O  O  O |
        # |   |                  |
        # |BAR|      (5, 4)      |
        # | X |                  |
        self.assertEqual(
            backgammon.Backgammon("27YBAAAAACAAAA", "cInyAAAAAAAE").generate_plays(),
            [],
        )

        # -----19-20-21-22-23-24-+
        # |   | O     O  O  O  O |
        # |   | O        O  O  O |
        # |   |                  |
        # |BAR|      (5, 4)      |
        # | X |                  |
        self.assertEqual(
            sorted(backgammon.Backgammon("2zIAAAAAAAQAAA", "cInyAAAAAAAE").generate_plays()),
            [
                Play(
                    moves=(
                        Move(pips=4, source=None, destination=20),
                        Move(pips=5, source=20, destination=15),
                    ),
                    position=Position(
                        board_points=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -2, 0, 0, -2, -2, -2),
                        player_bar=0,
                        player_off=14,
                        opponent_bar=1,
                        opponent_off=6,
                    ),
                ),
                Play(
                    moves=(
                        Move(pips=5, source=None, destination=19),
                        Move(pips=4, source=19, destination=15),
                    ),
                    position=Position(
                        board_points=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -2, 0, -1, -2, -2, -2),
                        player_bar=0,
                        player_off=14,
                        opponent_bar=0,
                        opponent_off=6,
                    ),
                ),
            ],
        )

    def test_bear_off(self):
        # |      (4, 3)
        # |       X  X     O |
        # |       X  X     O |
        # --6--5--4--3--2--1-+
        self.assertEqual(
            backgammon.Backgammon("AACAYQMAAAAAAA", "cAnuAAAAAAAE").generate_plays(),
            [
                Play(
                    moves=(
                        Move(pips=4, source=3, destination=None),
                        Move(pips=3, source=2, destination=None),
                    ),
                    position=Position(
                        board_points=(-2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        player_bar=0,
                        player_off=13,
                        opponent_bar=0,
                        opponent_off=13,
                    ),
                )
            ],
        )

        # |      (4, 2)
        # |             X  O |
        # |       X     X  O |
        # --6--5--4--3--2--1-+
        self.assertEqual(
            sorted(backgammon.Backgammon("AACAMQEAAAAAAA", "cAnqAAAAAAAE").generate_plays()),
            [
                Play(
                    moves=(
                        Move(pips=2, source=3, destination=1),
                        Move(pips=4, source=1, destination=None),
                    ),
                    position=Position(
                        board_points=(-2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        player_bar=0,
                        player_off=13,
                        opponent_bar=0,
                        opponent_off=13,
                    ),
                ),
                Play(
                    moves=(
                        Move(pips=4, source=3, destination=None),
                        Move(pips=2, source=1, destination=None),
                    ),
                    position=Position(
                        board_points=(-2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        player_bar=0,
                        player_off=14,
                        opponent_bar=0,
                        opponent_off=13,
                    ),
                ),
            ],
        )

        # |      (6, 4)
        # |    X           O |
        # |    X     X     O |
        # --6--5--4--3--2--1-+
        self.assertEqual(
            backgammon.Backgammon("AACAIQMAAAAAAA", "cAnzAAAAAAAE").generate_plays(),
            [
                Play(
                    moves=(
                        Move(pips=6, source=4, destination=None),
                    ),
                    position=Position(
                        board_points=(-2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        player_bar=0,
                        player_off=13,
                        opponent_bar=0,
                        opponent_off=13,
                    ),
                )
            ],
        )

        # |      (6, 4)
        # |    X           O |
        # | X  X     X     O |
        # --6--5--4--3--2--1-+
        self.assertEqual(
            backgammon.Backgammon("AACAIQsAAAAAAA", "cAnzAAAAAAAE").generate_plays(),
            [
                Play(
                    moves=(
                        Move(pips=4, source=5, destination=1),
                        Move(pips=6, source=4, destination=None),
                    ),
                    position=Position(
                        board_points=(-2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        player_bar=0,
                        player_off=12,
                        opponent_bar=0,
                        opponent_off=13,
                    ),
                )
            ],
        )

    def test_move(self):
        # +13-14-15-16-17-18------19-20-21-22-23-24-+
        # |             O  O |   | O  O  O  O     X |
        # |             O  O |   | O  O  O  O       |
        # |                O |   | O  O             |
        # |                  |   |                  |
        # |                  |   |                  |
        # |                  |BAR|      (6, 6)      |
        # |                  |   |                X |
        # |                  |   |                X |
        # |                  |   |             X  X |
        # |                  |   |    X  X  X  X  X |
        # |                  |   |    X  X  X  X  X |
        # +12-11-10--9--8--7-------6--5--4--3--2--1-+
        self.assertEqual(
            backgammon.Backgammon("bHc3AADfbQMAIA", "cAn7AAAAAAAE").generate_plays(),
            [],
        )

        # -19-20-21-22-23-24-+
        # | O     O  X  X  X |
        # |       O  X       |
        # |          X       |
        # |      (1, 1)      |
        self.assertEqual(
            backgammon.Backgammon("mAAAAAAArgAAAA", "cInkAAAAAAAE").generate_plays(),
            [
                Play(
                    moves=(
                        Move(pips=1, source=22, destination=21),
                        Move(pips=1, source=23, destination=22),
                        Move(pips=1, source=22, destination=21),
                    ),
                    position=Position(
                        board_points=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 5, 0, 0),
                        player_bar=0,
                        player_off=10,
                        opponent_bar=0,
                        opponent_off=12,
                    ),
                )
            ],
        )

        # +13-14-15-16-17-18------19-20-21-22-23-24-+
        # | O  O     O  O  X |   |       O  O  O  X |
        # |    O     O  O    |   |       O     O    |
        # |          O       |   |       O     O    |
        # |                  |   |      (3, 2)      |
        self.assertEqual(
            sorted(backgammon.Backgammon("rsPOAgAAAAIBAA", "cImpAAAAAAAE").generate_plays()),
            [
                Play(
                    moves=(
                        Move(pips=2, source=23, destination=21),
                        Move(pips=3, source=21, destination=18),
                    ),
                    position=Position(
                        board_points=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, 0, -3, -2, 1, 1, 0, -3, 0, -3, 0),
                        player_bar=0,
                        player_off=13,
                        opponent_bar=1,
                        opponent_off=0,
                    ),
                ),
                Play(
                    moves=(
                        Move(pips=3, source=17, destination=14),
                        Move(pips=2, source=14, destination=12),
                    ),
                    position=Position(
                        board_points=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -2, 0, -3, -2, 0, 0, 0, -3, -1, -3, 1),
                        player_bar=0,
                        player_off=13,
                        opponent_bar=1,
                        opponent_off=0,
                    ),
                ),
                Play(
                    moves=(
                        Move(pips=3, source=17, destination=14),
                        Move(pips=2, source=23, destination=21),
                    ),
                    position=Position(
                        board_points=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, 1, -3, -2, 0, 0, 0, -3, 1, -3, 0),
                        player_bar=0,
                        player_off=13,
                        opponent_bar=1,
                        opponent_off=0,
                    ),
                ),
            ],
        )
    # fmt: on

    @mock.patch("random.SystemRandom.randrange", side_effect=[3, 4])
    def test_start(self, randrange_mock):
        self.assertEqual(
            backgammon.Backgammon().start().encode(), "4HPwATDgc/ABMA:cIlxAAAAAAAA"
        )

    @mock.patch("random.SystemRandom.randrange", side_effect=[3, 4])
    def test_roll(self, randrange_mock):
        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPwATDgc/ABMA", "MAAOAAAAAAAA").roll()

        self.assertEqual(backgammon.Backgammon().roll(), (3, 4))

    @mock.patch("random.SystemRandom.randrange", side_effect=[3, 3, 4, 3, 3, 4])
    def test_first_roll(self, randrange_mock):
        p0: backgammon.Backgammon = backgammon.Backgammon()
        self.assertEqual(p0.first_roll(), (4, 3))
        self.assertEqual(p0.encode(), "4HPwATDgc/ABMA:MAAOAAAAAAAA")

        p1: backgammon.Backgammon = backgammon.Backgammon()
        self.assertEqual(p1.first_roll(), (3, 4))
        self.assertEqual(p1.encode(), "4HPwATDgc/ABMA:cIgRAAAAAAAA")

    @mock.patch("random.SystemRandom.randrange", side_effect=[5, 4, 3, 4, 4, 1])
    def test_play(self, randrange_mock):
        self.assertEqual(
            backgammon.Backgammon("4NvBEQiYz+ABAw", "cAlqAAAAAAAE")
            .play(((12, 8), (12, 10)))
            .encode(),
            "mM+SAQPg28EBRA:MAFgAAAAAAAA",
        )

        self.assertEqual(
            backgammon.Backgammon("CwAAiAIAAAAAAA", "cAluAAAAAAAE")
            .play(((3, None), (2, None)))
            .encode(),
            "4HPwATDgc/ABMA:MIFyAAAACAAA",
        )

        self.assertEqual(
            backgammon.Backgammon("2+4FAEAhAAAAAA", "cAlvAAAAAAAE")
            .play(((4, None), (0, None)))
            .encode(),
            "2+4FAEAAAAAAAA:cApvAAAAGAAA",
        )

        self.assertEqual(
            backgammon.Backgammon("2+4FAAQhAAAAAA", "cAlvAAAAAAAE")
            .play(((4, None), (0, None)))
            .encode(),
            "2+4FAAQAAAAAAA:cApvAAAAGAAA",
        )

        self.assertEqual(
            backgammon.Backgammon("2+4NAAAhAAAAAA", "cAlvAAAAAAAE")
            .play(((4, None), (0, None)))
            .encode(),
            "4HPwATDgc/ABMA:8IlxAAAAEAAA",
        )

        self.assertEqual(
            backgammon.Backgammon("XwAAgAEAAAAAAA", "cIltACAAAAAA")
            .play(((0, None), (0, None)))
            .encode(),
            "4HPwATDgc/ABMA:MAFmACAACAAA",
        )

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPwATDgc/ABMA", "cAlqAAAAAAAE").play(
                ((12, 8), (19, 17))
            )

    def test_double(self):
        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPwATDgc/ABMA", "cInxABAAAAAA").double()

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "EQHgAAAAAAAA").double()

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "MBngAAAAAAAE").double()

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "MAHgAGAAKAAA").double()

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "8AmgAEAAGAAA").double()

        self.assertEqual(
            backgammon.Backgammon("0PPgATDgc+EBIg", "UQngAAAAAAAA").double().encode(),
            "0PPgATDgc+EBIg:URHgAAAAAAAA",
        )

    def test_accept_double(self):
        self.assertEqual(
            backgammon.Backgammon("4HPhASLgc/ABMA", "MBngAAAAAAAE")
            .accept_double()
            .encode(),
            "4HPhASLgc/ABMA:EQHgAAAAAAAA",
        )

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "MAHgAAAAAAAA").accept_double()

    @mock.patch("random.SystemRandom.randrange", side_effect=[3, 4])
    def test_reject_double(self, randrange_mock):
        self.assertEqual(
            backgammon.Backgammon("4HPhASLgc/ABMA", "MBngAAAAAAAE")
            .reject_double()
            .encode(),
            "4HPwATDgc/ABMA:cInxABAAAAAA",
        )

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "MAHgAAAAAAAA").reject_double()

    def test_skip(self):
        self.assertEqual(
            backgammon.Backgammon("ZgAAAAAAIAAAAA", "cAnqAAAAAAAE").skip().encode(),
            "AAAAmQEAAAAAAA:MAHgAAAAAAAA",
        )

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("MgAAAAAAEAAAAA", "cAnqAAAAAAAE").skip()

    def test_end_turn(self):
        self.assertEqual(
            backgammon.Backgammon("ywEXAIGDAQEMAA", "MIGxABAAEAAA").end_turn().encode(),
            "OBgQwJYDLgACAA:cAmgABAAEAAA",
        )

    def test_encode(self):
        self.assertEqual(
            backgammon.Backgammon("4HPwATDgc/ABMA", "cAgAAAAAAAAA").encode(),
            "4HPwATDgc/ABMA:cAgAAAAAAAAA",
        )


if __name__ == "__main__":
    unittest.main()
