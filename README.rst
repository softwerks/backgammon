backgammon
==========

Backgammon engine for the `Backgammon Network <https://www.bkgmn.net>`_.

Installation
------------

.. code-block:: bash

    $ pip install backgammon

Getting Started
---------------

.. code-block:: pycon

    >>> import backgammon
    >>> b = backgammon.Backgammon("4OvgATDgc+QBUA", "cInpAAAAAAAA")
    >>> print(b)
                     Position ID: 4OvgATDgc+QBUA
                     Match ID   : cInpAAAAAAAA
     +13-14-15-16-17-18------19-20-21-22-23-24-+
     | X           O  O |   | O              X |
     | X           O    |   | O                |
     | X           O    |   | O                |
     | X                |   | O                |
     |                  |   | O                |
    v|                  |BAR|                  |
     |                  |   | X                |
     | O                |   | X                |
     | O           X    |   | X                |
     | O           X    |   | X              O |
     | O  X        X    | X | X              O |
     +12-11-10--9--8--7-------6--5--4--3--2--1-+
    >>> for play in b.generate_plays():
    ...     print(play.moves)
    ...     print(play.position)
    ...
    (Move(pips=3, source=None, destination=22), Move(pips=2, source=13, destination=11))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 2, -4, 3, 0, 0, 0, -3, -1, -5, 0, 0, 1, 0, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=2, source=None, destination=23), Move(pips=3, source=24, destination=21))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 0, 1, 0, 1, 0), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=3, source=None, destination=22), Move(pips=2, source=11, destination=9))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 1, 0, 0, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 1, 0, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=3, source=None, destination=22), Move(pips=2, source=22, destination=20))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 1, 0, 0, 0, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=2, source=None, destination=23), Move(pips=3, source=13, destination=10))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 1, 1, -4, 3, 0, 0, 0, -3, -1, -5, 0, 0, 0, 1, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=2, source=None, destination=23), Move(pips=3, source=8, destination=5))
    Position(board_points=(-2, 0, 0, 0, 1, 5, 0, 2, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 0, 1, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=3, source=None, destination=22), Move(pips=2, source=24, destination=22))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 2, 0, 0), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=3, source=None, destination=22), Move(pips=2, source=6, destination=4))
    Position(board_points=(-2, 0, 0, 1, 0, 4, 0, 3, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 1, 0, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=2, source=None, destination=23), Move(pips=3, source=6, destination=3))
    Position(board_points=(-2, 0, 1, 0, 0, 4, 0, 3, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 0, 1, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=2, source=None, destination=23), Move(pips=3, source=11, destination=8))
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 0, 1, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
    (Move(pips=3, source=None, destination=22), Move(pips=2, source=8, destination=6))
    Position(board_points=(-2, 0, 0, 0, 0, 6, 0, 2, 0, 0, 1, -4, 4, 0, 0, 0, -3, -1, -5, 0, 0, 1, 0, 1), player_bar=0, player_off=1, opponent_bar=0, opponent_off=0)
