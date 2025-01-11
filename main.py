import tkinter
from tkinter import ttk as tk
from tkinter import scrolledtext as sk
from tkinter import messagebox as mes
import os
import zipfile as zf
import shutil 
import threading
import json
import translators as ts

root = tkinter.Tk()
root.geometry("500x300")
root.title("test")

log_text = sk.ScrolledText(root, wrap=tkinter.WORD, width=50,font=("consolas",10),bg = "#ffffff")
log_text.pack(side = "left",padx= 4 ,pady= 4)
log_text.config(state=tk.DISABLED)  

frame = tk.Frame(root,width=120,height=300)
frame.pack(side = "right",anchor="n",padx= 4 ,pady= 4)
 
b = tk.Button(frame, text='start',font=("consolas"),bd=1,width=30,command=lambda:threading.Thread(target=unjar).start())
b.pack(side = "top",padx= 4 ,pady= 4)

setingsbuttun = tk.Button(frame,text = "setings",font =("consolas"),bd = 1,width=30,command=lambda:settings_window())
setingsbuttun.pack(side="top",padx= 4 ,pady= 4)

translator = None
fromlanguage = "en"
tolanguage = "zh-cn"

#函数段

log_text.tag_config('yellow', foreground='#FFD701')
def cutin(str):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, "mods log: {}".format(str),"yellow")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

def logcutin(str):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, "not mods log: {}".format(str))
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

def translates(str , fromlang , tolang ,tors):
    str = ts.translate_text(str,from_language=fromlang,to_language=tolang,translator=tors)
    return str

def settings_window():
    settings = tk.Toplevel(root)
    settings.geometry("300x300")
    settings.title("settings")

    text1 = tk.Label(settings,text="translator")
    text1.pack(side="top",anchor="w")

    combobox = tk.Combobox(settings,values=["google","youdao","bing","baidu","tencent","sogou","alibabacloud"],state="readonly")
    combobox.current(2)
    combobox.pack(side="top",anchor="w")

    text1 = tk.Label(settings,text="from language")
    text1.pack(side="top",anchor="w")
    
    v = tk.StringVar()
    fromlanguage_ = tk.Entry(settings,width=20,textvariable=v)
    v.set(fromlanguage)
    fromlanguage_.pack(side="top",anchor="w")

    text1 = tk.Label(settings,text="to language")
    text1.pack(side="top",anchor="w")
    
    v2 = tk.StringVar()
    tolanguage_ = tk.Entry(settings,width=20,textvariable=v2)
    v2.set(tolanguage)
    tolanguage_.pack(side="top",anchor="w")

    def returns():
        global translator
        translator = combobox.get()
        global fromlanguage
        fromlanguage = fromlanguage_.get()
        global tolanguage
        tolanguage = tolanguage_.get()
        settings.destroy()

    set_settings = tk.Button(settings,text="change settings",width=15,command=returns)
    set_settings.pack(side="bottom",anchor="e",padx=4,pady=4)

    help_buttun = tk.Button(settings,text="helps",width=15,command=helps_window)
    help_buttun.pack(side="bottom",anchor="e",padx=4,pady=4)

def helps_window():
    helps = tk.Toplevel(root)
    helps.geometry("300x200")
    helps.title("helps")

#主程序段-----

#创建目录
if not os.path.exists("input"):
    os.makedirs("./input")
    logcutin("inputfile is created\n")
else:
    logcutin("inpurfile is found\n")

if not os.path.exists("cache"):
    os.makedirs("./cache")
    logcutin("cachefile is created\n")
else:
    logcutin("cachefile is found\n")

if not os.path.exists("output"):
    os.makedirs("./output")
    logcutin("outputfile is created\n")
else:
    logcutin("outputfile is found\n")

#查看input目录
errfile = []
if len(os.listdir("input")) == 0:
    cutin("no files found\n")
else:
    modlist = os.listdir("input")
    for i in modlist:
        if not ".jar" in i:
            errfile.append(i)
            er = 1
        else:
            
            cutin("found {}\n".format(i))
    er = 0
    if er == 1:
        mes.showerror("warning","{} is not jar file".format(errfile))
        os._exit(1)
 
#询问用户
cutin("begin now?\n")

#jar解压并翻译
def unjar():
    for num2 in range(len(modlist)):
    
        cutin("开始解压jar文件\n")
        shutil.rmtree("./cache")

        #解压
        for i in modlist:
            cutin("开始解压{}\n waiting\n".format(i))
            cutin("waiting\n")
            with zf.ZipFile("./input/{}".format(i),"r") as z:
                z.extractall("./cache")
                z.close()
            cutin("完成解压\n")

        #找json
        ls = os.listdir("./cache/assets")
        ls.append("minecraft")
        file = ls[0]
        file = "./cache/assets/"+ file + "/lang/en_us.json"
    
        with open(file , "r") as f:
            data = json.load(f)
            num2 = len(data)
            cutin(f"预计翻译{num2}个词条\n")
            num = 0
            for i1 , i2 in data.items():
            
                text = ts.translate_text(i2,from_language=fromlanguage,to_language=tolanguage,translator=translator)
                data[i1] = text
                num += 1
                cutin(f"翻译{num}个词条,剩余{num2 - num}\n")
        
            cutin(f"完成翻译{num}个词条\n")
            logcutin("开始打包文件\n")
            json.dump(data,open(f"./cache/assets/{ls[0]}/lang/zh_cn.json","w"))
        
            with zf.ZipFile("./output/{}".format(i),"w") as z:
                for root, dirs, files in os.walk("./cache"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start="./cache")
                        z.write(file_path, arcname)
            logcutin("完成打包文件\n")
    


root.mainloop()
        