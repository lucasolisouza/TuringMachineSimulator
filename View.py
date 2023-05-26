from tkinter import *
import customtkinter


class Application:
    def __init__(self):
        self.window = customtkinter.CTk()
        self.window.geometry("400x400")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.window.title("Turing Machine Simulator")
        self.window.grid()

        self.msg = customtkinter.CTkLabel(self.window, text="Turing Machine Simulator")
        self.msg.place(x=20,y=20)

        self.Input = customtkinter.CTkEntry(self.window, placeholder_text="insert the word")
        self.Input.pack()
        self.Input.bind(self.InserirNaFita())


        self.run = customtkinter.CTkButton(self.window, text="run")
        self.run.pack(padx=10, pady=10)
        self.run.bind("<Button-1>", self.InserirNaFita)

        self.step = customtkinter.CTkButton(self.window,text="step")
        self.step.pack(padx=10, pady=10)
        self.window.mainloop()




    def InserirNaFita(self):
        msg = customtkinter.CTkLabel(self.window, text="Fita")
        msg.pack(padx=30,pady=50)
        return str(self.Input.get())


    def showTape(self):
        pass

    def showBloc(self):
        pass

    def showState(self):
        pass



