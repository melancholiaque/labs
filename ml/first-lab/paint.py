import numpy as np
import os
from tkinter import (Tk, Button, Canvas,
                     SUNKEN, RAISED, ROUND, TRUE)


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.eraser_button = Button(self.root, text='eraser',
                                    command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1)

        self.commit_button = Button(self.root, text='commit',
                                    command=self.commit)
        self.commit_button.grid(row=0, column=2)

        self.c = Canvas(self.root, bg='white', width=100, height=100)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.value = None
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def commit(self):
        self.value = np.zeros(100 * 100, dtype=np.bool)
        for i in range(100):
            for j in range(100):
                self.value[i * 100 + j] = self.pixel_color(i, j)
        self.root.destroy()

    def pixel_color(self, x, y):
        ids = self.c.find_overlapping(x, y, x, y)
        if len(ids) > 0:
            index = ids[-1]
            color = self.c.itemcget(index, "fill")
            color = color.upper()
            if color != '':
                return 1
        return 0

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = 20 if self.eraser_on else 2
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    p = Paint()
    letter = input('what letter was that?\n')
    letter = letter.lower()
    if letter not in 'qwertyuiopasdfghjklzxcvbnm':
        raise Exception('wrong letter')
    if not os.path.exists(f'characters'):
        os.makedirs(f'characters')
    with open(f'characters/{letter}.txt', 'a') as fd:
        fd.write(','.join(('1' if i else '0' for i in p.value)) + '\n')
