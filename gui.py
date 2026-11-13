"""
gui.py
 
Sprint 2
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from game import PegSolitaire
from manual_game import ManualGame
from automated_game import AutomatedGame
from game_record import GameRecorder

class SolitaireApp:
    def __init__(self, root):
        self.root = root
        root.title('Peg Solitaire - Sprint 2')
        """Sprint 3:Replaced game with manual game"""
        self.game = ManualGame()
        self.size = tk.StringVar(value='7')
        self.kind = tk.StringVar(value='English')
        """Sprint 3 addition (Next 2 lines)"""
        self.mode = tk.StringVar(value='Manual')
        self.autoplay_job = None
        self.recorder = None
        self.recording = False
        self.replay_job = None
        self.replay_moves = []
        self.replay_index = 0
        self.selected = None
        controls = tk.Frame(root, padx=12, pady=10)
        controls.pack()
        tk.Label(controls, text='Board size (odd ≥ 5):').pack(side='left')
        tk.Entry(controls, textvariable=self.size, width=5).pack(side='left', padx=8)
        for kind in PegSolitaire.TYPES:
            tk.Radiobutton(controls, text=kind, variable=self.kind, value=kind).pack(side='left')
            """Sprint 3 addition (Game mode label)"""
        tk.Label(controls, text="game mode:").pack(
                side='left', padx=8
            )
        for mode in ("Manual", "Automated"):
                tk.Radiobutton(
                    controls,
                    text=mode,
                    variable=self.mode,
                    value=mode
                ).pack(side='left')
        tk.Button(controls, text='New Game', command=self.new_game).pack(side='left', padx=12)

        """Sprint 3 addition (Autoplay button)"""
        tk.Button(controls, text='Autoplay', command=self.start_autoplay).pack(side='left', padx=8)
        self.status = tk.StringVar(value='Select a peg, then a destination hole.')

        """Sprint 3 addition: randomize button"""
        tk.Button(controls, text='Randomize', command=self.randomize_board).pack(side='left', padx=8)

        """Sprint 3 addition (Record button)"""
        tk.Button(controls, text="Start Recording", command=self.start_recording).pack(side='left', padx=5)

        """Sprint 3 addition (Save Recoding)"""
        tk.Button(controls, text="Save recording", command=self.save_recording).pack(side='left', padx=5)

        """Sprint 3 addition (Replay button)"""
        tk.Button(controls, text="Replay game", command=self.start_replay).pack(side='left', padx=5)


        tk.Label(root, textvariable=self.status).pack()
        self.canvas = tk.Canvas(root, width=560, height=560, bg='#f8fafc', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.draw()

    """Sprint 3 addition RANDOMIZE"""
    
    def randomize_board(self):
        # Randomize only in Manual mode
        if not isinstance(self.game, ManualGame):
            self.status.set(
                "Randomize is only available in Manual mode."
            )
            return

        # Check whether the game is already over
        if self.game.is_game_over():
            self.status.set(
                "Game over! Start a new game to randomize."
            )
            return

        moves = 0

        # Perform up to 3 random valid moves
        for _ in range(3):
            available_moves = self.game.valid_moves()

            if not available_moves:
                break

            import random
            start, end = random.choice(available_moves)

            if self.game.make_move(start, end):
                moves += 1

                # Record each random move
                if self.recording and self.recorder is not None:
                    self.recorder.record_move(start, end)

        self.selected = None
        self.draw()

        if self.game.is_game_over():
            self.status.set(
                f"Game over! {self.game.rating()} "
                f"({len(self.game.pegs)} pegs remaining)"
            )
        else:
            self.status.set(
                f"Randomized using {moves} moves. "
                f"({len(self.game.pegs)} pegs remaining)"
            )

    
    def new_game(self):
        # Cancel any active replay
        if self.replay_job is not None:
            self.root.after_cancel(self.replay_job)
            self.replay_job = None

        # Cancel any active autoplay
        if self.autoplay_job is not None:
            self.root.after_cancel(self.autoplay_job)
            self.autoplay_job = None

        try:
            size = int(self.size.get())

            if self.mode.get() == "Automated":
                new_game = AutomatedGame(
                    size, self.kind.get()
                )
            else:
                new_game = ManualGame(
                    size, self.kind.get()
                )

            self.game = new_game

        except ValueError as exc:
            messagebox.showerror(
                "Invalid configuration",
                str(exc)
            )
            return

        # Reset recording for the new game
        self.recorder = None
        self.recording = False

        # Reset selected peg
        self.selected = None

        self.status.set(
            f"{self.mode.get()} game started."
        )

        self.draw()


    def start_autoplay(self):
        if self.replay_job is not None:
            self.status.set("Please wait until replay finishes.")
            return

        if not isinstance(self.game, AutomatedGame):
            self.status.set(
            'Select Automated mode and click New Game.'
            )
            return

        if self.autoplay_job is not None:
            return

        self.selected = None
        self.autoplay_step()


    def autoplay_step(self):
        self.autoplay_job = None

        if self.game.is_game_over():
            self.status.set(
            f'Game over! {self.game.rating()} '
            f'({len(self.game.pegs)} pegs remaining)')
            return

        moved = self.game.auto_move()

        if moved and self.recording and self.recorder is not None:
            start, end = self.game.last_move
            self.recorder.record_move(start, end)
        self.draw()



        self.status.set(
        f'Autoplay: {len(self.game.pegs)} pegs remaining'
    )

        self.autoplay_job = self.root.after(
        350, self.autoplay_step
    )
        
    """Sprint 3 addition RECORDING"""
    def start_recording(self):
        if self.replay_job is not None:
            self.status.set("Wait until replay finishes.")
            return

        self.recorder = GameRecorder(self.game)
        self.recording = True
        self.status.set("Recording started.")


    def save_recording(self):
        if self.recorder is None:
            messagebox.showwarning(
                "No recording",
                "Start recording before saving."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )

        if filename:
            self.recorder.save_game(filename)
            self.recording = False
            self.status.set("Recording saved successfully.")

    """Sprint 3 addition REPLAY functionality """
    def start_replay(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )

        if not filename:
            return

        try:
            data = GameRecorder.load_game(filename)

            # Validate the recording before playback
            GameRecorder.replay_game(filename)

            self.game = ManualGame(
                data["board_size"],
                data["board_type"]
            )
            self.game.pegs = {
                tuple(pos) for pos in data["initial_pegs"]
            }

            self.replay_moves = data["moves"]
            self.replay_index = 0
            self.recording = False
            self.recorder = None
            self.selected = None

            self.draw()
            self.replay_step()

        except (OSError, ValueError, KeyError, TypeError) as exc:
            messagebox.showerror("Replay error", str(exc))


    def replay_step(self):
        self.replay_job = None

        if self.replay_index >= len(self.replay_moves):
            self.status.set("Replay completed.")
            return

        move = self.replay_moves[self.replay_index]

        start = tuple(move["start"])
        end = tuple(move["end"])

        if not self.game.make_move(start, end):
            self.status.set("Replay stopped: invalid move.")
            return

        self.replay_index += 1
        self.draw()

        self.status.set(
            f"Replaying move {self.replay_index} "
            f"of {len(self.replay_moves)}"
        )

        self.replay_job = self.root.after(
            500, self.replay_step
        )


    def draw(self):
        self.canvas.delete('all')
        n = self.game.size
        step = min(65, 500 / n)
        x0 = (560-(n-1)*step)/2
        y0 = (560-(n-1)*step)/2
        for r,c in sorted(self.game.cells):
            x,y=x0+c*step,y0+r*step
            radius=step*0.38
            self.canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill='#e2e8f0',outline='#94a3b8',width=2)
            if (r,c) in self.game.pegs:
                color='#f59e0b' if (r,c)==self.selected else '#2563eb'
                self.canvas.create_oval(x-radius*.78,y-radius*.78,x+radius*.78,y+radius*.78,fill=color,outline='')
            self.canvas.create_oval(x-radius,y-radius,x+radius,y+radius,outline='',fill='',tags=(f'cell_{r}_{c}',))
            self.canvas.tag_bind(f'cell_{r}_{c}', '<Button-1>', lambda e, pos=(r,c): self.click(pos))

    def click(self, pos):
        if self.replay_job is not None:
            self.status.set("Please wait until replay finishes")
            return
        if isinstance(self.game, AutomatedGame):
            self.status.set(
                'Automated mode: use the Autoplay button.'
            )
            return
        if self.game.is_game_over():
            self.status.set('Game over! Start a new game to continue.')
            return
        if self.selected is None:
            if pos in self.game.pegs:
                self.selected = pos
                self.status.set('Select the empty destination hole.')
        else:
            if self.game.make_move(self.selected,pos):
                if self.recording and self.recorder is not None:
                    self.recorder.record_move(self.selected, pos)
                self.status.set(f'{len(self.game.pegs)} pegs remaining')
                if self.game.is_game_over():
                    rating=self.game.rating()
                    self.status.set(f'Game over! {rating} ({len(self.game.pegs)} pegs remaining)')
                    messagebox.showinfo('Game over',self.status.get())
            elif pos in self.game.pegs:
                self.selected=pos
                self.draw()
                return
            else:
                self.status.set('Invalid move. Try another peg.')
            self.selected=None
        self.draw()

if __name__=='__main__':
    root=tk.Tk()
    SolitaireApp(root)
    root.mainloop()
