import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame1 = tk.Frame(self)
        tk.Label(self.frame1, text="Frame 1").pack()
        tk.Button(self.frame1, text="Go to Frame 2", command=self.show_frame2).pack()

        self.frame2 = tk.Frame(self)
        tk.Label(self.frame2, text="Frame 2").pack()
        tk.Button(self.frame2, text="Go to Frame 1", command=self.show_frame1).pack()

        self.frame1.pack()
        self.current_frame = self.frame1

    def show_frame1(self):
      self.current_frame.pack_forget()
      self.frame1.pack()
      self.current_frame = self.frame1

    def show_frame2(self):
        self.current_frame.pack_forget()
        self.frame2.pack()
        self.current_frame = self.frame2

if __name__ == "__main__":
    app = App()
    app.mainloop()