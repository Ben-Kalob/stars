import turtle
import time
import math
import random

turtle.hideturtle()
turtle.tracer(0)
turtle.color("white")
turtle.fillcolor("white")

Window = turtle.Screen()
Window.bgcolor("black")
Window.title("Steriods")

class INPUT_STRUCTURE :
    
    inputs = []
    
    def __init__(self, key_name):
        INPUT_STRUCTURE.inputs.append(self) #ever time an input is defined, add it to a list so it can be updated in INPUT()
        self.key = key_name
    
    key = ""
    is_pressed = False
    just_pressed = False
    
    has_been_released = True
    
    ##the just pressed var needs a small window of time since the program actually 
    just_pressed_window_length = 1
    just_pressed_window = 1
    
    def press(self) :
        self.is_pressed = True
        if self.has_been_released == True :
            self.just_pressed = True
        self.has_been_released = False
    
    def release(self) :
        self.is_pressed = False
        self.has_been_released = True
    
    def update(self) :
        if self.just_pressed == True : 
            if self.just_pressed_window > 0 :
                self.just_pressed_window -= 1
            else: 
                self.just_pressed_window = self.just_pressed_window_length
                self.just_pressed = False
        Window.onkeypress(self.press, self.key)
        Window.onkeyrelease(self.release, self.key)
    


class vec2 :
    def __init__(self,x, y):
        self.x = x
        self.y = y
    ##magic
    def __str__(self):
        return str((self.x,self.y))
    def __add__(self,value) :
        return vec2(self.x+value.x,self.y+value.y)
    def __sub__(self,value) :
        return vec2(self.x-value.x,self.y-value.y)
    def __iadd__(self,value) :
        return self.__add__(value)
    def __isub__(self,value) :
        return self.__sub__(value)
    
    def __mul__(self,value) :
        return vec2(self.x*value,self.y*value)
    ##end-magic
    
    ##modify
    def normalized(self) :
        d = math.sqrt(pow(self.x,2)+pow(self.y,2))
        if d == 0 :
            return self
        return vec2(self.x/d,self.y/d)
    def distance_to(self,value) :
        dir = value - self
        return math.sqrt(pow(dir.x,2)+pow(dir.y,2))
    ##transforms
    def rotated(self,angle) :
        s = math.sin(angle)
        c = math.cos(angle)

        x = c * self.x - s * self.y
        y = s * self.x + c * self.y

        return vec2(x,y)

key_up = INPUT_STRUCTURE('Up')
key_down = INPUT_STRUCTURE('Down')
key_left = INPUT_STRUCTURE("Left")
key_right = INPUT_STRUCTURE("Right")

key_space = INPUT_STRUCTURE("space")

key_plus = INPUT_STRUCTURE('+')
key_minus = INPUT_STRUCTURE("-")

key_ESC = INPUT_STRUCTURE("Escape")

class polygon() :

    class_instances = []

    def __init__(self,sides,size) :
        self.sides = sides
        self.size = size
        self.rotation = ((2*math.pi)/sides)
        self.position = vec2(0,0)
        self.velocity = vec2(0,0)
        
        polygon.class_instances.append(self)
    
    def free(self) :
        if self in self.class_instances :
            self.class_instances.remove(self)
            del(self)

    def get_shape(self) :
        base_point = vec2(0,self.size)

        j_angle = ((2*math.pi)/self.sides)
        base_point = base_point.rotated(self.rotation+j_angle)
        
        points = []
        for i in range(self.sides+1) :
            base_point = base_point.rotated(j_angle)
            points.append(base_point+self.position)
        return points

class rock(polygon) :

    def __init__(self, sides, size,health):
        self.health = health
        self.rotational_velocity = (random.randint(1,100)/100) * 0.1
        super().__init__(sides, size)

class bullet(polygon) :
    shape = [vec2(0,-1),vec2(0,1)]

    def __init__(self,rotation):
        polygon.class_instances.append(self)
        self.size = 5
        self.rotation = rotation
        self.position = vec2(0,0)
        self.velocity = vec2(0,0)

    def get_shape(self) :
        
        points = []

        for point in self.shape :
            points.append((point.rotated(self.rotation) * self.size) + self.position)

        return points

class ship_main(polygon) :

    shape = [vec2(-1,-1),vec2(0,-0.5),vec2(1,-1),vec2(0,1.75),vec2(-1,-1)]

    def __init__(self):
        polygon.class_instances.append(self)
        self.rotation = 0.0
        self.size = 10
        self.position = vec2(0,0)
        self.speed = 5
    def get_shape(self) :
        
        points = []

        for point in self.shape :
            points.append((point.rotated(self.rotation) * self.size) + self.position)

        return points

tick_per_second = 30

delta = 0.0
previous_time = 0.0

ticks = 0

ship = ship_main()

new_rock_timer = 0.0

def input_check() :

    global tick_per_second

    Window.listen()

    for input_method in INPUT_STRUCTURE.inputs :
        input_method.update()
    
    if key_ESC.is_pressed :
        Window.bye()
        input("GG")
        

    if key_minus.just_pressed :
        tick_per_second -= 1 
        print(tick_per_second)
    if key_plus.just_pressed :
        tick_per_second += 1
        print(tick_per_second)


    if key_left.is_pressed :
        ship.rotation += 0.15
    if key_right.is_pressed :
        ship.rotation -= 0.15
    if key_up.is_pressed :
        ship.position += vec2(0,1).rotated(ship.rotation) * ship.speed
    if key_down.is_pressed :
        ship.position += vec2(0,-0.78).rotated(ship.rotation) * ship.speed
    
    if key_space.just_pressed :
        print("shoot")
        new_bullet = bullet(ship.rotation)
        dir = vec2(0,1).rotated(ship.rotation)
        new_bullet.velocity = dir * 10
        new_bullet.position = ship.position + dir

alive = True

while True :
    while alive :

        delta = time.process_time() - previous_time
        previous_time = time.process_time()

        Window.update()
        
        input_check()

        turtle.clear()
        
        if new_rock_timer <= 0 :
            n_rock = rock(random.randint(3,7),random.randrange(15,80),random.randint(1,5))
            
            pos = random.randint(1,4)

            speed = (random.randint(10,100)/100) * 4

            dir = random.randrange(1,4)

            if dir == 1 :
                n_rock.position.x = Window.window_width()/2 - Window.window_width()
                n_rock.position.y = (random.randint(1,100)/100) * Window.window_height()
            elif dir == 2 :
                n_rock.position.y = Window.window_height()/2 - Window.window_height()
                n_rock.position.x = (random.randint(1,100)/100) * Window.window_width()
            elif dir == 3 :
                n_rock.position.y = Window.window_height()/2 + Window.window_height()
                n_rock.position.x = (random.randint(1,100)/100) * Window.window_width()
            else :
                n_rock.position.y = Window.window_height()/2 + Window.window_height()
                n_rock.position.x = (random.randint(1,100)/100) * Window.window_width()
            

            new_rock_timer = random.randrange(1,100)/500  
    
            #print("added new rock")
            #print(n_rock.position)
            
            n_rock.velocity = (ship.position - n_rock.position).normalized() * speed
        else :
            new_rock_timer -= delta

        for object in polygon.class_instances :
            turtle.penup()

            if not isinstance(object,ship_main) :
                object.position += object.velocity
            
            if object.position.x < -Window.window_width() or object.position.x > Window.window_width() or object.position.y > Window.window_height() or object.position.y < -Window.window_height() :
                object.free()
                continue
            if isinstance(object,rock) :
                if object.health <= 0 :
                    object.free()
                    continue
                else :
                    object.rotation += object.rotational_velocity

            collision_expections = []
            for collider in polygon.class_instances :
                #print(collider.position.distance_to(object.position))
                if collider.position.distance_to(object.position) < collider.size + object.size :
                    if collider != object :
                        collision_expections.append(collider)

            for possible_collider in collision_expections :
                if isinstance(object,ship_main) and isinstance(possible_collider,rock) :
                    print("died")
                    alive = False
                    pass
                if isinstance(object,bullet) and isinstance(possible_collider,rock) :
                    possible_collider.health -= 2
                    object.free()
                #if isinstance(object,rock) and isinstance(collider,rock) :
                    
                    #collider.velocity = (collider.velocity*-1) + (object.velocity*1)

                    #object.velocity = object.velocity * -1.1

                    
            for point in object.get_shape() :
                #point -= ship.position
                turtle.setpos(point.x,point.y)
                turtle.pendown()
            

        
        Window.update()

        sleep_time = (1/tick_per_second) - delta 
        if sleep_time > 0 :
            time.sleep(sleep_time)
        ticks += 1
        
    ##game over :(


    Window.setup(0,0)

    cmpt_input = input("You died, try again? Y/N: \n")
    if not cmpt_input.lower() == "y" :
        break
    else :
        Window.setup() 
        alive = True
        ship.position = vec2(0,0)
        for object in polygon.class_instances :
            if isinstance(object,rock) :
                object.free()
                
    

    


    
