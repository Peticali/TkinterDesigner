from tkinter import *


class app():
    
    def deletePropertys(self):
        count = 0
        size = len(self.propertys)

        print(size)

        while size > count:
            x = list(self.propertys.keys())[count]

            self.propertys[x].destroy()

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


    def createProperties(self):

        btnProperties = ["bg","borderwidth"]

        properties = btnProperties

        propertyCount = len(properties)

      
        self.deletePropertys()

        
        count = 0

        while count < propertyCount:
            
            propertyName = properties[count]
            propertyLabel = "Label" + propertyName
            propertyEntry = "Entry" + propertyName

            

            self.propertys[propertyLabel] = Label(self.FrameProperties,text=properties[count],bg="#242526",fg='white')
            self.propertys[propertyLabel].grid(column=0,row=count)
            
            self.propertys[propertyEntry] = Entry(self.FrameProperties,width=5)
            self.propertys[propertyEntry].grid(column=1,row=count)
            

            count = count + 1


    def listboxCall(self,event):
        
        self.objectSelected = self.listObjectsGUI.get(self.listObjectsGUI.curselection())
        print(self.objectSelected)

        x = self.objs[self.objectSelected].winfo_rootx() - self.frameDesigner.winfo_rootx()
        y = self.objs[self.objectSelected].winfo_rooty() - self.frameDesigner.winfo_rooty()

        print(x,y)
        

        objType= self.objs[self.objectSelected]
        


        print(objType)


        
        self.labelMove.place(x=x,y=y-20)
        self.createProperties()


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

    
    def __init__(self):
        self.janela = Tk()
        
        self.objs = {}
        self.propertys = {}

        self.countButton = 0
        self.janela.geometry("700x400")
        

        self.listboxIndex = 0
        self.listObjectsGUI = Listbox(self.janela,bg = '#242526',fg='white')
        self.listObjectsGUI.place(x=500,y=0)
        
        createButton = Button(self.janela,text='botao',command=lambda:[app.createComponent(self,value='botao')])
        createButton.place(x=0,y=0)


        createButton = Button(self.janela,text='label',command=lambda:[app.createComponent(self,value='label')])
        createButton.place(x=0,y=40)




        self.janela.configure(bg='#18191A')


        self.frameDesigner = Frame(self.janela,height=400,width=400,highlightbackground="#242526",highlightthickness=2)
        self.frameDesigner.place(x=50,y=0)



        self.FrameProperties = Frame(self.janela,bg='#242526',height=210,width=150,highlightbackground="#FFFFFF",highlightthickness=1)
        
        
        self.FrameProperties.place(x=500,y=180,height=210,width=150)
        
        
        apply = Button(text="apply",command=self.apply)
        apply.place(x=660,y=240)
       


        self.labelMove = Label(self.frameDesigner,text='MOVE')
        
        self.labelMove.bind('<Button-1>', self.moveObj)

        self.labelMove.bind('<ButtonRelease-1>', self.soltar)

        #self.janela.bind('<<ListboxSelect>>', self.listboxCall)

        self.listObjectsGUI.bind('<ButtonRelease-1>',self.listboxCall)
        #self.listObjectsGUI.bind('<<ListboxSelect>>',self.listboxCall)


        self.janela.mainloop()



app = app()