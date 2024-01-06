import tkinter as tk

def get_user_inputs():
    def on_radio_button_change():
        selected_option.set(radio_var.get())
    def on_submit_button_click():
        selected_option.set(radio_var.get())
        root.destroy()

    root = tk.Tk()
    window_width = 250
    window_height = 120
    root.geometry(f"{window_width}x{window_height}")
    root.title("Letter Boxed Puzzle Options")

    radio_var = tk.StringVar()
    selected_option = tk.StringVar()

    tk.Label(root, 
            text="""Choose a game mode:""",
            pady = 2, 
            justify = tk.LEFT,
            padx = 20).pack()

    game_modes = [
        ("Today's New York Times Puzzle", "nyt"),
        ("Custom Puzzle", "manual")
        ]
    
    for game_mode_title, game_mode in game_modes:
        tk.Radiobutton(root, 
                text=game_mode_title,
                #justify = tk.CENTER,
                indicatoron = 1,
                #width = 20,
                pady = 2, 
                padx = 100, 
                variable=radio_var, 
                command=on_radio_button_change,
                value=game_mode).pack(anchor=tk.W)
    
    # default nyt
    radio_var.set("nyt")

    submit_button = tk.Button(root, 
            text="Submit", command=on_submit_button_click)
    submit_button.pack()

    root.eval('tk::PlaceWindow . center')

    root.mainloop()

    return selected_option.get()

#print("Input 1:", get_user_inputs())