import customtkinter as ctk

root = ctk.CTk()
root.geometry("500x300")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=1, padx=100, fill="x", expand=True)

class main_window():
    def __init__(self):
        pass

if __name__ == "__main__":
    root.mainloop()