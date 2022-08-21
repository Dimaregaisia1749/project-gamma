import tkinter as tk

class CheatCode():
    def __init__(self, game_manager_link):
        self.game_manager_link = game_manager_link
        self.window = tk.Tk()
        self.window.title("Cheat Engine")
        self.window.resizable(width=False, height=False)
        self.frm_entry = tk.Frame(master=self.window)
        self.chips_entry = tk.Frame(master=self.window)
        self.ent_temperature = tk.Entry(master=self.frm_entry, width=10)
        self.lbl_temp = tk.Label(master=self.frm_entry, text="")
        self.ent_temperature.grid(row=0, column=0, sticky="e")
        self.lbl_temp.grid(row=0, column=1, sticky="w")

        self.btn_convert = tk.Button(
            master=self.window,
            text="начитерить чипов",
            command=self.add_money
        )
        self.frm_entry.grid(row=0, column=0, padx=10)
        self.btn_convert.grid(row=0, column=1, pady=10)
        self.window.mainloop()
    
    def add_money(self):
        self.game_manager_link.player_profile.chips += int(self.ent_temperature.get())