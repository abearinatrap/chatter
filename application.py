import requests, asyncio, tkinter as tk
from tkinter import ttk
import threading
import queue
import discord, io
# use while true inside async with await sleep inside to solve recursive memory leak

# bot-env\Scripts\activate.bat
# pyinstaller --onefile application.py


class Stream:
    def __init_(self,name):
        self.streamLink="https://twitch.tv/"+name
root = tk.Tk()
class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        self.frame_1 = tk.Frame(master)
        self.title_label = tk.Label(self.frame_1)
        self.title_label.config(anchor='w', text='Sample Title')
        self.title_label.pack(side='top')
        self.chat_text = tk.Text(self.frame_1)
        self.chat_text.config(height='10', relief='flat', setgrid='true', state='disabled')
        self.chat_text.config(tabstyle='tabular', undo='true', width='50')
        _text_ = ''''''
        self.chat_text.insert('0.0', _text_)
        self.chat_text.pack(side='top')
        self.frame_2 = tk.Frame(self.frame_1)
        self.channelS = ttk.Combobox(self.frame_2,values=["N/A"])
        self.channelS.pack(side="left")
        self.input_text = tk.Entry(self.frame_2)
        _text_ = '''entry_2'''
        self.input_text.delete('0', 'end')
        self.input_text.insert('0', _text_)
        self.input_text.pack(side='left')
        self.button_2 = tk.Button(self.frame_2)
        self.button_2.config(text='button_2')
        self.button_2.pack(side='right')
        self.frame_2.config(height='50', width='200')
        self.frame_2.pack(side='top')
        self.frame_1.config(height='400', width='300')
        self.frame_1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame_1
    def run(self):
        self.mainwindow.mainloop()
app = NewprojectApp(master=root)

guiq=queue.Queue()

class MyClient(discord.Client):
    async def on_ready(self):
        guiq.put({"title":"{0}".format(self.user)})
        for guild in self.guilds:
            print(guild.name)

    async def on_message(self, message):
        #print('Message from {0.author}: {0.content}'.format(message))
        guiq.put({"chid":"{0.guild}-{1.channel}".format(message,message),"author":"{0.author}".format(message),"message":"{0.content}".format(message)})
#simulated actual messages
async def makeItem():
    while True:
        guiq.put({"author":"test","message":"yo"})
        await asyncio.sleep(4)

def periodicMessageGui():
    while True:
        try:
            fn=guiq.get_nowait()
        except queue.Empty:
            break
        if fn.get("title")==None:
            app.chat_text.config(state='normal')
            app.chat_text.insert(tk.END,"\n"+fn["chid"]+" "+fn["author"]+": "+fn["message"])
            app.chat_text.config(state='disabled')
        else:
            app.title_label['text'] = fn["title"]
    root.after(1000, periodicMessageGui)
        
        
client = MyClient()
f = open("token.txt","r")
token=f.read()
f.close()
def start_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(client.run(token))
    loop.run_forever()
threading.Thread(target=start_loop, daemon=True).start()


periodicMessageGui()
app.run()
root.destroy