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

# Based on GNU Backgammon Position ID
# https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html

import base64

BITS_IN_BYTE: int = 8

STARTING_POSITION: str = (
    "00000111110011100000111110000000000011000000011111001110000011111000000000001100"
)
ENCODED_STARTING_POSITION: str = "4HPwATDgc/ABMA"


def _swap_endian(position: str) -> str:
    return "".join(
        [
            position[i : i + BITS_IN_BYTE][::-1]
            for i in range(0, len(position), BITS_IN_BYTE)
        ]
    )


def _to_int(position: str) -> int:
    return int(position, 2)


def _to_bytes(position: str) -> bytes:
    return bytes.fromhex(str(position)[2:])


def _to_base64(position: bytes) -> bytes:
    return base64.b64encode(position)


def encode(position: str) -> str:
    position_base64: bytes = _to_base64(_to_bytes(hex(_to_int(_swap_endian(position)))))
    return position_base64[:-2].decode()


def _from_base64(position: bytes) -> bytes:
    return base64.b64decode(position)


def _from_bytes(position: bytes) -> int:
    return int.from_bytes(position, byteorder="big")


def _from_int(position: int) -> str:
    return bin(position)[2:]


def decode(position: str) -> str:
    position_base64: bytes = bytes((position + "==").encode())
    return _swap_endian(_from_int(_from_bytes(_from_base64(position_base64))))
