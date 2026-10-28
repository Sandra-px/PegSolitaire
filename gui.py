"""
gui.py
 
Sprint 2
"""
import tkinter as tk
from tkinter import messagebox
from game import PegSolitaire

class SolitaireApp:
    def __init__(self, root):
        self.root = root
        root.title('Peg Solitaire - Sprint 2')
        self.game = PegSolitaire()
        self.size = tk.StringVar(value='7')
        self.kind = tk.StringVar(value='English')
        self.selected = None
        controls = tk.Frame(root, padx=12, pady=10)
        controls.pack()
        tk.Label(controls, text='Board size (odd ≥ 5):').pack(side='left')
        tk.Entry(controls, textvariable=self.size, width=5).pack(side='left', padx=8)
        for kind in PegSolitaire.TYPES:
            tk.Radiobutton(controls, text=kind, variable=self.kind, value=kind).pack(side='left')
        tk.Button(controls, text='New Game', command=self.new_game).pack(side='left', padx=12)
        self.status = tk.StringVar(value='Select a peg, then a destination hole.')
        tk.Label(root, textvariable=self.status).pack()
        self.canvas = tk.Canvas(root, width=560, height=560, bg='#f8fafc', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.draw()

    def new_game(self):
        try:
            size = int(self.size.get())
            self.game.new_game(size, self.kind.get())
        except ValueError as exc:
            messagebox.showerror('Invalid configuration', str(exc))
            return
        self.selected = None
        self.status.set('New game started. Select a peg, then an empty hole.')
        self.draw()

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
        if self.game.is_game_over():
            self.status.set('Game over! Start a new game to continue.')
            return
        if self.selected is None:
            if pos in self.game.pegs:
                self.selected = pos
                self.status.set('Select the empty destination hole.')
        else:
            if self.game.make_move(self.selected,pos):
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
