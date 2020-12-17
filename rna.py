import time

def main():

        '''
        x xxxxxxxxxxxxxxxxxxxxx
        | x                   x
       \/ x                   x
          x                   x
          x                   x
          xxxxxxxxxxxxxxxxxxxxx
        0 y->
        '''
        #open file and read in data
        dat = ""

        with open("input.txt", "r") as input:
            dat = input.read()

        dat = str(bin(int.from_bytes(dat.encode(), 'big')))[2:]

        x_size = 15
        y_size = 54
        fps = .01

        next_acid_location = y_size - 4

        demarker = 33
        demarker_sign = "|"

        border = "X"

        hover_height = 3
        hover_width = 3

        amino_acid = "RNA"
        amino_acids = ["000","001","010","011","100","101","110","111"]
        amino_acids_display = ["111", "110", "101", "100", "011", "010", "001", "000"]
        amino_acids_hovering = [1,1,1,1,1,1,1,1]
        amino_acids_getting = [0,0,0,0,0,0,0,0]
        amino_acids_placing = [0,0,0,0,0,0,0,0]
        amino_acids_returning = [0,0,0,0,0,0,0,0]
        amino_acids_location = [(hover_height, hover_width),(hover_height,hover_width+4),(hover_height,hover_width+8),(hover_height,hover_width+12),(hover_height,hover_width+16),(hover_height,hover_width+20),(hover_height,hover_width+24),(hover_height,hover_width+28)]

        world = [[" " for i in range(0, y_size)]for j in range(0, x_size)]

        waiting = False

        world[0] = [border for i in range(0, y_size)]
        world[x_size-1] = [border for i in range(0, y_size)]
        for i in world:
            i[0] = border
            i[y_size-1] = border



        index = 2
        for i in dat[:demarker-2]:

            world[x_size-3][index] = i;
            index = index + 1

        dat = dat[demarker-2:]



        iter = 0
        for i in amino_acids_location:
            world[i[0]][i[1]-1] = amino_acid[0]
            world[i[0]][i[1]] = amino_acid[1]
            world[i[0]][i[1]+1] = amino_acid[2]
            world[i[0]+1][i[1]-1] = amino_acids_display[iter][0]
            world[i[0]+1][i[1]] = amino_acids_display[iter][1]
            world[i[0]+1][i[1]+1] = amino_acids_display[iter][2]
            iter = iter + 1
        #place and display amino_acids
        print_world(world, demarker, demarker_sign)
        while dat:
            if world[x_size-3][1] == " " and not waiting:
                for i in range(1,demarker):
                    if i < demarker - 1:
                        world[x_size-3][i] = world[x_size-3][i+1]
                    else:
                        world[x_size-3][i] = dat[:1]
                        dat = dat[1:]
            else:
                check = world[x_size-3][2]+world[x_size-3][3]+world[x_size-3][4]
                if check in amino_acids:
                    nextAcid = amino_acids.index(check)
                if amino_acids_hovering[nextAcid]:
                    amino_acids_getting[nextAcid] = 1
                    amino_acids_hovering[nextAcid] = 0
                    waiting = False
                else:
                    #need to wait for the moving amino acid to get back
                    waiting = True

            #All of these are independent of rest of world
            if 1 in amino_acids_getting:
                for i in range(0,len(amino_acids_getting)):
                    #logic to move acid to the lower left corner and remove the three
                    #once there, set placing to 1, zero out that getting,
                    if amino_acids_getting[i] == 1:
                        if amino_acids_location[i][0] < x_size - 5:
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "down")
                        elif amino_acids_location[i][1] > hover_width:
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "left")
                        else:
                            world[x_size-3][1] = " "
                            world[x_size-3][2] = " "
                            world[x_size-3][3] = " "
                            amino_acids_placing[i] = 1
                            amino_acids_getting[i] = 0
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "up", amino_acids_placing[i])
                            

            if 1 in amino_acids_placing:
                #logic to move to next level in protein
                #place the next three letters, once place, change to colored block, set returning to 1, zero out that placing
                for i in range(0,len(amino_acids_placing)):
                    #logic to move acid to the lower left corner and remove the three
                    #once there, set placing to 1, zero out that getting,
                    if amino_acids_placing[i] == 1:
                        if amino_acids_location[i][0] > x_size - 8:
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "up", amino_acids_placing[i])
                        elif amino_acids_location[i][1] < next_acid_location:
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "right", amino_acids_placing[i])
                            waiting = False
                        else:
                            next_acid_location = next_acid_location - 3
                            amino_acids_returning[i] = 1
                            amino_acids_placing[i] = 0

            if 1 in amino_acids_returning:
                #logic to move to end of line
                #once there, set hovering to 1, zero out that returning
                for i in range(0,len(amino_acids_returning)):
                    #logic to move acid to the lower left corner and remove the three
                    #once there, set placing to 1, zero out that getting,
                    if amino_acids_returning[i] == 1:
                        if amino_acids_location[i][0] > hover_height:
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "up")
                        elif amino_acids_location[i][1] > demarker:
                            amino_acids_location[i] = move_acid(world, amino_acids_location[i], "left")
                        else:
                            amino_acids_hovering[i] = 1
                            amino_acids_returning[i] = 0

            #shift over in line
            for i in range (0,len(amino_acids_location)):
                if amino_acids_hovering[i] and world[amino_acids_location[i][0]][amino_acids_location[i][1]-2] == " ":
                    amino_acids_location[i] = move_acid(world, amino_acids_location[i], "left", amino_acids_placing[i])

            #check how filled the protein is, shift down if necessary, figure out next point in line
            if next_acid_location - 3 < demarker:
                for i in range(y_size - 2, demarker, -1):
                     for j in range(x_size-2, 8, -1):
                         world[j][i]= world[j-1][i]
                next_acid_location = y_size - 4
            render_amino_acids(world, amino_acids_location, amino_acids, amino_acids_display, amino_acid, amino_acids_placing, next_acid_location, demarker)
            print_world(world, demarker, demarker_sign)

            time.sleep(fps)

def print_world(world, demarker, demarker_sign):
    lines = "\n\n\n\n\n\n\n\n"
    for i in world:

        iter = 0;
        for j in i:
            if iter == demarker:
                lines = lines + demarker_sign
            else:
                lines = lines + j
            iter = iter + 1
        lines = lines +"\n"
    print(lines)

def move_acid(world, location, direction, carrying = 0):

    ret = location


    if direction == "left":
        ret = (location[0], location[1]-1)

    elif direction == "right":
        ret = (location[0], location[1]+1)

    elif direction == "down":
        ret = (location[0]+1, location[1])

    elif direction == "up":
        ret = (location[0]-1, location[1])

    return ret

def render_amino_acids(world, amino_acids_location, amino_acids, amino_acids_display, amino_acid, amino_acids_placing, next_acid_location, demarker):
    iter = 0
    cycle = 0
    for i in range(1,len(world)-3):#x
        for j in range(1, len(world[0])-2):#y
            if(j > next_acid_location+1 and i > 8):
                cycle = cycle + 1
            elif(j > demarker and i>9):
                cycle = cycle + 1
            else:
                world[i][j]=" "
    for i in amino_acids_location:
        world[i[0]][i[1]-1] = amino_acid[0]
        world[i[0]][i[1]] = amino_acid[1]
        world[i[0]][i[1]+1] = amino_acid[2]
        world[i[0]+1][i[1]-1] = amino_acids_display[iter][0]
        world[i[0]+1][i[1]] = amino_acids_display[iter][1]
        world[i[0]+1][i[1]+1] = amino_acids_display[iter][2]
        if amino_acids_placing[iter]:
            world[i[0]+2][i[1]-1] = amino_acids[iter][0]
            world[i[0]+2][i[1]] = amino_acids[iter][1]
            world[i[0]+2][i[1]+1] = amino_acids[iter][2]
        iter = iter + 1

main()
