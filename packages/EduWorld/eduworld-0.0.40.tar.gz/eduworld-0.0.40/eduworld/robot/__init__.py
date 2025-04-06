r"""
This package provides the following functions defined in __all__ for writing
simple procedural style programs with AlgoWorld Robots

This file is part of eduworld package

=== LICENSE INFO ===

Copyright (c) 2024 - Stanislav Grinkov

The eduworld package is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

The package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the algoworld package.
If not, see `<https://www.gnu.org/licenses/>`_.
"""

import sys
import tkinter as tk
from random import randint as rnd
from eduworld import (
    RobotApplication as Application,
    AlgoWorldBoard,
    Robot,
    RobotCanvas as Canvas,
)

app: Application = None
r: Robot = None
initialized: bool = False

_colors = [
    "red",
    "green",
    "dodgerblue",
    "orchid1",
    "firebrick",
    "orange",
    "gold2",
    "mediumpurple2",
    "slateblue2",
    "plum3",
    "tan2",
    "cyan3",
    "yellow2",
    "limegreen",
    "gray50",
    "gray30",
]
_col_max = len(_colors) - 1


def _hide_tk_err(f):
    def w(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except tk.TclError:
            sys.exit(1)

    return w


def _bind_keys():
    app.root.bind("<W>", lambda _: r.up())
    app.root.bind("<w>", lambda _: r.up())
    app.root.bind("<S>", lambda _: r.down())
    app.root.bind("<s>", lambda _: r.down())
    app.root.bind("<A>", lambda _: r.left())
    app.root.bind("<a>", lambda _: r.left())
    app.root.bind("<D>", lambda _: r.right())
    app.root.bind("<d>", lambda _: r.right())
    app.root.bind("<R>", lambda _: r.pickup())
    app.root.bind("<r>", lambda _: r.pickup())
    app.root.bind("<F>", lambda _: r.put())
    app.root.bind("<f>", lambda _: r.put())
    app.root.bind("<E>", lambda _: r.paint(_colors[rnd(0, _col_max)]))
    app.root.bind("<e>", lambda _: r.paint(_colors[rnd(0, _col_max)]))
    app.root.bind("<KP_8>", lambda _: toggle_top_wall())
    app.root.bind("<KP_6>", lambda _: toggle_right_wall())
    app.root.bind("<KP_2>", lambda _: toggle_bottom_wall())
    app.root.bind("<KP_4>", lambda _: toggle_left_wall())
    app.root.bind("<p>", lambda _: save_board())
    app.root.bind("<P>", lambda _: save_board())


def interactive_mode(world="10x10"):
    """Setup the interactive Robot application"""
    setup(world, interactive=True)


def setup(
    world: str,
    x: int = None,
    y: int = None,
    delay: float = 0.15,
    interactive: bool = False,
) -> None:
    """Setup the board and the robot"""
    global initialized
    global r
    global app
    if not initialized:
        initialized = True
        app = Application()
        canvas: Canvas = Canvas(app.root)
        board = AlgoWorldBoard(world=world)
        canvas.board = board
        app.set_canvas(canvas)
        canvas.set_draw_delay(delay)
        set_robot_pos(x, y)
        r = board.get_default_robot()
        r.on_update(lambda: canvas.redraw())
        if interactive:
            _bind_keys()
            canvas.set_draw_delay(0)
        app.run()
        if interactive:
            app.disconnect()


@_hide_tk_err
def save_board():
    global app
    board = app._canvas.board
    board.save()


@_hide_tk_err
def toggle_top_wall():
    global app
    board = app._canvas.board
    board.toggle_top_wall()
    app._canvas.redraw()


@_hide_tk_err
def toggle_right_wall():
    global app
    board = app._canvas.board
    board.toggle_right_wall()
    app._canvas.redraw()


@_hide_tk_err
def toggle_bottom_wall():
    global app
    board = app._canvas.board
    board.toggle_bottom_wall()
    app._canvas.redraw()


@_hide_tk_err
def toggle_left_wall():
    global app
    board = app._canvas.board
    board.toggle_left_wall()
    app._canvas.redraw()


@_hide_tk_err
def set_robot_pos(x, y):
    """Set Robot position on board"""
    global app
    board = app._canvas.board
    r = board.get_default_robot()
    if x is not None:
        r.x = max(1, x)
    if y is not None:
        r.y = max(1, y)


def disconnect() -> None:
    """Shut down the app"""
    print(r.get_steps())
    app.disconnect()


def shutdown(keep_window: bool = False) -> None:
    """Shut down the app"""
    print(r.get_steps())
    app.shutdown(keep_window)


@_hide_tk_err
def up() -> None:
    """Move default robot up"""
    r.up()


@_hide_tk_err
def down() -> None:
    """Move default robot down"""
    r.down()


@_hide_tk_err
def left() -> None:
    """Move default robot left"""
    r.left()


@_hide_tk_err
def right() -> None:
    """Move default robot right"""
    r.right()


@_hide_tk_err
def put() -> None:
    """Put beeper down"""
    r.put()


@_hide_tk_err
def pickup() -> None:
    """Pickup beeper"""
    r.pickup()


@_hide_tk_err
def paint(color: str = "tan2") -> None:
    """Paint tile with color"""
    r.paint(color=color)


def has_beepers() -> bool:
    """Test if robot has beepers"""
    return r.has_beepers()


def next_to_beeper() -> bool:
    """Test if tile the robot on has beepers"""
    return r.next_to_beeper()


def tile_is_painted() -> bool:
    """Test whether tile is painted or not"""
    return r.tile_is_painted()


def tile_color() -> str:
    """Return tile color"""
    return r.tile_color()


def tile_radiation() -> float:
    """Return tile radiation"""
    return r.tile_radiation()


def tile_temperature() -> float:
    """Return tile temperature"""
    return r.tile_temperature()


def up_is_wall() -> bool:
    """Test if up of robot is wall"""
    return r.up_is_wall()


def down_is_wall() -> bool:
    """Test if down of robot is wall"""
    return r.down_is_wall()


def left_is_wall() -> bool:
    """Test if left of robot is wall"""
    return r.left_is_wall()


def right_is_wall() -> bool:
    """Test if right of robot is wall"""
    return r.right_is_wall()


def up_is_free() -> bool:
    """Test if up of robot is free cell"""
    return not r.up_is_wall()


def down_is_free() -> bool:
    """Test if down of robot is free cell"""
    return not r.down_is_wall()


def left_is_free() -> bool:
    """Test if left of robot is free cell"""
    return not r.left_is_wall()


def right_is_free() -> bool:
    """Test if right of robot is free cell"""
    return not r.right_is_wall()


def get_steps():
    return r.get_steps()


__all__ = [
    # setup
    "setup",
    "shutdown",
    "set_robot_pos",
    "disconnect",
    "interactive_mode",
    # movement
    "up",
    "down",
    "left",
    "right",
    # check movement
    "up_is_free",
    "down_is_free",
    "left_is_free",
    "right_is_free",
    "up_is_wall",
    "down_is_wall",
    "left_is_wall",
    "right_is_wall",
    # color paint
    "tile_is_painted",
    "tile_color",
    "paint",
    # beepers
    "put",
    "pickup",
    "has_beepers",
    "next_to_beeper",
    # other sensors
    "tile_radiation",
    "tile_temperature",
    "get_steps",
]
