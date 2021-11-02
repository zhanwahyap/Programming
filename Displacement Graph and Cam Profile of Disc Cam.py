import turtle,math
myfile = open('NewData.txt')
while True:         #read the file
    max_h = 0
    motion_seg = {}
    myfile.seek(0)
    choice = input('Please input the data set you want to see: ')    #allows user to choose which data set they wish to see
    for lines in myfile:
        split_line = lines.split(',')
        if len(split_line) == 6:                                     #length of the list split_line is 6 iif it is the data about the displacement graph
            while split_line[5].strip() == choice:                   #obtain a dictionary containing the data required for displacement graph based on the data set
                if split_line[2] == 'dwell':
                    motion_seg[int(split_line[0])] = {'ar':int(split_line[1]),'motion':split_line[2],'distance':split_line[3],'curve':split_line[4]}
                else:
                    motion_seg[int(split_line[0])] = {'ar':int(split_line[1]),'motion':split_line[2],'distance':int(split_line[3]),'curve':split_line[4]}
                    if motion_seg[int(split_line[0])]['motion'] == 'rise':
                        max_h += int(split_line[3])
                break
        else:
            if split_line[2].strip() == choice:                      #obtain data of the radius of base circle and follower
                rad_base = int(split_line[0])
                rad_fol = int(split_line[1])

                                                                               ###Drawing of displacement graph###
    turtle.clearscreen()
    scale = 600/max_h
    width = 360
    current_ar = 0
    f_y = [] # f(theta)
    dy = [] #1st derivative of f(theta)
    #drawing of axis
    def axis_x(turtle, distance):   #Drawing of x-axis
        global graph_0
        turtle.pendown()
        turtle.forward(740)
        for j in range(0,distance+10,60):
            global height
            turtle.penup()
            turtle.goto(j-700, -320)
            turtle.pendown()
            turtle.write(int(j/2),align='center', font=('Arial', 9, 'normal'))
        turtle.penup()
        turtle.goto(-360, -350)
        turtle.pendown()
        turtle.write('Cam rotation', font=('Arial', 11, 'normal'))
        turtle.penup()

    def axis_y(turtle, distance):   #Drawing of y-axis
        position = turtle.position()
        turtle.pendown()
        turtle.forward(distance*scale)
        turtle.setposition(position)
        y_num = 0
        for j in range(0,int((distance+1)*scale),int(distance*scale/10)):
            turtle.penup()
            turtle.goto(-705 ,j-300)
            turtle.pendown()
            turtle.write(y_num, align='right', font=('Arial', 9, 'normal'))
            y_num += int(distance/10)
        turtle.penup()

    screen = turtle.Screen()
    screen.screensize(1000,500)
    screen.title('Displacement Graph & Cam Profile')


    axes = turtle.Turtle()  #axes is the turtle for drawing axis
    axes.hideturtle()
    axes.penup()
    axes.goto(-700,-300)
    graph_0 = axes.position() #0,0 for displacement graph
    axes.speed(0)
    axis_x(axes, 740)


    axes.penup()
    axes.setposition(graph_0)
    axes.setheading(90)
    axis_y(axes, max_h)

    axes.penup()
    axes.goto(-740, -100)
    axes.pendown()
    axes.write('D\ni\ns\np\nl\na\nc\ne\nm\ne\nn\nt',font=('Arial', 11, 'normal')) #y-axis label

    h=0

    def dwell(turt, ar):                                                                     #function if the motion type is dwell
        global current_ar,f_y,h
        for i in range(current_ar, current_ar + ar):
            if f_y == []:                                                                    #dwell line if dwell is the starting curve
                turt.goto(i*2-700, -300)
                f_y.append(0)
                dy.append(0)
            else:                                                                            #dwell line if dwell is after a rise or return
                turt.goto(i*2-700, f_y[current_ar-1]*scale - 300)  
                f_y.append(f_y[current_ar-1])
                dy.append(0)
        current_ar += ar
        

    def rise(turt, ar, distance, curve):                                                     #function if the motion type is rise
        global current_ar, f_y,h
        for i in range(current_ar, current_ar + ar):
            x = i - current_ar
            if curve == 'constant acceleration':                                             #rise curve if curve type is constant acceleration
                if i < current_ar + ar/2:
                    y = 2 * distance * (x / ar) ** 2 + h
                else: 
                    y = distance * (1 - 2 * (1 - x / ar) ** 2) + h
                dy.append(4 * distance * x / (ar ** 2))
            elif curve == 'simple harmonic':                                                 #rise curve if curve type is simple harmonic
                y = distance * (1 - math.cos(math.pi * x / ar)) / 2 + h
                dy.append((math.pi * distance / (2 * ar)) * math.sin(math.pi * x / ar))
            else:                                                                            #rise curve if curve type is cycloidal motion
                y = distance * (x / ar - math.sin(2 * math.pi * x / ar) / (2 * math.pi)) + h
                dy.append((distance / ar) * (1 - math.cos(2 * math.pi * x / ar)))
            turt.goto(i*2 - 700,y * scale - 300)
            f_y.append(y)
        current_ar += ar
        h = y

    def fall(turt, ar, distance, curve):                                                     #function if the motion type is return
        global current_ar, f_y,h
        for i in range(current_ar, current_ar + ar):
            x = i - current_ar
            if curve == 'constant acceleration':                                             #return curve if curve type is constant acceleration
                if i < current_ar + ar/2:
                    y = distance * (1 - 2 * (x / ar) ** 2) + (h - distance)
                else: 
                    y = 2 * distance * (1 - x / ar) ** 2  + (h - distance)
                dy.append(-(4 * distance * x / (ar ** 2)))
            elif curve == 'simple harmonic':                                                 #return curve if curve type is simple harmonic
                y = distance * (1 + math.cos(math.pi * x / ar)) / 2  + (h - distance)
                dy.append(-((math.pi * distance / (2 * ar)) * math.sin(math.pi * x / ar)))
            else:                                                                            #return curve if curve type is cycloidal motion
                y = distance * (1 - x / ar + math.sin(2 * math.pi * x / ar) / (2 * math.pi)) + (h - distance)
                dy.append(-((distance / ar) * (1 - math.cos(2 * math.pi * x / ar))))
            turt.goto(i*2-700,y*scale - 300)
            f_y.append(y)
        current_ar += ar
        h = y

    def graph(turt, ar, motion, distance = 0, curve = 0):                #function to be called when drawing displacement graph, distance and curve defaulted to 0 if motion is dwell 
        if motion == 'dwell':
            dwell(turt, ar)
        elif motion == 'rise':
            rise(turt, ar, distance, curve)
        else:
            fall(turt, ar, distance, curve)

    t = turtle.Turtle()             #t is the turtle for drawing the displacement graph
    t.hideturtle()
    t.penup()
    t.setposition(graph_0)
    t.pencolor('red')
    t.pen(pensize=2)
    t.speed(0)
    t.pendown()

    num_seg = len(motion_seg)
    for i in range(1, num_seg + 1):
        if motion_seg[i]['motion'] != 'dwell':   
            graph(t, motion_seg[i]['ar'], motion_seg[i]['motion'], motion_seg[i]['distance'], motion_seg[i]['curve'])
        else:
            graph(t, motion_seg[i]['ar'], motion_seg[i]['motion'])       
    print('Segment Number      Angular Range      Motion Type      Displacement      Curve Type')
    for key in sorted(motion_seg):
        print('{:^14d}      {:^13d}      {:^11s}      {:^12}      {:^10s}'.format(key,motion_seg[key]['ar'],motion_seg[key]['motion'],motion_seg[key]['distance'],motion_seg[key]['curve']))
    print('Radius of base circle:',rad_base)
    print('Radius of follower:',rad_fol)

    cam_scale = 50/rad_fol      #cam is the turtle for drawing the cam profile
    cam = turtle.Turtle()
    cam.hideturtle()
    cam.pencolor('blue')
    cam.penup()
    cam.goto(450,0)
    cam.speed(0)
    cam.pendown()
    cam.dot(3) 
    start_x,start_y = cam.position() #center of base circle
    cam.penup()
    cam.forward(rad_base * cam_scale)
    cam.pendown()
    cam.left(90)
    cam.right(180)
    cam.fillcolor('blue')
    cam.begin_fill()
    cam.circle(rad_fol * cam_scale) #drawing the follower
    cam.end_fill()
    cam.right(180)
    end_x,end_y = cam.position()
    cam.pencolor('black')
    cam.fillcolor('orange')
    cam.begin_fill()
    for x in range(360):         #drawing the cam profile
        R = rad_base + rad_fol + f_y[x]
        X = R * math.cos(math.radians(x))
        Y = R * math.sin(math.radians(x))
        Tx = math.cos(math.radians(x)) * dy[x] - R * math.sin(math.radians(x))
        Ty = math.sin(math.radians(x)) * dy[x] + R * math.cos(math.radians(x))
        Nx = -Ty
        Ny = Tx
        m = math.sqrt((Nx ** 2) + (Ny ** 2))
        nx = Nx / m
        ny = Ny / m
        Px = X + rad_fol * (nx)
        Py = Y + rad_fol * (ny)
        cam.goto(Px*cam_scale+start_x,Py*cam_scale+start_y)
    cam.goto(end_x,end_y)
    cam.end_fill()
    cam.pencolor('red')
    cam.circle(rad_base * cam_scale)  #drawing the base circle
myfile.close()    
