import Pyro4

uri = "PYRO:obj_4452f056e2064f1b916c65f155da26a2@localhost:54003"
game = Pyro4.Proxy(uri)

print(game.update_game())

import json, socket, ast, threading
import tkMessageBox
from common import *
from tkSimpleDialog import askstring
from Tkinter import *

class Menu():
    def __init__(self, master, nickname):
        self.nickname = nickname
        self.master = master
        self.frame = Frame(self.master)

        self.master.title(self.nickname)
        self.create_buttons()
        self.frame.pack()

    ## Setting up layout
    def create_buttons(self):
        global SERVER, PORT

        while True:
            try:
                SERVER = askstring("Enter server IP", "")
                PORT = int(askstring("Enter server PORT", ""))
                if SERVER == None or PORT == None:
                    sys.exit(0)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((SERVER, int(PORT)))
                client.close()
                break
            except Exception as e:
                tkMessageBox.showinfo("Try again", e)

        self.JOIN = Button(self.frame, command=lambda: self.handle_join_game())
        self.JOIN['text'] = 'JOIN GAME'
        self.JOIN.pack({'side': 'left'})
        self.CREATE = Button(self.frame, command=lambda: self.connect(CREATE_GAME))
        self.CREATE['text'] = 'CREATE GAME'
        self.CREATE.pack({'side': 'left'})

    ## Does a request of LIST_GAMES and then asks for user input.
    def handle_join_game(self):
        games = json.loads(self.connect(LIST_GAMES))["games"]

        while True:
            self.JOIN["state"] = DISABLED
            self.CREATE["state"] = DISABLED
            game_id = askstring("Which game do you want to join?", games)
            if game_id == None:
                self.JOIN["state"] = NORMAL
                self.CREATE["state"] = NORMAL
                return
            elif game_id in games:
                break
        new_window = Toplevel(self.master)
        new_window.protocol('WM_DELETE_WINDOW', lambda: self.handle_quit(new_window))
        game_view = GameView(new_window)

        # Starts a new thread which handles the network communication and adds messages to GUI queue for updating
        thread = threading.Thread(target=connect_to_game, args=[game_view, game_id, self.nickname])
        thread.start()

    ## Enables buttons again when window is destroyed, also tells network thread that the connection can be closed
    def handle_quit(self, context):
        global connected
        self.JOIN["state"] = NORMAL
        self.CREATE["state"] = NORMAL
        connected = False
        context.destroy()

    def connect(self, type):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))

        response = ""
        if type == CREATE_GAME:
            client.send(json.dumps({'req': CREATE_GAME}))
            response = client.recv(BUFFER_SIZE)
            assert response == DONE
        elif type == LIST_GAMES:
            client.send(json.dumps({'req': LIST_GAMES}))
            response = client.recv(BUFFER_SIZE)
        client.close()
        return response


## Game View GUI
class GameView:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.state = "0" * 81
        self.scores = {}
        self.buttons = []
        self.latest_guess = ""


        ## Setting up the 9x9 grid for sudoku
        Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 0, weight=1)
        self.frame.grid(row=0, column=0, stick=N + S + E + W)

        for row_index in range(9):
            self.buttons.append([])
            Grid.rowconfigure(self.frame, row_index, weight=1)
            for col_index in range(9):
                Grid.columnconfigure(self.frame, col_index, weight=1)
                btn = Button(self.frame, command=lambda i=(row_index, col_index): self.new_guess(i[0], i[
                    1]))
                self.buttons[row_index].append(btn)
                btn.grid(row=row_index, column=col_index, sticky=N + S + E + W)
        self.score_label = Label(self.frame)
        self.score_label.grid(row=0, column=10, columnspan=10, rowspan=10, sticky=W + E + N + S)
        self.frame.pack()
        self.periodic_update()

    ## Updates the latest_guess which is being listened by network thread
    def new_guess(self, row_index, col_index):
        print(row_index, col_index)
        current = self.buttons[row_index][col_index]["text"]
        print(current)
        if current != "0":
            return
        guess = ""
        while not (guess in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            guess = askstring("Guess", "1-9")
            if guess is None:
                return
        self.latest_guess = str(row_index) + str(col_index) + str(guess)

    ## Every 1 second the GUI is updated with latest data
    def periodic_update(self):
        for row_index in range(9):
            for col_index in range(9):
                self.buttons[row_index][col_index]["text"] = self.state[row_index * 9 + col_index]
        scores = ""
        for (k, v) in self.scores.iteritems():
            scores += k + ": " + str(v) + "\n"
        self.score_label["text"] = scores
        self.frame.after(1000, self.periodic_update)


def main():
    root = Tk()
    nickname = ""
    while (nickname == "") or (" " in nickname) or (len(nickname) > 8):
        nickname = askstring("What's your nickname?", "length <= 8 and spaces not allowed")
        if nickname is None:
            return
    app = Menu(root, nickname)
    root.mainloop()