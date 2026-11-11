import tkinter as tk
import random

class PokemonCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Card Thrower: Pokemon Edition")
        self.root.geometry("800x550")
        self.root.configure(bg="#222222")

        # Game State
        self.player_score = 0
        self.computer_score = 0
        
        # Core Layout Constraints for Graphics
        self.start_x = 50     # Where the player stands to throw
        self.wall_x = 450     # The X coordinate of the wall line
        self.max_travel = self.wall_x - self.start_x  # Maximum physical distance a card can travel
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="WALL THROW CHAMPIONSHIP", font=("Arial", 18, "bold"), fg="#FFCB05", bg="#222222")
        title.pack(pady=10)

        # Main Layout Split
        self.main_frame = tk.Frame(self.root, bg="#222222")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # --- LEFT SIDE: THE ACTIVE GRAPHICS ARENA ---
        self.canvas_frame = tk.LabelFrame(self.main_frame, text=" Interactive Arena ", fg="white", bg="#333333", font=("Arial", 10, "bold"))
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Extended canvas width to fit the travel path cleanly
        self.card_canvas = tk.Canvas(self.canvas_frame, bg="#1a1a1a", highlightthickness=0, width=500, height=350)
        self.card_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial map rendering
        self.reset_arena_graphics()

        # --- RIGHT SIDE: CONTROLS & LOG ---
        self.game_frame = tk.LabelFrame(self.main_frame, text=" Battle Zone ", fg="white", bg="#333333", font=("Arial", 10, "bold"))
        self.game_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Scoreboard
        self.score_label = tk.Label(self.game_frame, text="Score\nYou: 0  |  CPU: 0", font=("Arial", 12, "bold"), fg="#00A7E1", bg="#333333")
        self.score_label.pack(pady=15)

        # Throw Button
        self.throw_button = tk.Button(self.game_frame, text="👉 THROW CARD 👈", font=("Arial", 12, "bold"), bg="#FF0000", fg="white", activebackground="#CC0000", activeforeground="white", command=self.play_round)
        self.throw_button.pack(pady=15, ipadx=10, ipady=5)

        # Status & Results Textbox
        self.result_log = tk.Text(self.game_frame, height=12, width=32, font=("Consolas", 10), bg="#111111", fg="#00FF00", state="disabled")
        self.result_log.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_message("Stand 10-20 feet away...\nPress Throw to flick your card!")

    def reset_arena_graphics(self):
        """Clears old cards and redraws the base environment elements."""
        self.card_canvas.delete("all")
        
        # 1. Draw the Wall (Right side boundary)
        # Using a thick grey rectangle to simulate a structural wall base
        self.card_canvas.create_rectangle(self.wall_x, 0, self.wall_x + 30, 400, fill="#555555", outline="#777777")
        self.card_canvas.create_line(self.wall_x, 0, self.wall_x, 400, fill="#FF4444", width=3) # Target Wall Line
        self.card_canvas.create_text(self.wall_x + 15, 40, text="W\nA\nL\nL", fill="white", font=("Arial", 10, "bold"))
        
        # 2. Draw the Launch Zone Line (Left side)
        self.card_canvas.create_line(self.start_x, 0, self.start_x, 400, fill="#333333", dash=(4, 4))
        self.card_canvas.create_text(self.start_x, 20, text="Flick Line", fill="#888888", font=("Arial", 8))

    def log_message(self, message):
        """Helper to append updates to the interactive log window."""
        self.result_log.configure(state="normal")
        self.result_log.insert(tk.END, message + "\n" + "-"*30 + "\n")
        self.result_log.see(tk.END)
        self.result_log.configure(state="disabled")

    def draw_card(self, throw_percentage, lane_y, color, label):
        """Calculates exact linear positioning based on 1-100 throw percentage."""
        # Convert 1-100 value to exact decimal percentage (e.g., 40 -> 0.40)
        decimal_percentage = throw_percentage / 100.0
        
        # Exact distance target from start line
        distance_traveled = self.max_travel * decimal_percentage
        
        # Map to final X coordinate on canvas
        final_x = self.start_x + distance_traveled
        
        # Dimension specifications for the miniature card asset
        card_w, card_h = 35, 50
        
        # Draw Card body
        self.card_canvas.create_rectangle(
            final_x - card_w, lane_y - card_h//2, 
            final_x, lane_y + card_h//2, 
            fill=color, outline="white", width=2
        )
        # Draw card emblem/label inside
        self.card_canvas.create_text(final_x - card_w//2, lane_y, text=label, fill="white", font=("Arial", 8, "bold"))

    def play_round(self):
        self.throw_button.config(state="disabled")
        self.reset_arena_graphics() # Wipe previous round's positions
        
        # 1. Player Throws
        player_roll = random.randint(1, 100)
        self.log_message(f"You threw your card!\nPower: {player_roll}% towards the wall.")
        
        # Render player card in upper lane (Lane Y = 100)
        self.draw_card(player_roll, 100, "#0076CE", "YOU")
        
        # 2. Delay for computer response
        self.root.after(800, lambda: self.computer_turn(player_roll))

    def computer_turn(self, player_roll):
        # Computer Throws
        computer_roll = random.randint(1, 100)
        self.log_message(f"CPU flicked their card!\nPower: {computer_roll}% towards the wall.")
        
        # Render computer card in lower lane (Lane Y = 220)
        self.draw_card(computer_roll, 220, "#C70039", "CPU")
        
        # 3. Score Evaluation
        if player_roll > computer_roll:
            self.player_score += 1
            self.log_message("🎉 YOU WIN! Your card is closer to the wall.")
        elif computer_roll > player_roll:
            self.computer_score += 1
            self.log_message("❌ CPU WINS! Their card is closer to the wall.")
        else:
            self.log_message("🤝 DRAW! Both cards landed dead even.")
            
        # Update Scoreboard display
        self.score_label.config(text=f"Score\nYou: {self.player_score}  |  CPU: {self.computer_score}")
        self.throw_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = PokemonCardGame(root)
    root.mainloop()
