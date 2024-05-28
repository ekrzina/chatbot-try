import tkinter as tk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import argparse

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("ChatterBot App")

        self.cBot = ChatBot(
            "Bottie",
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.BestMatch'
            ],
            database_uri='sqlite:///HRChatDB.sqlite3'
        )

        self.cTrainer = ChatterBotCorpusTrainer(self.cBot)
        self.cTrainer.train("english", './categories.yml')

        self.create_widgets()

    def create_widgets(self):
        self.chat_display = tk.Text(self.master, state=tk.DISABLED, wrap="word", height=20, width=50)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.user_input_entry = tk.Entry(self.master, width=40)
        self.user_input_entry.grid(row=1, column=0, padx=10, pady=5)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

    def send_message(self):
        user_input = self.user_input_entry.get()
        response = self.cBot.get_response(user_input)

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"Ja: {user_input}\n")

        if response.confidence >= 0.3:
            self.chat_display.insert(tk.END, f"Bottie: {response}\n")
        else:
            self.chat_display.insert(tk.END, "Bottie: Molim? Ne razumijem...\n")

        self.chat_display.config(state=tk.DISABLED)
        self.user_input_entry.delete(0, tk.END)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatterBot App je mali chatterbot namijenjen za kratke razgovore. Pokrece ga se s python3 rjesenje.py i koristi ChatterBot, chatterbot corpus, Tkinter i sqllite bazu.")
    args = parser.parse_args()

    if hasattr(args, 'help'):
        print("ChatterBot App je mali chatterbot namijenjen za kratke razgovore. Pokrece ga se s python3 rjesenje.py i koristi ChatterBot, chatterbot corpus, Tkinter i sqllite bazu.")
    else:
        root = tk.Tk()
        app = ChatApp(root)
        root.mainloop()
