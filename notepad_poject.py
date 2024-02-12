import tkinter as tk
import tkinter.messagebox as txt
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os
root=tk.Tk()
root.geometry("600x300")
root.title("*Untitled - Notepad")


#####---variable start from here----------#########
zoom_variable=tk.StringVar()
zoom_variable.set("100%")
font_style=["Times",12,"normal"]
status_var=tk.IntVar()
status_var.set(1)
file=None
status_line=tk.Variable()
status_line.set(f"Ln {1}, Col {1}")
for_save_or_not="\n"


#########----------frame and level start from here ------##########

#---------main menu and scrollbar packing-----#####
Mainmenu=tk.Menu(root)
scrollbar=tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT,fill="y")
####-------below is the code for status bar----######
status_frame=tk.Frame(root,height=25,relief=tk.SUNKEN,bg="#C0C0C0")
status_frame.pack(side=tk.BOTTOM,fill=tk.X) #statusbar
status_label1=tk.Label(status_frame,text="Python",bg="#C0C0C0",highlightthickness=1,highlightbackground="grey",padx=10)
status_label1.pack(fill=tk.Y,side=tk.RIGHT)
status_label3=tk.Label(status_frame,textvariable=zoom_variable,bg="#C0C0C0",highlightthickness=1,highlightbackground="grey",padx=10)
status_label3.pack(fill=tk.Y,side=tk.RIGHT)
status_label2=tk.Label(status_frame,textvariable=status_line,bg="#C0C0C0",highlightthickness=1,highlightbackground="grey",anchor=tk.W,width=15,padx=10)
status_label2.pack(fill=tk.Y,side=tk.RIGHT)
###-------text area-----------#########
text=tk.Text(root,undo=True,font=font_style)
text.pack(fill=tk.BOTH,expand=True)
text.focus()      #this line activate widget without clicking on it
# ---------scrollbar configuration------
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)


####@@@!@!!@!@##------function start from here-----------########

#---------special function----------
def curser_entry(event):
    line,column = text.index('insert').split(".")
    status_line.set(f"Ln {line}, Col {int(column)+1}")
def ask_save_notsave():
    if for_save_or_not==text.get(1.0,tk.END):
        return True
    else:
        value=txt.askyesnocancel("Notepad","Do you want to save changes?")
        if value==True:
            save()
            if for_save_or_not==text.get(1.0,tk.END):
                return True
        elif value==False:
            return True
        else:
            return False

##------file menu's function-----------------------
def new():
    global file
    root.title("Untitled - Notepad")
    file=None
    a=ask_save_notsave()
    if a==True:
        text.delete(1.0,tk.END)
def new_window():
    a=tk.Toplevel(root)
    
    
def open_file():
    global file,for_save_or_not
    text.delete("end-2c")
    a=ask_save_notsave()
    if a==True:
        file=askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        if file=="":
            file=None
        else:
            root.title(os.path.basename(file)+" - Notepad")
            text.delete(1.0,tk.END)
            with open(file) as f:
                text.insert(1.0,f.read())
            curser_entry("just for event")
            for_save_or_not=text.get(1.0,tk.END)
def save():
    global file,for_save_or_not
    print(file)
    if file==None:
        save_as()
    else:
        with open(file,"w") as f:
            f.write(text.get(1.0,tk.END))
        for_save_or_not=text.get(1.0,tk.END)
def save_as():
    global file,for_save_or_not  
    file=asksaveasfilename(initialfile='*.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if file=="":
        file=None
    else:
        with open(file,"w") as f:
            f.write(text.get(1.0,tk.END))
        for_save_or_not=text.get(1.0,tk.END)
def exit_window():
    a=ask_save_notsave()
    if a==True:
        root.destroy()
##@!@--------------edit menu's function------------------
def undo():
    text.event_generate("<<Undo>>")
def redo():
    text.event_generate("<<Redo>>")
def cut():    
    text.event_generate("<<Cut>>")
    # text.event_generate("<Control-x>")
def coppy():
    text.event_generate("<Copy>")
def paste():
    text.event_generate("<<Paste>>")
def delete():
    text.event_generate("<<Clear>>")
#!#1@!#!##!------------view menu's function--------------------
def zoom_in():
    font_style[1]=font_style[1]+2
    text.config(font=font_style)
    zoom_variable.set(f"{int(zoom_variable.get().removesuffix('%'))+5}%")
def zoom_out():
    font_style[1]=font_style[1]-2
    text.config(font=font_style)
    zoom_variable.set(f"{int(zoom_variable.get().removesuffix('%'))-5}%")
def zoom_def():
    font_style[1]=12
    text.config(font=font_style)
    zoom_variable.set('100%')
def status():
    if status_var.get()==0:
        status_frame.pack_forget()
    else:
        status_frame.pack(after=scrollbar,side=tk.BOTTOM,fill=tk.X)
#!*&#(!&----------help menu's func---------------
def help():
    txt.showwarning("About Notepad","This is just for learning perpose only.\nThe orignal 'Notepad' belongs to 'Microsoft'.")


#####---------function binding with key--------######

root.bind("<Control-n>",lambda event:new())
root.bind("<Control-o>",lambda event:open_file())
root.bind("<Control-s>",lambda event:save())
root.bind("<Control-S>",lambda event:save_as())
root.bind("<Control-+>",lambda event:zoom_in())
root.bind("<Control-minus>",lambda event:zoom_out())
root.event_add("<<boom>>",*("<KeyPress>","<Button-1>","<Motion>"))     ####--event add method---
# root.bind("<Key>",curser_entry)
# root.bind("<Button-1>",curser_entry)
root.bind('<<boom>>',curser_entry)
root.protocol("WM_DELETE_WINDOW",exit_window)      ### ---binding with close window button


########----------menus start here----------#########

####------1--file menu---------
file_menu=tk.Menu(Mainmenu,tearoff=0)
file_menu.add_command(label="New",command=new)
file_menu.add_command(label="New Window",command=new_window)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save)
file_menu.add_command(label="Save As",command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=exit_window)
Mainmenu.add_cascade(label="File",menu=file_menu)
####------2--edit menu---------
edit_menu=tk.Menu(Mainmenu,tearoff=0)
edit_menu.add_command(label="Undo",command=undo)
edit_menu.add_command(label="Redo",command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut",command=cut)
edit_menu.add_command(label="Copy",command=coppy)
edit_menu.add_command(label="Paste",command=paste)
edit_menu.add_command(label="Delete",command=delete)
Mainmenu.add_cascade(label="Edit",menu=edit_menu)
####------3--view menu---------
view_menu=tk.Menu(Mainmenu,tearoff=0)
zoom_menu=tk.Menu(Mainmenu,tearoff=0)
zoom_menu.add_command(label="Zoom In",command=zoom_in)
zoom_menu.add_command(label="Zoom Out",command=zoom_out)
zoom_menu.add_command(label="Restore Default Zoom",command=zoom_def)
view_menu.add_cascade(label="Zoom",menu=zoom_menu)
view_menu.add_checkbutton(label="Statusbar",variable=status_var,command=status)
Mainmenu.add_cascade(label="View",menu=view_menu)
####------4--fhelp menu---------
help_menu=tk.Menu(Mainmenu,tearoff=0)
help_menu.add_command(label="About Notepad",command=help)
Mainmenu.add_cascade(label="Help",menu=help_menu)


root.config(menu=Mainmenu)
root.mainloop()