import tkinter as tk
import time

class PDController:
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd
        self.prev_error = None

    def control(self, error):
        if self.prev_error is None:
            self.prev_error = error
        derivative = error - self.prev_error
        control = self.kp * error + self.kd * derivative
        self.prev_error = error
        return control




class Point:
    def __init__(self, canvas, x, y, color,controller):
        self.canvas = canvas
        self.color = color
        self.id = canvas.create_oval(x-5, y-5, x+5, y+5, fill=self.color)
        self.pos = [x,y]

        self.controller = controller

    def move(self,x,y):
        error = self.distance(x, y)
        control = self.controller.control(error)
        dx = control * (x - self.pos[0]) / error
        dy = control * (y - self.pos[1]) / error
        self.canvas.move(self.id, dx, dy)
        self.pos[0] += dx
        self.pos[1] += dy


    def distance(self,x,y):
        a=((self.pos[0] - x) ** 2 + (self.pos[1] - y) ** 2) ** 0.5
        #print(a)
        return a


class Cross:
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.id1 = canvas.create_line(x-30,y,x+30,y)
        self.id2 = canvas.create_line(x,y+30,x,y-30)
        self.center = [x,y]

    def move(self, dx, dy):
        self.canvas.move(self.id1, dx, dy)
        self.canvas.move(self.id2, dx, dy)
        self.center[0] += dx
        self.center[1] += dy


class App:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=1280, height=720)
        self.canvas.pack()


        self.controller = PDController(0.1, 0.02)
        self.points = Point(self.canvas, 50, 50, 'red',self.controller)
        self.cross = Cross(self.canvas,400,400)
        
        self.canvas.bind("<Button-1>", self.callback_mouse)
        #self.detect_cross()
        self.after_id = None
        
    def callback_mouse(self,event):
        x, y = event.x, event.y
        dx, dy = x - self.cross.center[0], y - self.cross.center[1]
        self.cross.move(dx, dy)
        if self.after_id:
            self.master.after_cancel(self.after_id)
        self.detect_cross()

    def detect_cross(self):
        self.points.move(self.cross.center[0], self.cross.center[1])
        self.after_id=self.master.after(10, self.detect_cross)
        


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
