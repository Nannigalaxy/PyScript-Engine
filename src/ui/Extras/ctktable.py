# CTkTable Widget by Akascape
# License: MIT
# Author: Akash Bora

import copy

import customtkinter


class CTkTable(customtkinter.CTkFrame):
    """CTkTable Widget"""

    def __init__(
        self,
        master: any,
        row: int = None,
        column: int = None,
        padx: int = 1,
        pady: int = 0,
        width: int = 140,
        height: int = 28,
        values: list = None,
        colors: list = [None, None],
        orientation: str = "horizontal",
        color_phase: str = "horizontal",
        border_width: int = 0,
        text_color: str or tuple = None,
        border_color: str or tuple = None,
        font: tuple = None,
        header_color: str or tuple = None,
        corner_radius: int = 25,
        write: str = False,
        command=None,
        anchor: str = "center",
        hover_color: str or tuple = None,
        hover: bool = False,
        justify: str = "center",
        wraplength: int = 1000,
        **kwargs
    ):

        super().__init__(master, fg_color="transparent")

        if values is None:
            values = [[None, None], [None, None]]

        self.master = master  # parent widget
        self.rows = row if row else len(values)  # number of default rows
        self.columns = column if column else len(values[0])  # number of default columns
        self.width = width
        self.height = height
        self.padx = padx  # internal padding between the rows/columns
        self.pady = pady
        self.command = command
        self.values = values  # the default values of the table
        self.colors = colors  # colors of the table if required
        self.header_color = header_color  # specify the topmost row color
        self.phase = color_phase
        self.corner = corner_radius
        self.write = write
        self.justify = justify
        self.binded_objects = []

        if self.write:
            border_width = border_width = +1

        if hover_color is not None and hover is False:
            hover = True

        self.anchor = anchor
        self.wraplength = wraplength
        self.hover = hover
        self.border_width = border_width
        self.hover_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]
            if hover_color is None
            else hover_color
        )
        self.orient = orientation
        self.border_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["border_color"]
            if border_color is None
            else border_color
        )
        self.inside_frame = customtkinter.CTkFrame(
            self, border_width=0, fg_color="transparent"
        )
        super().configure(
            border_color=self.border_color,
            border_width=self.border_width,
            corner_radius=self.corner,
        )
        self.inside_frame.pack(
            expand=True, fill="both", padx=self.border_width, pady=self.border_width
        )

        self.text_color = (
            customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
            if text_color is None
            else text_color
        )
        self.font = font
        # if colors are None then use the default frame colors:
        self.data = {}
        self.fg_color = (
            customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
            if not self.colors[0]
            else self.colors[0]
        )
        self.fg_color2 = (
            customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"]
            if not self.colors[1]
            else self.colors[1]
        )

        if self.colors[0] is None and self.colors[1] is None:
            if self.fg_color == self.master.cget("fg_color"):
                self.fg_color = customtkinter.ThemeManager.theme["CTk"]["fg_color"]
            if self.fg_color2 == self.master.cget("fg_color"):
                self.fg_color2 = customtkinter.ThemeManager.theme["CTk"]["fg_color"]

        if not self.header_color:
            self.header_color = self.fg_color

        self.frame = {}
        self.corner_buttons = {}
        self.draw_table(**kwargs)

    def draw_table(self, **kwargs):
        """draw the table"""
        for i in range(self.rows):
            for j in range(self.columns):
                if self.phase == "horizontal":
                    fg = self.fg_color2

                if self.header_color:
                    if self.orient == "horizontal":
                        if i == 0:
                            fg = self.header_color
                    else:
                        if j == 0:
                            fg = self.header_color

                if i == 0:
                    pady = (0, self.pady)
                else:
                    pady = self.pady

                if j == 0:
                    padx = (0, self.padx)
                else:
                    padx = self.padx

                if i == self.rows - 1:
                    pady = (self.pady, 0)

                if j == self.columns - 1:
                    padx = (self.padx, 0)

                if self.values:
                    try:
                        if self.orient == "horizontal":
                            value = self.values[i][j]
                        else:
                            value = self.values[j][i]
                    except IndexError:
                        value = " "
                else:
                    value = " "

                if value == "":
                    value = " "

                if value is None:
                    value = " "
                self.frame[i, j] = customtkinter.CTkLabel(
                    self.inside_frame,
                    font=self.font,
                    text=value,
                    fg_color=fg,
                    width=self.width,
                    text_color=self.text_color,
                    anchor=self.anchor,
                )
                self.frame[i, j].grid(
                    column=j, row=i, padx=padx, pady=pady, sticky="nsew"
                )
