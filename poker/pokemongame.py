import tkinter as tk
from tkinter import messagebox
import random

class PokemonCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Card Thrower: Pokemon Edition")
        self.root.geometry("600x500")
        self.root.configure(bg="#222222")

        # Game State
        self.player_collection = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"]
        self.computer_collection = ["Mewtwo", "Charizard", "Gengar", "Eevee"]
        
        self.player_score = 0
        self.computer_score = 0
        
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title = tk.Label(self.root, text="WALL THROW CHAMPIONSHIP", font=("Arial", 18, "bold"), fg="#FFCB05", bg="#222222")
        title.pack(pady=10)

        # Main Workspace Split
        self.main_frame = tk.Frame(self.root, bg="#222222")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # --- LEFT SIDE: CARD CANVAS CONTAINER ---
        self.canvas_frame = tk.LabelFrame(self.main_frame, text=" Digital Card Collection (Canvas) ", fg="white", bg="#333333", font=("Arial", 10, "bold"))
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=10)

        # The Empty Canvas for future card rendering
        self.card_canvas = tk.Canvas(self.canvas_frame, bg="#444444", highlightthickness=0)
        self.card_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder text on canvas
        self.card_canvas.create_text(140, 150, text="[ Empty Canvas ]\nRender Card Graphics Here", fill="#888888", justify="center", font=("Arial", 11, "italic"))

        # --- RIGHT SIDE: GAMEPLAY CONTROLS ---
        self.game_frame = tk.LabelFrame(self.main_frame, text=" Battle Zone ", fg="white", bg="#333333", font=("Arial", 10, "bold"))
        self.game_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Scoreboard
        self.score_label = tk.Label(self.game_frame, text="Score\nYou: 0  |  CPU: 0", font=("Arial", 12, "bold"), fg="#00A7E1", bg="#333333")
        self.score_label.pack(pady=15)

        # Throw Button
        self.throw_button = tk.Button(self.game_frame, text="👉 THROW CARD 👈", font=("Arial", 12, "bold"), bg="#FF0000", fg="white", activebackground="#CC0000", activeforeground="white", command=self.play_round)
        self.throw_button.pack(pady=20, ipadx=10, ipady=5)

        # Status & Results Textbox
        self.result_log = tk.Text(self.game_frame, height=10, width=30, font=("Consolas", 10), bg="#111111", fg="#00FF00", state="disabled")
        self.result_log.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_message("Hold card between index & middle finger...\nReady to throw!")

    def log_message(self, message):
        """Helper to append updates to the interactive log window."""
        self.result_log.configure(state="normal")
        self.result_log.insert(tk.END, message + "\n" + "-"*30 + "\n")
        self.result_log.see(tk.END)
        self.result_log.configure(state="disabled")

    def play_round(self):
        # Disable button briefly to mimic a turn sequence
        self.throw_button.config(state="disabled")
        
        # 1. Player throws (1-100, higher is closer to wall)
        player_roll = random.randint(1, 100)
        self.log_message(f"You flicked the card!\nDistance rating: {player_roll}/100")
        
        # 2. Computer throws after a brief simulated delay
        self.root.after(800, lambda: self.computer_turn(player_roll))

    def computer_turn(self, player_roll):
        computer_roll = random.randint(1, 100)
        self.log_message(f"CPU flicked a card!\nDistance rating: {computer_roll}/100")
        
        # 3. Determine winner of the throw
        if player_roll > computer_roll:
            self.player_score += 1
            self.log_message("🎉 YOU WIN THIS THROW! Your card landed closer to the wall.")
        elif computer_roll > player_roll:
            self.computer_score += 1
            self.log_message("❌ CPU WINS THIS THROW! Their card is closer.")
        else:
            self.log_message("🤝 IT'S A DRAW! Exactly the same distance.")
            
        # Update scoreboard
        self.score_label.config(text=f"Score\nYou: {self.player_score}  |  CPU: {self.computer_score}")
        
        # Re-enable the action button for next round
        self.throw_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = PokemonCardGame(root)
    root.mainloop()
