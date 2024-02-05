from Tkinter import *
import time
master = Tk()



frame = Canvas(master, width=600, height=600, bg="white")

frame.pack()




def redFirework(x1,y1, xn,yn, tag="redFirework", outline='red'):
    frame.create_rectangle(x1,y1, xn,yn, tag="redFirework", outline='red')

def blueFirework(x1, y1, xn, yn):
    frame.create_rectangle(x1, y1, xn, yn)
    
def greenFirework(x1, y1, xn, yn):
    frame.create_rectangle(x1, y1, xn, yn)






#Objects that don't move 
frame.create_line(0, 500, 600, 500)

#launcher 1
firework_launcher1 = frame.create_rectangle(100, 500, 110, 490)

#launcher 2
firework_launcher2 = frame.create_rectangle(300, 500, 310, 490)

#launcher 3
firework_launcher3 = frame.create_rectangle(500, 500, 510, 490)
#firework starting postion

redFirework(102, 490, 108,485)
#determinig if it should launch the fireworks 
def mouseClick(mouseClickCoords):
    redFireworkX1 = 102
    redFireworkXn = 108
    redFireworkY1 = 490
    redFireworkYn = 485
    
    if mouseClickCoords.x >= 100 and mouseClickCoords.x <= 110 and mouseClickCoords and mouseClickCoords.y >= 490 and mouseClickCoords.y <= 500 and redFireworkY1 > 400:
        for i in range(1,50): #animation of Firework
            redFireworkY1 = (redFireworkY1 - 3)
            redFireworkYn = (redFireworkYn - 3)
            redFirework(104, redFireworkY1, 106, redFireworkYn)
            frame.update()
            frame.delete("redFirework")
            time.sleep(0.03)
          #explosion animation  
    if redFireworkY1 < 400:
        frame.create_line(104, 200, 340, 300, tag=("explosion"))
        frame.update()
        time.sleep(2)
        frame.delete("explosion")
        
            
            
            
        





    
    

frame.bind ("<Button-1>", mouseClick)
mainloop()