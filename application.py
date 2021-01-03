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
root.title("chatter discord bot")
root.resizable(False, False)
class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        
        self.frame_1 = tk.Frame(master)
        self.title_label = tk.Label(self.frame_1)
        self.title_label.config(anchor='w', text='connecting to discord .............')
        self.title_label.pack(side='top')
        self.chat_text = tk.Text(self.frame_1)
        self.chat_text.config(height='10', relief='flat', setgrid='true', state='disabled')
        self.chat_text.config(tabstyle='tabular', undo='true', width='50')
        _text_ = ''''''
        self.chat_text.insert('0.0', _text_)
        self.chat_text.pack(side='top')
        self.frame_2 = tk.Frame(self.frame_1)
        self.channelS = ttk.Combobox(self.frame_2,values=["N/A"])
        self.channelS.bind("<<ComboboxSelected>>", self.textxU)
        root.bind('<Return>', self.sendMsg)
        self.channelS.current(0)
        self.channelS.pack(side="left")
        self.textc = ttk.Combobox(self.frame_2,values=["N/A"])
        self.textc.current(0)
        self.textc.pack(side="left")
        self.input_text = tk.Entry(self.frame_2)
        _text_ = ''''''
        self.input_text.delete('0', 'end')
        self.input_text.insert('0', _text_)
        self.input_text.pack(side='left')
        self.button_2 = tk.Button(self.frame_2,command=self.sendMsg)
        self.button_2.config(text='Send')
        self.button_2.pack(side='right')
        self.frame_2.config(height='50', width='200')
        self.frame_2.pack(side='top')
        self.frame_1.config(height='400', width='300')
        self.frame_1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame_1
    def run(self):
        self.mainwindow.mainloop()

    def textxU(self,event):
        tempList=list()
        #print(self.channelS.get())
        # innefficient sort/look
        for textChat in (y for y in client.guildList if y.guild.name==self.channelS.get()):
            tempList.append(textChat.name)
        app.textc['values']=tempList
    
    def sendMsg(self,event=None):
        for textChat in (y for y in client.guildList if y.guild.name==self.channelS.get() and y.name==self.textc.get()):
            #postUrl="https://www.discord.com/channels/"+str(textChat.id)+"/messages"
            #print(postUrl)
            #dataobj={"content":self.input_text.get()}
            #await textChat.send(self.input_text.get())
            #x=requests.post(postUrl,data=dataobj)
            #print(x.text)
            
            discq.put({"channel":str(textChat.id),"content":self.input_text.get()})
            self.input_text.delete('0', 'end')
app = NewprojectApp(master=root)

guiq=queue.Queue()
discq=queue.Queue()

class MyClient(discord.Client):
    async def on_ready(self):
        self.serverList=[]
        self.guildList=[]
        self.ownName="{0}".format(self.user)
        guiq.put({"title":self.ownName})
        for guild in self.guilds:
            self.serverList.append(guild)
            tempList=list(app.channelS['values'])
            tempList.append(guild.name)
            #this works even though in different thread?? i need to read about threading
            app.channelS['values']=tempList
            for channel in guild.channels:
                if channel.type.name=="text":
                    self.guildList.append(channel)

    async def on_message(self, message):
        #global ownName
        #print('Message from {0.author}: {0.content}'.format(message))
        if "{0.author}".format(message)!=self.ownName:
            guiq.put({"chid":"{0.guild}-{1.channel}".format(message,message),"author":"{0.author}".format(message),"message":"{0.content}".format(message)})
            #await message.channel.send('👀')
#simulated actual messages
async def makeItem():
    while True:
        guiq.put({"author":"test","message":"yo"})
        await asyncio.sleep(4)

async def check_client():
    await client.wait_until_ready()
    while True:
        while True:
            try:
                msgg=discq.get_nowait()
            except queue.Empty:
                break
            for textChat in (y for y in client.guildList if str(y.id)==msgg["channel"]):
                await textChat.send(msgg["content"])
                break
        await asyncio.sleep(1) # task runs every 60 seconds

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
    client.loop.create_task(check_client())
    loop.create_task(client.run(token))
    loop.run_forever()
threading.Thread(target=start_loop, daemon=True).start()


periodicMessageGui()
app.run()
root.destroy