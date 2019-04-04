import tkinter as tk

from PIL import Image, ImageTk


class View:
    DEFAULT_CASE_WIDTH = 10
    DEFAULT_CASE_LENGTH = 10

    def __init__(self, model, case_width=None, case_length=None):
        self._case_width = case_width if case_width else self.DEFAULT_CASE_WIDTH
        self._case_length = case_length if case_length else self.DEFAULT_CASE_LENGTH
        self.grid = []
        self._model = model
        self._controller = None
        self.width, self.length = self._model.get_dimensions()
        self.root = tk.Tk()
        self.root.title('Game Of Life')
        self._is_drawing_mode = False
        self._is_erasing_mode = False
        self._init_view()

    def stop(self):
        self.root.destroy()
        self._controller.stop()

    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def update(self, model):
        self._model = model
        self._update_view()

    def reset(self):
        if self._controller:
            self._controller.reset()
            self.play_and_pause.set('Play')

    def play(self):
        if self._controller:
            if self._controller.is_playing():
                self.play_and_pause.set('Play')
                self._controller.pause()
            else:
                if self._is_erasing_mode:
                    self.toggle_erasing_mode()
                    self.eraser.pack_forget()

                if self._is_drawing_mode:
                    self.toggle_draw_mode()

                self.play_and_pause.set('Pause')
                self._controller.start()

    # event handlers
    def toggle_draw_mode(self):
        self.play_and_pause.set('Play')
        self._is_drawing_mode = not self._is_drawing_mode
        if not self._is_drawing_mode:
            self.root.config(cursor='arrow')
            self.eraser.pack_forget()
        else:
            self.root.config(cursor='tcross')
            self._controller.pause()
            self.eraser.pack(padx=2)

        self._update_view()

    def toggle_erasing_mode(self):
        self._is_erasing_mode = not self._is_erasing_mode
        if self._is_erasing_mode:
            self.eraser.config(bg='pink')
        else:
            self.eraser.config(bg='white')

    def speed_up(self):
        self._controller.speed_up()

    def speed_down(self):
        self._controller.speed_down()

    def draw(self, event):
        if self._is_drawing_mode:
            i = event.widget.x
            j = event.widget.y
            self._model.game_area[i][j] = not self._is_erasing_mode
            self._update_color(i, j)

    def set_controller(self, controller):
        self._controller = controller

    # internal methods
    def _init_view(self):
        # frames
        self.main_frame = tk.Frame(self.root)
        self.separator = tk.Frame(self.root, height=10, bg='gainsboro')
        self.menu_frame = tk.Frame(self.root, height=50, bg='white')
        self.buttons_frame = tk.Frame(self.menu_frame, bg='white')
        self.edit_frame = tk.Frame(self.menu_frame, bg='white')



        # menu
        self.play_and_pause = tk.StringVar()
        self.play_and_pause.set('Pause')
        self.reset_button = tk.Button(self.buttons_frame, text='Reset', command=self.reset)
        self.play_button = tk.Button(self.buttons_frame, textvariable=self.play_and_pause, command=self.play)
        self.speed_down_button = tk.Button(self.buttons_frame, text='<<', command=self.speed_down)
        self.speed_up_button = tk.Button(self.buttons_frame, text='>>', command=self.speed_up)

        self._pencil_image = ImageTk.PhotoImage(Image.open('assets/img/pencil.jpg'))
        self.pencil = tk.Button(self.edit_frame,
                                image=self._pencil_image,
                                width='27',
                                height='20',
                                command=self.toggle_draw_mode)
        self.pencil.config(bg='white')

        self._eraser_image = ImageTk.PhotoImage(Image.open('assets/img/eraser.jpg'))
        self.eraser = tk.Button(self.edit_frame,
                                image=self._eraser_image,
                                width='23',
                                height='23',
                                command=self.toggle_erasing_mode)
        self.eraser.config(bg='white')

        # display
        self.menu_frame.pack(fill=tk.X)
        self.separator.pack(fill=tk.X)
        self.main_frame.pack()
        self.speed_down_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.speed_up_button.pack(side=tk.LEFT, padx=5)
        self.pencil.pack(side=tk.RIGHT, padx=2)
        self.edit_frame.pack(side=tk.RIGHT)
        self.buttons_frame.pack(side=tk.TOP)

        # game area
        for i in range(self.width):
            self.grid.append([])
            for j in range(self.length):
                canvas = tk.Canvas(self.main_frame,
                                   width=self._case_width,
                                   height=self._case_length,
                                   highlightthickness=0)
                canvas.grid(row=i, column=j)
                canvas.x = i
                canvas.y = j
                canvas.bind("<Button-1>", self.draw)
                self.grid[i].append(canvas)
                self._update_color(i, j)

    def _update_view(self):
        for i in range(self.width):
            for j in range(self.length):
                self._update_color(i, j)

    def _update_color(self, i, j):
        background = 'black' if self._model.game_area[i][j] else 'white'
        self.grid[i][j].configure(background=background)
