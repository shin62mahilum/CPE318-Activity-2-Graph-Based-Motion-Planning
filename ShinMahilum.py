import time
import queue
import pygame
import tkinter as tk
from tkinter import StringVar
from tkinter import OptionMenu

obs = []
counter = 0
invalids = []
repeats = []
all_pos = []
all_paths = []
all_paths2 = []


class StartingPoint():

    def __init__(self):
        self.color = (0, 255, 0)
        self.pos = [sposx, sposy]
        self.path = []

    def add_all_pos(self):
        for x1 in range(rows):
            for y1 in range(rows):
                all_pos.append([x1, y1])

    def add_inv(self):

        for x1 in range(rows):
            for y1 in range(rows):
                if x1 == 0 or y1 == 0 or x1 == rows - 1 or y1 == rows - 1:
                    invalids.append([x1, y1])

    def draw_obs(self, surface):
        for pos in obs:
            pygame.draw.rect(surface, (0, 0, 0), ((pos[0]) * dis + 1, (pos[1]) * dis + 1, dis - 1, dis - 1))
            pygame.display.flip()

    def message_display(self):
        self.root2 = tk.Tk()
        self.info = tk.Canvas(self.root2, width=300, height=40)
        self.info.pack()
        label3 = tk.Label(self.root2, text="First Click: Start Position").pack()
        self.info.create_window(150, 35, window=label3)
        label4 = tk.Label(self.root2, text="Second Click: End Position").pack()
        self.info.create_window(150, 30, window=label4)
        label5 = tk.Label(self.root2, text="Third Click: Set Obstacles").pack()
        self.info.create_window(150, 20, window=label5)
        button2 = tk.Button(text="ENTER", command=self.quit).pack()
        self.info.create_window(150, 10, window=button2)
        self.root2.mainloop()

    def invalid_pos(self):
        self.root2 = tk.Tk()
        self.info = tk.Canvas(self.root2, width=300, height=40)
        self.info.pack()
        label3 = tk.Label(self.root2, text="INVALID POSITION!").pack()
        self.info.create_window(150, 35, window=label3)
        button2 = tk.Button(text="TRY AGAIN!", command=self.quit).pack()
        self.info.create_window(150, 10, window=button2)
        self.root2.mainloop()

    def quit(self):
        self.root2.destroy()

    def def_pos(self, surface):
        self.add_inv()
        global sposx, sposy, eposx, eposy, counter
        surface.fill((255, 255, 255))
        fases = ["initial", "final", "obstacle"]
        click = False
        gridDraw(surface)
        if counter == 0:
            self.message_display()
            counter += 1
        for fase in range(2):
            corriendo = True
            while corriendo:

                pygame.init()
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        pygame.quit()
                        exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN and fases[fase] == "initial":
                        sposx, sposy = pygame.mouse.get_pos()
                        sposx = sposx // dis
                        sposy = sposy // dis

                        if [sposx, sposy] in invalids:
                            print("INSIDE THE BLACK BOX ONLY!")
                            self.invalid_pos()
                            invalids.clear()
                            obs.clear()
                            all_paths.clear()
                            main()

                        else:
                            pygame.draw.rect(surface, self.color,
                                             ((sposx) * dis + 1, (sposy) * dis + 1, dis - 1, dis - 1))
                            print("This is the initial position: ", sposx, sposy)
                            pygame.display.flip()
                            corriendo = False

                    elif event.type == pygame.MOUSEBUTTONDOWN and fases[fase] == "final":
                        eposx, eposy = pygame.mouse.get_pos()
                        eposx = eposx // dis
                        eposy = eposy // dis
                        if [eposx, eposy] in invalids:
                            print("INSIDE THE BLACK BOX ONLY!")
                            self.invalid_pos()
                            invalids.clear()
                            obs.clear()
                            all_paths.clear()
                            main()

                        elif [eposx, eposy] == [sposx, sposy]:
                            print("YOU CAN'T OVER THE INITIAL POSITION")
                            self.invalid_pos()
                            invalids.clear()
                            obs.clear()
                            all_paths.clear()
                            main()
                        else:
                            pygame.draw.rect(surface, EndPoint().color,
                                             ((eposx) * dis + 1, (eposy) * dis + 1, dis - 1, dis - 1))
                            print("This is the final position: ", eposx, eposy)
                            pygame.display.flip()
                            corriendo = False

        while len(obs) != obstacles:
            oposx, oposy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = 1

                elif event.type == pygame.MOUSEBUTTONUP:
                    click = 0

                if click == 1:
                    oposx = oposx // dis
                    oposy = oposy // dis
                    pygame.draw.rect(surface, (0, 0, 0), ((oposx) * dis + 1, (oposy) * dis + 1, dis - 1, dis - 1))
                    pygame.display.flip()

                    if [oposx, oposy] not in invalids:
                        invalids.append([oposx, oposy])
                        obs.append([oposx, oposy])

                    if [oposx, oposy] == [sposx, sposy] or [oposx, oposy] == [eposx, eposy]:
                        print("NO ENTRY OR EXIT CAN BE COVERED")
                        self.invalid_pos()
                        invalids.clear()
                        obs.clear()
                        all_paths.clear()
                        main()

                    if [sposx + 1, sposy] in invalids and [sposx, sposy + 1] in invalids and [sposx - 1,
                                                                                              sposy] in invalids and [
                        sposx, sposy - 1] in invalids:
                        print("THE CUBE IS ENCLOSED!")
                        self.invalid_pos()
                        invalids.clear()
                        obs.clear()
                        all_paths.clear()
                        main()

                    if [eposx + 1, eposy] in invalids and [eposx, eposy + 1] in invalids and [eposx - 1,
                                                                                              eposy] in invalids and [
                        eposx, eposy - 1] in invalids:
                        print("THE CUBE IS ENCLOSED")
                        self.invalid_pos()
                        invalids.clear()
                        obs.clear()
                        all_paths.clear()
                        main()

        self.move(surface)

    def draw_paths(self, surface, sum):
        self.pos = [sposx, sposy]

        # self.draw_obs(surface)

        for move in all_paths[sum]:

            if move[-1] == "L":
                self.pos[0] -= 1


            elif move[-1] == "R":
                self.pos[0] += 1


            elif move[-1] == "U":
                self.pos[1] -= 1


            elif move[-1] == "D":
                self.pos[1] += 1
            pygame.draw.rect(surface, (0, 0, 255), (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))

        pygame.draw.rect(surface, (255, 69, 0), (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))
        pygame.display.flip()

    def draw_correct_path(self, surface, right_path):
        all_paths2.clear()
        surface.fill((255, 255, 255))
        while True:
            gridDraw(surface)
            self.draw_obs(surface)
            # print(self.pos)
            self.pos = [sposx, sposy]
            # print(self.pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    invalids.clear()
                    obs.clear()
                    all_paths.clear()
                    main()

            for move in right_path[0]:
                if move == "L":
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))
                    self.pos[0] -= 1
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))


                elif move == "R":
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))
                    self.pos[0] += 1
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))


                elif move == "U":
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))
                    self.pos[1] -= 1
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))


                elif move == "D":
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))
                    self.pos[1] += 1
                    pygame.draw.rect(surface, (255, 69, 0),
                                     (self.pos[0] * dis + 1, self.pos[1] * dis + 1, dis - 1, dis - 1))

                pygame.display.flip()

    def valid_move(self, moves):

        self.pos = [sposx, sposy]

        for move in moves:
            invalids.append(self.pos.copy())
            if move == "L":
                self.pos[0] -= 1

            elif move == "R":
                self.pos[0] += 1

            elif move == "U":
                self.pos[1] -= 1

            elif move == "D":
                self.pos[1] += 1

        if self.pos in invalids or self.pos in obs:
            return False
        else:
            invalids.append(self.pos.copy())
            all_pos.append(self.pos.copy())

            return True

    def End(self, surface):
        right_path = []

        for path in all_paths2:
            self.pos = [sposx, sposy]
            for move in path:

                if move == "L":
                    self.pos[0] -= 1

                elif move == "R":
                    self.pos[0] += 1

                elif move == "U":
                    self.pos[1] -= 1

                elif move == "D":
                    self.pos[1] += 1

            if self.pos == EndPoint().pos:
                print("HERE IS THE WINNER: ", path, "WITH POSITION ", self.pos)
                right_path.append(path)
                self.draw_correct_path(surface, right_path)
            all_paths2.remove(path)

        return False

    def move(self, surface):

        nums = queue.Queue()
        nums.put("")
        add = ""
        put = ""
        sum = 0
        cor = True
        while self.End(surface) == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

            add = nums.get()
            # print(self.pos, put)
            for x in ["R", "L", "U", "D"]:
                put = add + x
                if self.valid_move(put):
                    all_paths.append(put)
                    all_paths2.append(put)

                    self.draw_paths(surface, sum)
                    nums.put(put)

                    sum += 1


class EndPoint():

    def __init__(self):
        self.color = (255, 0, 0)
        self.pos = [eposx, eposy]


def gridDraw(surface):
    positions = []

    black = []

    x = 0
    y = 0

    for i in range(rows):
        x = x + dis
        y = y + dis

        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, width))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (width, x))

    for x1 in range(rows):
        for y1 in range(rows):
            if x1 == 0 or y1 == 0 or x1 == rows - 1 or y1 == rows - 1:
                pygame.draw.rect(surface, (0, 0, 0), (x1 * dis + 1, y1 * dis + 1, dis - 1, dis - 1))

    pygame.display.flip()


def main():
    global width, rows, running, dis, sposx, sposy, eposx, eposy, oposx, oposy, obstacles
    sposx = 0
    sposy = 0
    eposx = 0
    eposy = 0
    oposx = 0
    oposy = 0

    width = 500
    # pygame.display.quit()
    dis = width // rows
    win = pygame.display.set_mode((width, width))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            else:
                StartingPoint().def_pos(win)

    pass


root = tk.Tk()
ask_display = tk.Canvas(root, width=400, height=300)
ask_display.pack()
entry1 = tk.Entry(root)
ask_display.create_window(200, 100, window=entry1)
label1 = tk.Label(root, text="Input number of grids: ")
ask_display.create_window(200, 50, window=label1)
label2 = tk.Label(root, text="Input grid size: ")
ask_display.create_window(200, 150, window=label2)


def get_input():
    global rows, obstacles
    x1 = int(entry1.get())
    x2 = variable.get()

    label2 = tk.Label(root, text="")
    ask_display.create_window(200, 250, window=label2)
    obstacles = int(x1)
    if x2 == "Small" and x1 < 29:
        rows = 12
        root.destroy()
    elif x2 == "Medium" and x1 < 150:
        rows = 20
        root.destroy()
    elif x2 == "Large" and x1 < 400:
        rows = 50
        root.destroy()
    else:
        label2 = tk.Label(root, text="Number of obstacles exceeded")
        ask_display.create_window(200, 250, window=label2)


variable = StringVar(root)
variable.set("Small")
menu = OptionMenu(root, variable, "Small", "Medium", "Large")
ask_display.create_window(200, 200, window=menu)
button1 = tk.Button(text='ENTER', command=get_input)
ask_display.create_window(200, 275, window=button1)
root.mainloop()

main()