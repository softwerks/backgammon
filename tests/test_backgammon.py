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


class TestBackgammon(unittest.TestCase):
    def test_generate_plays(self):
        pass

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

    def test_play(self):
        pass

    def test_double(self):
        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPwATDgc/ABMA", "cInxABAAAAAA").double()

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "EQHgAAAAAAAA").double()

        with self.assertRaises(backgammon.BackgammonError):
            backgammon.Backgammon("4HPhASLgc/ABMA", "MBngAAAAAAAE").double()

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
