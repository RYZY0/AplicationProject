import tkinter as tk
from tkinter import messagebox
import google.generativeai as genai


#Ai config 
#-----------------------------------------------------------------------------------
#AIzaSyA486c6xtxdaQjAjPossn1Jqa-68WOrfP0
genai.configure(api_key="AIzaSyD7Kdbf1a7GFHiVkO6pY-KkCG6_WUM9Tic")
model = genai.GenerativeModel("gemini-1.5-flash")
#-----------------------------------------------------------------------------------



#Pytania
#-----------------------------------------------------------------------------------
def diagnose():
    try:
        ip = int(entry_questions.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number")
        return

    objawy = []
    for i in range(ip):
        prompt = "Na podstawie poniższej listy już znanych objawów(jeśli żaden nie jest znany lista jest pusta), zadaj jedno-zdaniowe proste pytanie o symptom, który nie był poruszany wcześniej w żadnych zdaniach z listy, na które urzytkownik odpwie tak/nie/nie wiem): " + ", ".join(objawy)
        diagnose = model.generate_content(prompt)
        question_label.config(text=diagnose.text)
        
        root.update()
        root.wait_variable(user_response)
        
        odp = user_response.get()
        obj = diagnose.text[:-1] + odp
        
        objawy.append(obj)
        
    #print(objawy)
    res = "Na podstawie poniższej listy odpowiedzi pacjenta na pytania na temat symptomów jego dolegliwości, podaj możliwie najdokładniej, na co może dolegać pacjentowi".join(objawy)
    raport = model.generate_content(res)
    messagebox.showinfo("Diagnosis Report", raport.text)
#-----------------------------------------------------------------------------------



#Okno
#-----------------------------------------------------------------------------------
def submit_response(response):
    user_response.set(response)


root = tk.Tk()
root.title("Doktor Ai")


tk.Label(root, text="Na ile tak/nie/nie wiem pytań masz czas odpowiedzieć?").pack()
entry_questions = tk.Entry(root)
entry_questions.pack()


tk.Button(root, text="Rozpocznij Diagnozę", command=diagnose).pack()

question_label = tk.Label(root, text="")
question_label.pack()

user_response = tk.StringVar()



tk.Button(root, text="Tak", command=lambda: submit_response("tak")).pack(side=tk.LEFT)
tk.Button(root, text="Nie", command=lambda: submit_response("nie")).pack(side=tk.LEFT)
tk.Button(root, text="Nie wiem", command=lambda: submit_response("nie wiem")).pack(side=tk.LEFT)



root.mainloop()
#-----------------------------------------------------------------------------------