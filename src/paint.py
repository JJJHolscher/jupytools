#! /usr/bin/env python3
# vim:fenc=utf-8
from pathlib import Path

from ipycanvas import RoughCanvas, hold_canvas
from ipywidgets import (AppLayout, Box, Button, ColorPicker, HBox, Image,
                        IntSlider, Layout, link)

# from dnd import *


class MouseEvents:
    def __init__(self, canvas, path=None):
        self.canvas = canvas
        self.drawing = False
        self.position = None
        self.shape = []
        self.history = []
        self.path = path
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)

    def on_mouse_down(self, x, y):
        self.drawing = True
        self.position = (x, y)
        self.shape = [(x, y)]

    def on_mouse_move(self, x, y):
        if not self.drawing:
            return

        with hold_canvas():
            self.canvas.stroke_line(self.position[0], self.position[1], x, y)
            self.position = (x, y)

        self.shape.append((x, y))

    def on_mouse_up(self, _x, _y):
        self.drawing = False

        if self.path:
            self.canvas.to_file(str(self.path))

        # with hold_canvas():
        # canvas.stroke_line(position[0], position[1], x, y)
        # canvas.fill_polygon(shape)

        self.shape = []


def eraser(canvas):
    def f(_):
        canvas.stroke_style = "#000000"
        canvas.line_width = max(canvas.line_width, 5)

    return f


def paint(path=None, width=720, height=512):
    path = Path(path) if path else None
    canvas = RoughCanvas(width=width, height=height, sync_image_data=True)

    if path and path.exists():
        img = Image.from_file(path)
        canvas.draw_image(img)
    else:
        canvas.fill_style = "#000000"
        canvas.rough_fill_style = "solid"
        canvas.fill_rect(0, 0, width, height)
        canvas.rough_fill_style = "hachure"

    me = MouseEvents(canvas, path)
    canvas.on_mouse_down(me.on_mouse_down)
    canvas.on_mouse_move(me.on_mouse_move)
    canvas.on_mouse_up(me.on_mouse_up)

    canvas.stroke_style = "#749cb8"
    canvas.fill_style = "#749cb8"

    picker = ColorPicker(value="#749cb8")
    link((picker, "value"), (canvas, "stroke_style"))
    link((picker, "value"), (canvas, "fill_style"))

    eraser_button = Button(description="eraser")
    eraser_button.on_click(eraser(canvas))

    line_width_slider = IntSlider(
        value=2, min=1, max=20, step=1, description="line width"
    )
    link((line_width_slider, "value"), (canvas, "line_width"))

    canvas = Box(
        (canvas,), layout=Layout(min_height=f"{height}.px", min_width=f"{width}.px")
    )
    menu = HBox((picker, eraser_button, line_width_slider))
    return Box(
        [canvas, menu],
        layout=Layout(
            display="flex", flex_flow="column", flex_wrap="wrap", max_width="99%"
        ),
    )
