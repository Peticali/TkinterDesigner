from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from pathlib import Path
from tkinter.ttk import Style
from pyautogui import failSafeCheck
from tkfontchooser import askfont
import os

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

        self.createProperties(window=self.FrameProperties,windowString="self.FrameProperties")
        



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

        self.createProperties(window=self.FrameProperties,windowString="self.FrameProperties")





    def getObjectsExport(self):
        
        countScript = 0
        code = """from tkinter import * 

class app(): #NOT DELETE ANY COMMENTS GENERATED BY THE PROGRAM."""


        scriptCount = len(self.objScripts)


        
        while countScript < scriptCount:
            widgetName = list(self.objScripts.keys())[countScript]
            widgetScript = self.objScripts[widgetName]
            widgetScript = '        '.join(('\n'+widgetScript.lstrip()).splitlines(True))


          



            StrFunction = '    def ' + widgetName + '(self):\n'
            StrFunction = StrFunction  + widgetScript

            #'\t\t\t'.join(StrFunction.splitlines(True))
            #StrFunction = '\t\t\t'.join(('\n'+StrFunction.lstrip()).splitlines(True))





            print(StrFunction)
            countScript = countScript + 1
            code = code + '\n' + StrFunction + "\n" + "\t\t#endFunction\n"




        code = code +"""
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
            #print(widget)

            type = self.objs[widget].winfo_class() 
        
            string = type+ "(self.root,"

            x = self.objs[widget].winfo_rootx() - self.frameDesigner.winfo_rootx()
            y = self.objs[widget].winfo_rooty() - self.frameDesigner.winfo_rooty()


            for property in self.objs[widget].keys():
                

                if property == "command":
                    try:
                        widgetScript = self.objScripts[widget]
                        string = string + property + '=' +  "self." + widget + ','
                    except:
                        value = self.objs[widget].cget(property)
                        string = string + property + '=' +  "'" + str(value) + "'" + ','
                    
                elif property == "class":
                    pass
                else:
                    value = self.objs[widget].cget(property)
                    string = string + property + '=' +  "'" + str(value) + "'" + ','

            
            height = self.objs[widget].winfo_height()
            width = self.objs[widget].winfo_width()

            string = "        " + 'self.' + widget + " = " + string[:-1] + ')\n'  
            string = string + "        " + 'self.' + widget + ".place(x=" + str(x) + ',y=' + str(y) +  ",height=" + str(height) + ",width=" + str(width) + ')'


            code = code + "\n" + string

            count = count + 1

        exportinit =  '        '.join(('\n'+self.initScript.lstrip()).splitlines(True))

        code = code + "\n\t\t#close Objects\n\n" + exportinit + "\n        self.root.mainloop()"
        code = code + "\napp = app()"


        try:
            file = open(self.homeDir + "/Desktop/code.py", "w")
            n = file.write(code)
            file.close()
        except:
            pass

        path = "python " + '"'+ self.homeDir + "/Desktop/code.py" + '"'
        #path = self.homeDir + "/Desktop/code.py " + '1'

        #os.system('cmd /k' + path)
      
        os.system(path)
        

        #exec(code)


        #print(code)


    




    def importProject(self):
        countWidgets = 0
        countImportar = 1
        
        countWidgetLine = 1

        countPlaceLine = 2

        path = askopenfilename()

        file = open(path, "r")
        f = file.read()
        file.close()

        initScript = f

        f = f.split("#init Objects")[1]
        f = f.split("#close Objects")[0]

        self.listObjectsGUI.delete(0,'end')


        for child in self.frameDesigner.winfo_children():
            if child != self.labelMove:
                if child != self.ResizeObjW:
                
                    child.destroy()


        for line in f:
            if line == "\n":
                countWidgets = countWidgets + 1

        countWidgets = countWidgets - 1
        countWidgets = countWidgets /2


        f = f.replace("self.root"," ")

        lines = f.split("\n")
        
        


        rootScript = initScript.split("#this script will execute after all widgets are created.")[1]
        rootScript = rootScript.split("self.root.mainloop()")[0]

        
        
        count = 1
        stringFunc = ""
        function = rootScript.split("\n")

        size = len(function)

        while count < size:
            stringFunc = stringFunc + "\n" +  str(function[count])[8:]

            #print(function[count])

            count = count + 1
            
        

        stringFunc = stringFunc[:stringFunc.rfind('\n')]




        rootScript = "#this script will execute after all widgets are created." + stringFunc

        self.initScript = rootScript
        
        
        
        print(rootScript)


        while countImportar <= countWidgets :

            lineObject = lines[countWidgetLine] #ler o objeto (o primeiro é em linha 1)

            linePlace = lines[countPlaceLine] #ler o place do objeto


            widgetName = linePlace.split("self.")[1]
            widgetName = widgetName.split(".")[0]

            tipo = lineObject.split(" ")[10]
            tipo = tipo.split("(")[0]

            placex = linePlace.split("=")[1]
            placex = placex.split(",")[0]

            placey = linePlace.split("=")[2]
            placey = placey.split(",")[0]

            height = linePlace.split("=")[3]
            height = height.split(",")[0]

            width = linePlace.split("=")[4]
            width = width.split(",")[0]

            width = width[:-1]


            widgetproperties = lineObject.split("(")[1]
            widgetproperties = widgetproperties.split(")")[0]

            widgetproperties = widgetproperties.replace("=",":")
            
            propertiesToProcess = 1

            propertyDict = {}

            for char in widgetproperties:
                if char == ',':
                    
                    propertie = widgetproperties.split(",")[propertiesToProcess]
                    propertie = propertie.split(",")[0]

                    propertyName = propertie.split(":")[0]
                    
                    try:
                        propertyValue = propertie.split("'")[1]
                        
                        if propertyName == "command":
                            print(widgetName,"n tem script")
                    except:
                        propertyValue = ""

                        if propertyName == "command":
                            print(widgetName,"TEM SCRIPT")

                            file = open(path, "r")
                            string = file.read()
                            file.close()

                            func = string.split("def " + widgetName + "(self):\n\n")[1]

                            func = func.split("#endFunction")[0]
                            
                            #function = ""
                            count = 0
                            stringFunc = ""
                            function = func.split("\n")

                            size = len(function)

                            while count < size:
                                stringFunc = stringFunc + "\n" +  str(function[count])[8:]

                                #print(function[count])

                                count = count + 1
                                
                            
                            stringFunc = stringFunc.split("\n",1)[1]

                            stringFunc = stringFunc[:stringFunc.rfind('\n')]

                            
                            print(stringFunc)


                            self.objScripts[widgetName] = stringFunc
                    
                    propertyDict[propertyName] = propertyValue
                    
                    propertiesToProcess = propertiesToProcess + 1

            #print(propertyDict)


            if tipo == "Button":
                self.objs[widgetName] = Button(self.frameDesigner,propertyDict)
            if tipo == "Label":
                self.objs[widgetName] = Label(self.frameDesigner,propertyDict)
            if tipo == "Entry":
                self.objs[widgetName] = Entry(self.frameDesigner,propertyDict)
            if tipo == "Frame":
                self.objs[widgetName] = Frame(self.frameDesigner,propertyDict)
            if tipo == "Listbox":
                self.objs[widgetName] = Listbox(self.frameDesigner,propertyDict)

            self.objs[widgetName].place(x=placex,y=placey,width=width,height=height)
            
            self.listboxIndex = self.listboxIndex + 1
            self.listObjectsGUI.insert(self.listboxIndex,widgetName)


            countPlaceLine = countPlaceLine +2
            countWidgetLine = countWidgetLine +2


            countImportar = countImportar + 1#proximo obj




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

        #print(size)

        while size > count:
            x = list(self.propertys.keys())[count]

            try:
                get = self.propertys[x].get()
                config = {}

                x = x.split("Entry")[1]

               


                config[x] = get
                
                #print(config)

                self.objs[self.objectSelected].config(config)

                #print(get)
            except:
                pass


            count = count + 1

    #def createFuncButton(self):

    def addScriptToWidget(self):
        
        script = self.script.get('1.0', 'end-1c')

        if script == "":
         
            try:
                del self.objScripts[self.objectSelected]
            except:
                pass

        else:

            self.objScripts[self.objectSelected] = script

        self.scripter.destroy()


    def setInitString(self):
        script = self.script.get('1.0', 'end-1c')

        self.initScript = script

        self.scripter.destroy()


    def getPropertysScripter(self,event):
        self.objectTempSelected = self.objectSelected
       
        self.objectSelected = self.listObjectsPropChooser.get(self.listObjectsPropChooser.curselection())
        print(self.objectSelected)
        self.createProperties(window=self.FramePropertiesChoose,windowString="self.FramePropertiesChoose")

    def getLabelPushed(self,event):
        caller = "self." + self.objectSelected + ".config(" + event.widget.cget("text") + "="
        print(caller)

        self.objectSelected = self.objectTempSelected
        
        self.script.insert(INSERT,caller)

        self.chooseProperty.destroy()


    def scriptBoxGetPropertyWindow(self):
        self.chooseProperty = Tk()
        self.listObjectsPropChooser = Listbox(self.chooseProperty,bg = '#242526',fg='white')
        self.listObjectsPropChooser.place(x=0,y=0,width=180)

        self.chooseProperty.geometry("185x390")
        self.chooseProperty.config(bg="#242526")

        values = self.listObjectsGUI.get(0,END)

        index = 1
        for key in values:
            self.listObjectsPropChooser.insert(index, key)
            index = index + 1

        
        container = Frame(self.chooseProperty,bg = '#242526',highlightbackground="#FFFFFF",highlightthickness=1)
        container.place(x=0,y=180,height=200,width=180) #coloca na janela

        canvas = Canvas(container,bg = '#242526')
        canvas.place(x=0,y=0,width=180) #canvas para controle y dentro do container

        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") #criando a scroll bar dentro do container

        self.FramePropertiesChoose = Frame(canvas,bg = '#242526') #frame dentro do canvas q vai ter todas propriedades

        self.FramePropertiesChoose.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((20, 0), window=self.FramePropertiesChoose, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set) #define a scrollbar como a pos y do canvas

        self.listObjectsPropChooser.bind('<ButtonRelease-1>',self.getPropertysScripter)




    def createScriptBox(self,property):
        self.scripter = Tk()

        self.scripter.geometry("620x430")
        self.scripter.config(bg="#242526")

        self.script = Text(self.scripter,bg="#242526",fg="white")
        self.script.pack()

        chooseProperty = Button(self.scripter,text="Choose WidgetProp",command=self.scriptBoxGetPropertyWindow)
        chooseProperty.pack(side=LEFT)

        if property != "commandRoot":

            try:
                scriptExistent = self.objScripts[self.objectSelected]
                self.script.insert(INSERT,scriptExistent)
            except:
                pass
            

            concluir = Button(self.scripter,text="concluir",command=self.addScriptToWidget)
            concluir.pack(side=RIGHT)

        else:
            scriptExistent = self.initScript
            self.script.insert(INSERT,scriptExistent)
            concluir = Button(self.scripter,text="concluir",command=self.setInitString)
            concluir.pack(side=RIGHT)


        self.scripter.mainloop()




    def setEntryFont(self,property):
        #print(propertyEntry)

        dictio= self.prop[property]

        entry = dictio.split(",")[0]

        button = dictio.split(",")[1]

        print(button)

        font = askfont(self.janela)

        
        print(font)

        #print(self.propertys)

        if font != "":

            FontFamily = font["family"].replace(" ","")

            stringFont = FontFamily + " " + str(font["size"]) + " " + font["weight"]
        

        
            self.propertys[entry].delete(0,END)
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

        
        print(color_code)

        if color_code != None:
            self.propertys[entry].delete(0,END)
            self.propertys[entry].insert(0,color_code)

            self.propertys[button].config(bg=color_code)

            self.apply()




    def createProperties(self,window,windowString):

        #btnProperties = ["background","borderwidth","text","relief"]
        btnProperties = []

        #window = self.FrameProperties

        #all = self.objs[self.objectSelected].config()
        #print(all)

        if self.objectSelected != "root":

            for item in self.objs[self.objectSelected].keys():
                #print(item)
                btnProperties.append(item)


                #print(self.objs[self.objectSelected].cget(item))
        else:
            btnProperties.append("title")
            btnProperties.append("bg")
            btnProperties.append("width") 
            btnProperties.append("height")         
            btnProperties.append("command")


        
        properties = btnProperties

        self.prop = {}

        try:
            properties.remove("class")
        except:
            pass
        try:
            properties.remove("background")
        except:
            pass
        try:
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
                
                try:
                    x = self.frameDesigner.cget(propertyName)
                
                except:
                    x = ""
            
            
            #print(str(window))

            if windowString != "self.FramePropertiesChoose":
            
            
                self.propertys[propertyLabel] = Label(window,text=labelText,bg="#242526",fg='white')
                self.propertys[propertyLabel].grid(column=0,row=count)
            



                if propertyName == "bg" or "fg" or "font" or "command":
                    
                    btn = propertyName + 'Button'
                    self.prop[propertyName] = propertyEntry + ',' + btn
                    
                
                    if propertyName == "bg":
                        self.propertys[btn] = Button(window,bg=x,text='..',command=lambda:[app.setEntryColor(self,'bg')])
                        self.propertys[btn].grid(column=2,row=count)
                    
                    if propertyName == "fg":
                        self.propertys[btn] = Button(window,bg=x,text='..',command=lambda:[app.setEntryColor(self,'fg')])
                        self.propertys[btn].grid(column=2,row=count)

                    if propertyName == "font":
                        self.propertys[btn] = Button(window,bg="white",text='..',command=lambda:[app.setEntryFont(self,'font')])
                        self.propertys[btn].grid(column=2,row=count)

                    if propertyName == "command":
                        if self.objectSelected != "root":

                            self.propertys[btn] = Button(window,bg="white",text='onClick',command=lambda:[app.createScriptBox(self,'command')])
                            self.propertys[btn].grid(column=1,row=count)
                        else:
                            self.propertys[btn] = Button(window,bg="white",text='onClick',command=lambda:[app.createScriptBox(self,'commandRoot')])
                            self.propertys[btn].grid(column=1,row=count)

                
                if propertyName != "command":
                    self.propertys[propertyEntry] = Entry(window,width=width)

                    self.propertys[propertyEntry].grid(column=1,row=count)

                    self.propertys[propertyEntry].insert(0,x)
                
                #print(x)
            
            
            else:
                btn = propertyName + 'LabelChooseProp'
                self.propertys[btn] = Label(window,bg="#242526",text=propertyName,fg="white")
                self.propertys[btn].grid(column=0,row=count)
                self.propertys[btn].bind("<Button-1>", self.getLabelPushed)


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


            
            self.labelMove.place(x=x,y=y-20) #DELETOU ESSA PORRA

            x = self.objs[self.objectSelected].winfo_rootx() - self.frameDesigner.winfo_rootx() + self.objs[self.objectSelected].winfo_width() 
            y = self.objs[self.objectSelected].winfo_rooty() - self.frameDesigner.winfo_rooty() + self.objs[self.objectSelected].winfo_height() 

            self.ResizeObjW.place(x=x+5,y=y+5)

            self.createProperties(window=self.FrameProperties,windowString="self.FrameProperties")
        except:
            pass


    def moveObj(self,event):
        self.soltar = 0
        try:
            self.labelMove.tkraise()
            self.ResizeObjW.tkraise()
        except:
            pass

        if event.widget.cget("text") == "MOVE":

            
            while self.soltar == 0:
                x = self.frameDesigner.winfo_pointerx() - self.frameDesigner.winfo_rootx() - self.objs[self.objectSelected].winfo_width() / 2
                y = self.frameDesigner.winfo_pointery() - self.frameDesigner.winfo_rooty() - self.objs[self.objectSelected].winfo_height() / 2
                

                xRes = self.frameDesigner.winfo_pointerx() - self.frameDesigner.winfo_rootx() + self.objs[self.objectSelected].winfo_width() /2
                yRes = self.frameDesigner.winfo_pointery() - self.frameDesigner.winfo_rooty() + self.objs[self.objectSelected].winfo_height() / 2
     

                self.objs[self.objectSelected].place(x=x,y=y)
                
                self.labelMove.place(x=x,y=y-20)
                
                self.ResizeObjW.place(x=xRes+5,y=yRes+5)


                self.janela.update()
        
        
        if event.widget.cget("text") == ">":
            xStatic = self.frameDesigner.winfo_pointerx() - self.frameDesigner.winfo_rootx() - self.objs[self.objectSelected].winfo_width() #/ 2
            yStatic = self.frameDesigner.winfo_pointery() - self.frameDesigner.winfo_rooty() - self.objs[self.objectSelected].winfo_height() #/ 2
            
            self.labelMove.place(x=xStatic,y=yStatic-20)

            while self.soltar == 0:
                


                x = self.frameDesigner.winfo_pointerx() - self.frameDesigner.winfo_rootx() #-  #/ 2
                y = self.frameDesigner.winfo_pointery() - self.frameDesigner.winfo_rooty() #- self.objs[self.objectSelected].winfo_height() #/ 2
               

                #print("diferença", x,y)

                x = x - xStatic
                y = y - yStatic

                

                self.objs[self.objectSelected].place(x=xStatic,y=yStatic,height=y,width=x)

                x = self.frameDesigner.winfo_pointerx() - self.frameDesigner.winfo_rootx() #- self.objs[self.objectSelected].winfo_width() / 2
                y = self.frameDesigner.winfo_pointery() - self.frameDesigner.winfo_rooty() #- self.objs[self.objectSelected].winfo_height() / 2
               

                self.ResizeObjW.place(x=x,y=y)

                
                self.janela.update()
                #self.objs[self.objectSelected].place(x=x,y=y)
                #



    def createComponent(self,value):
        
        #print(name)
        
        centerx = self.frameDesigner.winfo_width() / 2
        centery = self.frameDesigner.winfo_height() / 2

        self.countButton = self.countButton + 1

        if value == 'botao':
            
            name = 'Button' + str(self.countButton)
            self.objs[name] = Button(self.frameDesigner,text='button')
            self.objs[name].place(x=centerx,y=centery)

        if value == "entry":
            name = 'Entry' + str(self.countButton)
            self.objs[name] = Entry(self.frameDesigner)
            self.objs[name].place(x=centerx,y=centery)

        if value == "frame":
            name = 'Frame' + str(self.countButton)
            self.objs[name] = Frame(self.frameDesigner)
            self.objs[name].place(x=centerx,y=centery)

        if value == "listbox":
            name = 'Listbox' + str(self.countButton)
            self.objs[name] = Listbox(self.frameDesigner)
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
        self.createProperties(window=self.FrameProperties,windowString="self.FrameProperties")


    def __init__(self):
        self.janela = Tk()
        
        self.objs = {}
        self.propertys = {}
        self.objScripts = {}
        self.initScript = "#this script will execute after all widgets are created."


        self.homeDir = str(Path.home())

        self.countButton = 0
        self.janela.geometry("700x418")
        

        self.listboxIndex = 0
        self.listObjectsGUI = Listbox(self.janela,bg = '#242526',fg='white')
        self.listObjectsGUI.place(x=500,y=0)
        
        styleButtons = {"bg":"#242526", "fg":"white","relief":"groove","borderwidth":2}

        
        createButton = Button(self.janela,styleButtons,text='Open',bg="#242526",command=self.importProject)
        createButton.place(x=0,y=0)

        createButton = Button(self.janela,styleButtons,text='Label',command=lambda:[app.createComponent(self,value='label')])
        createButton.place(x=0,y=40)
        
        createButton = Button(self.janela,styleButtons,text='Button',command=lambda:[app.createComponent(self,value='botao')])
        createButton.place(x=0,y=80)

        createButton = Button(self.janela,styleButtons,text='Frame',command=lambda:[app.createComponent(self,value='frame')])
        createButton.place(x=0,y=120)

        createButton = Button(self.janela,styleButtons,text='Entry',command=lambda:[app.createComponent(self,value='entry')])
        createButton.place(x=0,y=160)

        createButton = Button(self.janela,styleButtons,text='Listbox',command=lambda:[app.createComponent(self,value='listbox')])
        createButton.place(x=0,y=200)

        



        self.janela.configure(bg='#18191A')


        self.frameDesigner = Frame(self.janela,height=400,width=400)#highlightbackground="#242526",highlightthickness=2)
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

        
        apply = Button(self.janela,styleButtons,text="apply",command=self.apply)
        apply.place(x=576,y=390)

        export = Button(self.janela,styleButtons,text="export",bg="#3BB143",command=self.getObjectsExport)
        export.place(x=640,y=50)

        export = Button(self.janela,styleButtons,text="delete",bg="#FF0000",command=self.deleteComponent)
        export.place(x=640,y=100)
       
        self.detach = Button(text="detach",command=self.propertyDetach,bg='#18191A',borderwidth=0,fg='white')
        self.detach.place(x=640,y=150)


        self.labelMove = Label(self.frameDesigner,text='MOVE')
        
        self.labelMove.bind('<Button-1>', self.moveObj)

        self.labelMove.bind('<ButtonRelease-1>', self.soltar)


        self.ResizeObjW = Label(self.frameDesigner,text='>')


        self.ResizeObjW.bind('<Button-1>', self.moveObj)

        self.ResizeObjW.bind('<ButtonRelease-1>', self.soltar)


        self.frameDesigner.bind('<Button-1>', self.clickFrame)

        #self.janela.bind('<<ListboxSelect>>', self.listboxCall)

        self.listObjectsGUI.bind('<ButtonRelease-1>',self.listboxCall)
        #self.listObjectsGUI.bind('<<ListboxSelect>>',self.listboxCall)

        


        self.janela.mainloop()


app = app()
