from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog,messagebox
import PIL.ImageGrab as ImageGrab
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import os

class Draw():
    def __init__(self,root):

#Defining title and Size of the Tkinter Window GUI
        self.root =root
        self.train_name='train_data.csv'
        self.targets_name='targets.csv'
        self.root.state("zoomed") #maximize
        self.root.title("Copy Assignment Painter")
#         self.root.geometry("810x530")
        self.root.configure(background="white")
        self.root.resizable(False,False)
#         self.root.resizable(0,0)

#variables for pointer and Eraser   
        self.pointer= "white"
        self.erase="white"

#Widgets for Tkinter Window
    
# Configure the alignment , font size and color of the text
        text=Text(root)
        text.tag_configure("tag_name", justify='center', font=('arial',25),background='#292826',foreground='orange')

# Insert a Text
        text.insert("1.0", "Drawing Application in Python")

# Add the tag for following given text
        text.tag_add("tag_name", "1.0", "end")
        text.pack()
        
        canvas = Canvas(root,bg="white",width=100, height=30 ,bd=0)
        canvas.create_line(0, 25, 75, 25)
        canvas.place(x=0,y=270)
        
        self.text_result=Label(root,text='RESULT:',font=("Helvetica", 9),bg="white",fg="red")
        self.text_result.place(x=0,y=310)
        
        self.final_result=Label(root,text='')
        self.error=Label(root,text='',font=("Helvetica", 9),bg="white",fg="red")
        self.add_msg=Label(root,text='',font=("Helvetica", 9),bg="white",fg="red")

# Reset Button to clear the entire screen 
        self.clear_screen= Button(self.root,text="Clear Screen",bd=4,bg='white',command=self.clear_screen,width=9,relief=RIDGE)
        self.clear_screen.place(x=0,y=227)

# Save Button for saving the image in local computer
        self.save_btn= Button(self.root,text="PREDICT",bd=4,bg='white',command=self.predict,width=9,relief=RIDGE)
        self.save_btn.place(x=0,y=257)
        
# Add Button 
        self.add_btn= Button(self.root,text="ADD",bd=4,bg='white',command=self.add,width=9,relief=RIDGE)
        self.add_btn.place(x=0,y=370)

# adding Entry
        self.number=Entry(self.root,bd=7,width=11)
        self.number.place(x=0,y=403)


#Defining a background color for the Canvas 
        self.background = Canvas(self.root,bg='black',bd=5,relief=GROOVE,height=470,width=680)
        self.background.place(x=80,y=40)


#Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>",self.paint) 
        
    ################################## training #########################################
        if(not(os.path.exists(self.train_name) and os.path.exists(self.targets_name) )):
            digits=cv2.imread("digits.png",cv2.IMREAD_GRAYSCALE)
            rows=np.vsplit(digits,50)
            cells=[]
            cells2=[]
            for row in rows :
                row_cells=np.hsplit(row,100)
                for cell in row_cells:
                    cells.append(cell)
                    #all in one column 
                    cells2.append(cell.flatten())

            #cells2 is a list and in openCV we need numpy array because it is faster than list
            cells2=np.array(cells2,dtype=np.float32)
            pd.DataFrame(cells2,index=None).to_csv("train_data.csv",index=False)
            self.cells2=np.array(pd.read_csv('train_data.csv'),dtype=np.float32)
            n=np.arange(10)
            targets=np.repeat(n,500)
            pd.DataFrame(targets,index=None).to_csv("targets.csv",index=False)
            self.targets=np.array(pd.read_csv('targets.csv'),dtype=np.int32).flatten()
        
#        self.knn=KNeighborsClassifier(n_neighbors=6,metric='minkowski')
#        self.knn.fit(cells2,targets)
        else:
            self.cells2=np.array(pd.read_csv('train_data.csv'),dtype=np.float32)
            self.targets=np.array(pd.read_csv('targets.csv'),dtype=np.int32).flatten()
            
        self.knn=cv2.ml.KNearest_create()
        self.knn.train(self.cells2,cv2.ml.ROW_SAMPLE,self.targets)
    #####################################################################################

    def paint(self,event):       
        x1,y1 = (event.x-2), (event.y-2)  
        x2,y2 = (event.x+2), (event.y+2)  

        self.background.create_oval(x1,y1,x2,y2,fill=self.pointer,outline=self.pointer,width=35)
        
    def add(self):     
        
        my_number=self.number.get()
        if my_number.isdigit():
            self.targets=np.append(self.targets, my_number)
            self.cells2=np.concatenate(  (self.cells2,self.my_test_flat),axis=0 )
            pd.DataFrame(self.cells2,index=None).to_csv("train_data.csv",index=False)
            pd.DataFrame(self.targets,index=None).to_csv("targets.csv",index=False)
            self.add_msg.configure(text='Target added \n successfully',font=("Helvetica", 9),bg="white",fg="green")
            self.add_msg.place(x=0,y=430)

        else:
            # self.error=Label(root,text='please enter \n an integer',font=("Helvetica", 9),bg="white",fg="red")
            self.error.configure(text='please enter \n an integer')
            self.error.place(x=0,y=430)
        
        
    def clear_screen(self):
        self.background.delete('all')
        self.final_result.configure(text='')
        self.error.configure(text='')
        self.add_msg.configure(text='')
        
    def select_color(self,col):
        pass
    def eraser(self):
        pass
    def canvas_color(self):
        pass
    def predict(self):
        
        ############################## save image ################################
        try:
            # self.background update()
#            file_ss =filedialog.asksaveasfilename(defaultextension='jpg')
            #print(file_ss)
            x=self.root.winfo_rootx() + self.background.winfo_x()
            #print(x, self.background.winfo_x())
            y=self.root.winfo_rooty() + self.background.winfo_y()
            #print(y)

            x1= x + self.background.winfo_width() 
            #print(x1)
            y1= y + self.background.winfo_height()
            #print(y1)
            ImageGrab.grab().crop((x+55 , y+45, x1+370, y1+260)).save("test.png")
#            messagebox.showinfo('Screenshot Successfully Saved as' + str(file_ss))

        except:
            print("Error in saving the screenshot")
        
        ######################################### predict ##############################
        my_digit=cv2.imread("test.png",cv2.IMREAD_GRAYSCALE)
        my_digit = cv2.resize(my_digit, (20, 20)) 
        ####################
        my_test_flat=[]
        my_test_flat.append(my_digit.flatten())
        self.my_test_flat=np.array(my_test_flat,dtype=np.float32)
        
#        my_predict = self.knn.predict(my_test_flat)
        ret,result,neighbours,dist=self.knn.findNearest(self.my_test_flat,k=3)
        print(result)
        
        
        self.final_result.configure(text=int(result[0][0]),font=("Helvetica", 9),bg="white",fg="red")
        self.final_result.place(x=55,y=310)

        #####################
#        cv2.imshow("digits",my_digit)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        #####################
        
        
        

###############################################################################################


if __name__ =="__main__":
    root = Tk()
    p= Draw(root)
    root.mainloop()
    


