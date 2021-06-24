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

from backgammon import match


class TestMatch(unittest.TestCase):
    def test_swap_players(self):
        self.assertEqual(
            match.decode("cImxABAAEAAA").swap_players(), match.decode("MIGxABAAEAAA")
        )

    def test_swap_turn(self):
        self.assertEqual(
            match.decode("cImxABAAEAAA").swap_turn(), match.decode("cIGxABAAEAAA")
        )

    def test_reset_dice(self):
        self.assertEqual(
            match.decode("cImxABAAEAAA").reset_dice(), match.decode("cAmgABAAEAAA")
        )

    def test_reset_cube(self):
        self.assertEqual(
            match.decode("QYmxABAAEAAA").reset_cube(), match.decode("cImxABAAEAAA")
        )

    def test_drop_cube(self):
        self.assertEqual(
            match.decode("cBFgABAACAAA").drop_cube(), match.decode("cAFgABAAEAAA")
        )
        self.assertEqual(
            match.decode("ARlgABAAEAAA").drop_cube(), match.decode("AQxgADAAEAAA")
        )

    def test_update_score(self):
        self.assertEqual(
            match.decode("QYkqASAAIAAA").update_score(1), match.decode("QYkqASAAMAAA")
        )
        self.assertEqual(
            match.decode("MIFlABAAEAAA").update_score(3), match.decode("MIJlAEAAEAAA")
        )
        self.assertEqual(
            match.decode("MIGqACAAGAAA").update_score(2), match.decode("sIGqAEAAGAAA")
        )
        self.assertEqual(
            match.decode("QYnqACAAIAAA").update_score(1), match.decode("wYnqACAAMAAA")
        )
        self.assertEqual(
            match.decode("MIGqACAAIAAA").update_score(2), match.decode("MIGqAEAAIAAA")
        )

    def test_encode(self):
        self.assertEqual(
            match.Match(
                cube_value=2,
                cube_holder=match.Player.ZERO,
                player=match.Player.ONE,
                crawford=False,
                game_state=match.GameState.PLAYING,
                turn=match.Player.ONE,
                double=False,
                resign=match.Resign.NONE,
                dice=(5, 2),
                length=9,
                player_0_score=2,
                player_1_score=4,
            ).encode(),
            "QYkqASAAIAAA",
        )

    def test_decode(self):
        self.assertEqual(
            match.decode("QYkqASAAIAAA"),
            match.Match(
                cube_value=2,
                cube_holder=match.Player.ZERO,
                player=match.Player.ONE,
                crawford=False,
                game_state=match.GameState.PLAYING,
                turn=match.Player.ONE,
                double=False,
                resign=match.Resign.NONE,
                dice=(5, 2),
                length=9,
                player_0_score=2,
                player_1_score=4,
            ),
        )


if __name__ == "__main__":
    unittest.main()
