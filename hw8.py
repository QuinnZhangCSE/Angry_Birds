#Import statements
from Pig import *
from Bird import *
from Barrier import *
import math

#Functions
def collide(bird, other): #Checks if the pig collides with another object
    if abs(bird.radius-other.radius) <= math.sqrt((bird.x-other.x)**2+(bird.y-other.y)**2) and math.sqrt((bird.x-other.x)**2+(bird.y-other.y)**2) <= bird.radius+other.radius:
    #Magic, whoever thought of this is genius
        return True
    return False

def out(bird): #Checks if bird goes out of bound
    if bird.x-bird.radius < 0 or bird.y-bird.radius < 0 or bird.x+bird.radius > 1000 or bird.y+bird.radius > 1000:
        return True
    return False

def slow(bird): #Checks if the bird is too slow
    if math.sqrt(bird.dx**2 + bird.dy**2) < 6:
        return True
    return False

def enter(t,bird): #Prints out the info of the new bird entering
    print("Time {}: {} starts at ({},{})".format(t,bird.name, bird.x, bird.y))
    

#The list of objects
pigs = []
birds = []
barriers = []

#Askes the user for inputs
bd_f = input("Enter the name of the bird file => ")
print(bd_f)
pg_f = input("Enter the name of the pig file => ")
print(pg_f)
br_f = input("Enter the name of the barrier file => ")
print(br_f)

#Reads the file and add them to the list as objects
for line in open(bd_f):
    line = line.strip()
    b = []
    b = line.split("|")
    birds.append(Bird(b[0],b[1],b[2],b[3],b[4],b[5],b[6]))
for line in open(pg_f):
    line = line.strip()
    p = []
    p = line.split("|")
    pigs.append(Pig(p[0],p[1],p[2],p[3]))
for line in open(br_f):
    line = line.strip()
    b = []
    b = line.split("|")
    barriers.append(Barrier(b[0],b[1],b[2],b[3],b[4]))

#Prints out the initial information
print("")
print("There are {} birds:".format(len(birds)))
for b in birds:
    print("    " + str(b))
print("")
print("There are {} pigs:".format(len(pigs)))
for p in pigs:
    print("    " + str(p))
print("")
print("There are {} barriers:".format(len(barriers)))
for b in barriers:
    print("    " + str(b))
print("")
    
#The code that stimulates the run
time = 0
bird = birds[0]#Makes initial settings
enter(0,bird)
while len(birds) != 0 and len(pigs) != 0: #If there are no more pigs or no more birds, loop will stop
    time += 1
    bird.fly()
    if out(bird): #If the bird goes out
        print("Time {}: {} at ({:.1f},{:.1f}) has left the game".format(time,bird.name,bird.x,bird.y))
        birds.pop(0)
        if len(birds) == 0:
            print("Time {}: No more birds. The pigs win!".format(time))
            print("Remaining pigs:")
            for p in pigs:
                print(p.name)
            break
        bird = birds[0]
        enter(time,bird)
    for p in pigs:
        if collide(bird,p): #If bird hits pig
            print("Time {}: {} at ({:.1f},{:.1f}) pops {}".format(time,bird.name,bird.x,bird.y,p.name))
            bird.dx /= 2
            print("Time {}: {} at ({:.1f},{:.1f}) has (dx, dy) = ({:.1f},{:.1f})".format(time,bird.name,bird.x,bird.y,bird.dx,bird.dy))
            if slow(bird):
                print("Time {}: {} at ({:.1f},{:.1f}) with speed {:.1f} stops".format(time,bird.name,bird.x,bird.y,math.sqrt(bird.dx**2 + bird.dy**2)))               
            pigs.remove(p)
            if len(pigs) == 0:
                print("Time {}: All pigs are popped. The birds win!".format(time))
                break
            if slow(bird): #This was not written together witht the code at top in order to prevent the situation where pigs and birds both gets poped
                birds.pop(0)
                bird = birds[0]
                enter(time,bird)
    for b in barriers:
        if collide(bird,b):
            b.hp -= bird.mass * (bird.dx**2 + bird.dy**2) #decrease the strength by mv^2
            if b.hp < 0: #prevent the strength from falling to zero
                b.hp = 0
            print("Time {}: {} at ({:.1f},{:.1f}) hits {}, Strength {:.1f}".format(time,bird.name,bird.x,bird.y,b.name,b.hp))
            if b.hp == 0:
                print("Time {}: {} crumbles".format(time,b.name))
                for i in range(len(barriers)):
                    if b.name == barriers[i].name:
                        barriers.pop(i)
                print("Time {}: {} at ({:.1f},{:.1f}) has (dx, dy) = (0.0,0.0)".format(time,bird.name,bird.x,bird.y))
            print("Time {}: {} at ({:.1f},{:.1f}) with speed 0.0 stops".format(time,bird.name,bird.x,bird.y))
            birds.pop(0)
            bird = birds[0]
            enter(time,bird)