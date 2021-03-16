from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from pathlib import Path
from tkfontchooser import askfont

class app():
    
    def attachProperties(self):

        '''for child in self.container.winfo_children():
            child.destroy()
        self.container.destroy()'''

        self.propertiesWindow.destroy()
        self.detach.place(x=640,y=150)

        self.container = Frame(self.janela,bg = '#242526',highlightbackground="#FFFFFF",highlightthickness=1)
        self.container.place(x=500,y=180,height=210,width=197) #coloca na janela

        canvas = Canvas(self.container,bg = '#242526')
        canvas.place(x=0,y=0,height=210,width=180) #canvas para controle y dentro do container

        scrollbar = Scrollbar(self.container, orient="vertical", command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") #criando a scroll bar dentro do container

        self.FrameProperties = Frame(canvas,bg = '#242526') #frame dentro do canvas q vai ter todas propriedades

        self.FrameProperties.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.FrameProperties, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set) #define a scrollbar como a pos y do canvas

        self.listboxCall(event=None)
        



    def propertyDetach(self):
            
        for child in self.container.winfo_children():
            child.destroy()

        self.container.destroy()

        self.detach.place_forget()
            
        self.propertiesWindow = Tk()

        screen_width = self.propertiesWindow.winfo_screenwidth()
        screen_height = self.propertiesWindow.winfo_screenheight()

        screen_width = str(screen_width - 200)
        screen_height = '0'

        self.propertiesWindow.geometry("200x500+" +screen_width + '+' + screen_height)

        self.container = Frame(self.propertiesWindow,bg = '#242526',highlightbackground="#FFFFFF",highlightthickness=1)
        self.container.place(x=0,y=0,width=197,height=500) #coloca na janela

        canvas = Canvas(self.container,bg = '#242526')
        canvas.place(x=0,y=0,height=500,width=180) #canvas para controle y dentro do container

        scrollbar = Scrollbar(self.container, orient="vertical", command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") #criando a scroll bar dentro do container

        self.FrameProperties = Frame(canvas,bg = '#242526') #frame dentro do canvas q vai ter todas propriedades

        self.FrameProperties.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.FrameProperties, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set) #define a scrollbar como a pos y do canvas

        self.propertiesWindow.protocol("WM_DELETE_WINDOW", self.attachProperties)

        self.listboxCall(event=None)





    def getObjectsExport(self):

        code = """from tkinter import * 

class app():
    def __init__(self):
        self.root = Tk()
        """

        frameL = self.frameDesigner.winfo_width()
        frameA = self.frameDesigner.winfo_height()
        framesize = "self.root.geometry('" + str(frameL) + "x" + str(frameA) + "')\n\n\t\t#init Objects"

        code = code + framesize


        count = 0
        lista = self.listObjectsGUI.get(0,END)
        size = len(lista)

        while count < size: #pega todas as propriedades de todos objetos na tela
            widget = lista[count]
            print(widget)

            type = self.objs[widget].winfo_class() 
        
            string = type+ "(self.root,"

            x = self.objs[widget].winfo_rootx() - self.frameDesigner.winfo_rootx()
            y = self.objs[widget].winfo_rooty() - self.frameDesigner.winfo_rooty()


            for property in self.objs[widget].keys():
                
                value = self.objs[widget].cget(property)
                string = string + property + '=' +  "'" + str(value) + "'" + ','

            
            string = "        " + widget + " = " + string[:-1] + ')' + ".place(x=" + str(x) + ',y=' + str(y) + ')' 
            

            code = code + "\n" + string

            count = count + 1

        code = code + "\n\t\t#close Objects\n\n" + "        self.root.mainloop()"
        code = code + "\napp = app()"


        try:
            file = open(self.homeDir + "/Desktop/code.py", "w")
            n = file.write(code)
            file.close()
        except:
            pass

        exec(code)


        #print(code)


    

    def openProject(self):
        path = askopenfilename()

        f = open(path, "r")
        f.read()


    def openCommand(self):
        
        self.createScriptBox()
        pass


    def deleteComponent(self):
        self.objs[self.objectSelected].destroy()

       
        index = self.listObjectsGUI.get(0, END).index(self.objectSelected)
        self.listObjectsGUI.delete(index)


    def deletePropertys(self):
        count = 0
        size = len(self.propertys)

        print(size)

        while size > count:
            x = list(self.propertys.keys())[count]

            try:
                self.propertys[x].destroy()
            except:
                pass

            print(x)

            count = count + 1


    def apply(self):

        count = 0
        size = len(self.propertys)

        print(size)

        while size > count:
            x = list(self.propertys.keys())[count]

            try:
                get = self.propertys[x].get()
                config = {}

                x = x.split("Entry")[1]

               


                config[x] = get
                
                print(config)

                self.objs[self.objectSelected].config(config)

                #print(get)
            except:
                pass


            count = count + 1

    #def createFuncButton(self):

    def addScriptToWidget(self):
        
        script = self.script.get('1.0', 'end-1c')

        self.objScripts[self.objectSelected] = script


    def createScriptBox(self,property):
        scripter = Tk()

        scripter.geometry("600x430")

        self.script = Text(scripter)
        self.script.pack()

        try:
            scriptExistent = self.objScripts[self.objectSelected]
            self.script.insert(INSERT,scriptExistent)
        except:
            pass
        

        concluir = Button(scripter,text="concluir",command=self.addScriptToWidget)
        concluir.pack()

        scripter.mainloop()




    def setEntryFont(self,property):
        #print(propertyEntry)

        dictio= self.prop[property]

        entry = dictio.split(",")[0]

        button = dictio.split(",")[1]

        print(button)

        font = askfont(self.janela)

        
        print(self.propertys)

        self.propertys[entry].delete(0,END)

        FontFamily = font["family"].replace(" ","")

        stringFont = FontFamily + " " + str(font["size"]) + " " + font["weight"]
        

        self.propertys[entry].insert(0,stringFont)


        #self.objs[self.objectSelected].config(font=(font["family"],font["size"],font["weight"]))

        self.apply()


    def setEntryColor(self,property):
        #print(propertyEntry)

        dictio= self.prop[property]

        entry = dictio.split(",")[0]

        button = dictio.split(",")[1]

        print(button)

        color_code = colorchooser.askcolor(title ="Color")[1]

        
        print(self.propertys)

        self.propertys[entry].delete(0,END)
        self.propertys[entry].insert(0,color_code)

        self.propertys[button].config(bg=color_code)

        self.apply()


    def createProperties(self):

        #btnProperties = ["background","borderwidth","text","relief"]
        btnProperties = []


        #all = self.objs[self.objectSelected].config()
        #print(all)

        if self.objectSelected != "root":

            for item in self.objs[self.objectSelected].keys():
                print(item)
                btnProperties.append(item)
                #print(self.objs[self.objectSelected].cget(item))
        else:
            for item in self.janela.keys():
                print(item)
                btnProperties.append(item)
                #print(self.objs[self.objectSelected].cget(item)) 


        
        properties = btnProperties

        self.prop = {}

        try:
            properties.remove("background")
            properties.remove("foreground")
        except:
            pass
        
        
        propertyCount = len(properties)

      
        self.deletePropertys()

        
        count = 0

        while count < propertyCount:
            width = 14

            propertyName = properties[count]
            propertyLabel = "Label" + propertyName
            propertyEntry = "Entry" + propertyName

            #print(len(propertyLabel))
            labelText = properties[count]

            if len(labelText) > 12:
                labelText = labelText[:11] + "..."

            #print(propertyName)
 
            if self.objectSelected != "root":
                x = self.objs[self.objectSelected].cget(propertyName)
            else:
                x = self.janela.cget(propertyName)
            
            

            self.propertys[propertyLabel] = Label(self.FrameProperties,text=labelText,bg="#242526",fg='white')
            self.propertys[propertyLabel].grid(column=0,row=count)
            



            if propertyName == "bg" or "fg" or "font" or "command":
                
                btn = propertyName + 'Button'
                self.prop[propertyName] = propertyEntry + ',' + btn
                
            
                if propertyName == "bg":
                    self.propertys[btn] = Button(self.FrameProperties,bg=x,text='..',command=lambda:[app.setEntryColor(self,'bg')])
                    self.propertys[btn].grid(column=2,row=count)
                
                if propertyName == "fg":
                    self.propertys[btn] = Button(self.FrameProperties,bg=x,text='..',command=lambda:[app.setEntryColor(self,'fg')])
                    self.propertys[btn].grid(column=2,row=count)

                if propertyName == "font":
                    self.propertys[btn] = Button(self.FrameProperties,bg="white",text='..',command=lambda:[app.setEntryFont(self,'font')])
                    self.propertys[btn].grid(column=2,row=count)

                if propertyName == "command":
                    self.propertys[btn] = Button(self.FrameProperties,bg="white",text='onClick',command=lambda:[app.createScriptBox(self,'command')])
                    self.propertys[btn].grid(column=1,row=count)

            
            if propertyName != "command":
                self.propertys[propertyEntry] = Entry(self.FrameProperties,width=width)

                self.propertys[propertyEntry].grid(column=1,row=count)

                self.propertys[propertyEntry].insert(0,x)
            
            #print(x)

            count = count + 1


    def listboxCall(self,event):
        
        try:
            self.objectSelected = self.listObjectsGUI.get(self.listObjectsGUI.curselection())
            print(self.objectSelected)

            x = self.objs[self.objectSelected].winfo_rootx() - self.frameDesigner.winfo_rootx()
            y = self.objs[self.objectSelected].winfo_rooty() - self.frameDesigner.winfo_rooty()

            print(x,y)
            

            objType= self.objs[self.objectSelected]
            


            print(objType)


            
            self.labelMove.place(x=x,y=y-20)
            self.createProperties()
        except:
            pass


    def moveObj(self,event):
        self.soltar = 0


        while self.soltar == 0:
            x = self.frameDesigner.winfo_pointerx() - self.frameDesigner.winfo_rootx() - self.objs[self.objectSelected].winfo_width() / 2
            y = self.frameDesigner.winfo_pointery() - self.frameDesigner.winfo_rooty() - self.objs[self.objectSelected].winfo_height() / 2
            
            print(x,y)


            self.objs[self.objectSelected].place(x=x,y=y)
            
            
            self.labelMove.place(x=x,y=y-20)


            self.janela.update()
            


    def createComponent(self,value):
        
        #print(name)
        
        centerx = self.frameDesigner.winfo_width() / 2
        centery = self.frameDesigner.winfo_height() / 2

        self.countButton = self.countButton + 1

        if value == 'botao':
            
            name = 'Button' + str(self.countButton)

            self.objs[name] = Button(self.frameDesigner,text='button')
            self.objs[name].place(x=centerx,y=centery)

        if value == 'label':
            name = 'Label' + str(self.countButton)
            self.objs[name] = Label(self.frameDesigner,text='Label')
            self.objs[name].place(x=centerx,y=centery)

        
        self.listboxIndex = self.listboxIndex + 1

        self.listObjectsGUI.insert(self.listboxIndex,name)

        
    def soltar(self,event):
        self.soltar = 1

    def clickFrame(self,event):
        self.objectSelected = "root"
        self.createProperties()


    def __init__(self):
        self.janela = Tk()
        
        self.objs = {}
        self.propertys = {}
        self.objScripts = {}


        self.homeDir = str(Path.home())

        self.countButton = 0
        self.janela.geometry("700x400")
        

        self.listboxIndex = 0
        self.listObjectsGUI = Listbox(self.janela,bg = '#242526',fg='white')
        self.listObjectsGUI.place(x=500,y=0)
        
        createButton = Button(self.janela,text='botao',command=lambda:[app.createComponent(self,value='botao')])
        createButton.place(x=0,y=0)


        createButton = Button(self.janela,text='label',command=lambda:[app.createComponent(self,value='label')])
        createButton.place(x=0,y=40)

        createButton = Button(self.janela,text='command',command=self.openCommand)
        createButton.place(x=0,y=80)
        




        self.janela.configure(bg='#18191A')


        self.frameDesigner = Frame(self.janela,height=400,width=400,highlightbackground="#242526",highlightthickness=2)
        self.frameDesigner.place(x=50,y=0)



        #self.FrameProperties = Frame(self.janela,bg='#242526',height=210,width=150,highlightbackground="#FFFFFF",highlightthickness=1)
        #self.FrameProperties.place(x=500,y=180,height=210,width=150)
        
        

        ######             preciso ver essa programacao     ###########

        self.container = Frame(self.janela,bg = '#242526',highlightbackground="#FFFFFF",highlightthickness=1)
        self.container.place(x=500,y=180,height=210,width=197) #coloca na janela

        canvas = Canvas(self.container,bg = '#242526')
        canvas.place(x=0,y=0,height=210,width=180) #canvas para controle y dentro do container

        scrollbar = Scrollbar(self.container, orient="vertical", command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") #criando a scroll bar dentro do container

        self.FrameProperties = Frame(canvas,bg = '#242526') #frame dentro do canvas q vai ter todas propriedades

        self.FrameProperties.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.FrameProperties, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set) #define a scrollbar como a pos y do canvas

        ################################################################

        
        apply = Button(text="apply",command=self.apply)
        apply.place(x=640,y=0)

        export = Button(text="export",command=self.getObjectsExport)
        export.place(x=640,y=50)

        export = Button(text="delete",command=self.deleteComponent)
        export.place(x=640,y=100)
       
        self.detach = Button(text="detach",command=self.propertyDetach,bg='#18191A',borderwidth=0,fg='white')
        self.detach.place(x=640,y=150)


        self.labelMove = Label(self.frameDesigner,text='MOVE')
        
        self.labelMove.bind('<Button-1>', self.moveObj)

        self.labelMove.bind('<ButtonRelease-1>', self.soltar)

        self.frameDesigner.bind('<Button-1>', self.clickFrame)

        #self.janela.bind('<<ListboxSelect>>', self.listboxCall)

        self.listObjectsGUI.bind('<ButtonRelease-1>',self.listboxCall)
        #self.listObjectsGUI.bind('<<ListboxSelect>>',self.listboxCall)

        


        self.janela.mainloop()


app = app()
