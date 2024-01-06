import pygame
import random
import math
import time
width,height, =(800,500)

fps=30
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((width,height))
clock= pygame.time.Clock()

draw_trails=True

class dot(pygame.sprite.Sprite):
    def __init__(self,center,radius,color):
        pygame.sprite.Sprite.__init__(self)
        self.floatx=center[0]
        self.floaty=center[1]
        self.radius=radius
        self.image=pygame.Surface((radius*2,radius*2))
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        pygame.draw.circle(self.image,color,(radius,radius),radius)
        self.rect.center=center
        self.last_update=pygame.time.get_ticks()
        self.frame_lenght=100
    def update(self):
        self.last_update=pygame.time.get_ticks()
    def change_color(self,rgb):
        pygame.draw.circle(self.image, rgb, (self.radius, self.radius), self.radius)

class Circle(pygame.sprite.Sprite):
    def __init__(self,center,radius,angle,color,speed):
        pygame.sprite.Sprite.__init__(self)
        self.floatx=center[0]
        self.floaty=center[1]

        self.radius=radius

        self.angle=angle
        self.speed=speed

        #preload red and green cricles named red_image and green_image
        self.green_image=pygame.Surface((radius*2,radius*2))
        self.green_image.fill(white)
        self.green_image.set_colorkey(white)
        pygame.draw.circle(self.green_image,color,(radius,radius),radius)
        self.red_image=pygame.Surface((radius*2,radius*2))
        self.red_image.fill(white)
        self.red_image.set_colorkey(white)
        pygame.draw.circle(self.red_image,red,(radius,radius),radius)

        #set initial image
        self.image=self.green_image

        self.rect=self.image.get_rect()
        self.rect.center=center

        self.line_point=self.rect.center

        self.next_point=get_next_intercept((self.floatx,self.floaty), self.angle)
        self.last_d = 0


    def update(self):
        #trail
        '''
        if self.rect.center not in trails_pos:
            trails_pos.append(self.rect.center)
            trails.add(Trail(self.rect.center))
        '''
        #move
        self.move_to((self.floatx+self.speed*math.cos(self.angle),self.floaty-self.speed*math.sin(self.angle)))
        '''if in_elipse(self.rect.x,self.rect.y):
            self.image=self.green_image
        else:
            self.image=self.red_image'''
        if get_distance((self.floatx,self.floaty), self.next_point)<=self.speed:
            self.angle=reflentoin_angle(slope_elipse(self.next_point), self.angle)
            self.angle+=math.pi
            remaining_distance=self.speed-get_distance((self.floatx,self.floaty), self.next_point)
            dx=remaining_distance*math.cos(self.angle)
            dy=(height-self.next_point[1])-linear(math.tan(self.angle),self.next_point[0]+dx,(height-self.next_point[1])-(math.tan(self.angle)*self.next_point[0]))
            self.move_to((self.next_point[0]+dx,self.next_point[1]+dy))
            last_point=self.next_point
            self.next_point=get_next_intercept((self.floatx, self.floaty), self.angle)
            line_lst.append((last_point,self.next_point))
            self.last_distance=get_distance((self.floatx,self.floaty), self.next_point)

    def change_color(self,rgb):
        pygame.draw.circle(self.image, rgb, (self.radius, self.radius), self.radius)

    def move_to(self,*args):
        (x, y) ,= args

        #update floats
        self.floatx += (x - self.floatx)
        self.floaty += (y - self.floaty)
        self.rect.center = (math.floor(self.floatx),math.floor(self.floaty))

class Elipse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((width,height))
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        pygame.draw.ellipse(self.image,green,self.rect,1)

class Trail(dot):
    def __init__(self,center):
        spread=0
        time_spread=3
        dot.__init__(self,center,1,(255,0,0))
        self.created=frame_count
        self.tot_time=10+random.randint(-time_spread,time_spread)

    def update(self):
        pass

def top_elipse(x):
    try:
        return ((height/2)*(math.sqrt(-((((x-width/2))/(width/2))**2-1)))+(height/2))
    except ValueError:
        return width/2
def bottem_elipse(x):
    try:
        return ((height/2)*(-math.sqrt(-(((x-(width/2))/(width/2))**2-1)))+(height/2))
    except ValueError:
        return width/2

def get_distance(x_y1,x_y2):
    return (math.sqrt((x_y1[0]-x_y2[0])**2+(x_y1[1]-x_y2[1])**2))

def in_elipse(x,y):
    y=height-y
    try:
        if not y>top_elipse(x) and not y<bottem_elipse(x):
            return True
        else:
            return False
    except ValueError:
        return False

def slope_elipse(x_y):
    x,y ,=x_y
    y=height-y
    try:
        return (((((height/2)**2*2*((x-(width/2))/(width/2))*(1/(width/2)))/(-2*((y-(height/2))/(height/2)))))/(height/2))
    except ZeroDivisionError:
        return 10000000000

def linear(m,x,b):
    return m*x+b

def reflentoin_angle(slope,angle):
    return (math.atan(-1/slope)+(math.atan(-1/slope)-angle))

def get_next_intercept(point,angle):
    point=(point[0],height-point[1])
    if angle==math.pi/2 or angle==3*math.pi/2:
        return (point[0],height-(top_elipse(point[0]) if angle==math.pi/2 else bottem_elipse(point[0])))
    elif math.cos(angle)==0 and point[1]==height/2:
        x=width/2
    else:
        slope=math.tan(angle)
        a=(-(height/2)**2/(width/2)**2-slope**2)
        b=(((height/2)**2*2*(width/2))/(width/2)**2)+2*(height/2)*slope+slope**2*2*point[0]-2*point[1]*slope
        c=-(height/2)**2-2*(height/2)*slope*point[0]+(height/2)*point[1]-slope**2*point[0]**2+point[1]*slope*point[0]+(height/2)*point[1]+point[1]*slope*point[0]-point[1]**2
        s=(-b+math.sqrt(b**2-4*a*c))/2*a
        s2=(-b-math.sqrt(b**2-4*a*c))/2*a
        if math.cos(angle)>=0:
            x=(-b-math.sqrt(b**2-(4*a*c)))/(2*a)
        else:
            x=(-b+math.sqrt(b**2-(4*a*c)))/(2*a)
    lin_y=linear(math.tan(angle),x,(point[1]-math.tan(angle)*point[0]))
    if lin_y>height/2:
        y=top_elipse(x)
    elif lin_y==height/2:
        y=height/2
    else:
        y=bottem_elipse(x)
    return (x,height-y)

focus1=(math.sqrt(((width)/2)**2-((height)/2)**2)+width/2,height/2)
focus0=(width-(math.sqrt(((width)/2)**2-((height)/2)**2)+width/2),height/2)

things_group=pygame.sprite.Group()
trails=pygame.sprite.Group()
things_group.add(dot(focus1,7,red))
things_group.add(dot(focus0,7,red))
things_group.add(Elipse())
trails_pos=[]
line_lst=[]

circles=pygame.sprite.Group()
#circles.add(Circle((510,253.18987169553748),5,3.853972602954816,green,5))
#n=15
#[circles.add(Circle((focus0[0],focus0[1]),2,i*2*math.pi/n,green,3)) for i in range(n)]
#circles.add(Circle((200,200),5,(11/32)*2*math.pi+.3,green,5))
circles.add(Circle((440,253.18987169553748),5,4.24,green,5))

#circles.add(Circle((101,100),5,.3,green,5))


frame_count=0
last_fps_update=time.time()
last_fps=0

running=True

while running:
    clock.tick(fps)
    #prosses input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            pass
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                pass
            if event.key==pygame.K_v:
                pass
            if event.key==pygame.K_b:
                pass


    #update
    things_group.update()
    circles.update()

    #draw
    screen.fill(black)
    if line_lst and draw_trails:
        for i in line_lst:
            pygame.draw.line(screen,red,i[0],i[1])
    things_group.draw(screen)
    circles.draw(screen)
    trails.draw(screen)


    pygame.display.flip()
    frame_count+=1
    #pirnt fps
    if last_fps_update+1<=time.time():
        #print(frame_count-last_fps)
        last_fps_update=time.time()
        last_fps=frame_count


