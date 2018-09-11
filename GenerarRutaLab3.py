Lat1= -33.4503685
Lon1= -70.6897731
Alt = 10
AltMax = 20
perimetroLat= [-33.4506, -33.4506, -33.4500, -33.4500];
perimetroLon= [-70.6897, -70.6894, -70.6894, -70.6897];
largo=0
ancho=0
dron = [0, 0, 4, Alt]
area=0
completitud= 0
trayectoria= []

import numpy as np

def SetearParametros():
    Lat1 = input("Latitud de Despegue: ")
    Lon1 = input("Longitud de Despegue: ")
    Alt = input("Altitud de Vuelo: ")
    AltMax = input("Altitud Max de Vuelo: ")
    print("A continuacion se le pedira el perimetro de vuelo:")

    i = 1
    while i <= 4:
        print("Latitud del punto: " + {i})
        perimetroLat[i]=input()
        print("Longitud del punto: " + {i})
        perimetroLon[i]=input()
        i += 1

def EscribirParametros():
    print(Lat1, Lon1)
    i = 0
    while i < 4:
        print(perimetroLat[i], perimetroLon[i])
        i += 1

def ConstruirGrid():
    global ancho
    global largo
    ancho= int((abs(perimetroLon[0])- abs(perimetroLon[1]))/0.00005435)
    largo= int((abs(perimetroLat[1]) - abs(perimetroLat[2])) / 0.0000416 )
    valoresGrid = np.zeros((ancho,largo), dtype=int)
    return valoresGrid

def GenerarWaypoints():
    puntos = largo*ancho
    waypoints= np.zeros((puntos,2), dtype=float)
    lon_i=perimetroLon[0]
    lat_i=perimetroLat[2]
    i =0
    while i<puntos:
        waypoints[i][0]= lat_i-(int(i%largo)*0.0000416 + 0.0000208)
        waypoints[i][1] = lon_i + (int(i / largo) * 0.00005435 - 0.0000272)
        print(waypoints[i][0], "+", waypoints[i][1])
        print("everything okay?")
        i += 1
    return waypoints

def EscribirWaypoints(ruta, waypoints):
    f = open(ruta, "w+")
    i=1
    init ="QGC WPL 110\n"
    initialPoint="0	1	0	16	0	0	0	0	"+ str(Lat1)+"	"+str(Lon1) +"	"+str(Alt)+"   1\n"
    f.write(init)
    f.write(initialPoint)
    for x in trayectoria:
        punto= x[0]*largo + x[1]
        latitudPunto= str(waypoints[punto][0])
        longitudPunto= str(waypoints[punto][1])
        alturaPunto= str(x[2])
        Punto= str(i)+"	1	0	16	0	0	0	0	"+latitudPunto +"	"+longitudPunto +"	"+ alturaPunto+"   1\n"
        f.write(Punto)
        i+=1
    f.close
def IngresarObtaculo():
    obstaculos= int(input("ingresar el numero de obstaculos:"))
    vertices = np.zeros((4, 2), dtype=int)
    global Grid
    i=0
    while i<obstaculos:


        print("Coordenadas Centro")
        pLat= float(input("ingresar latitud:"))
        pLon= float(input("ingresar longitud:"))
        alturaObs = int(input("ingresar altura Obstaculo (mt): "))
        dim= float(input("Ingresar Dimensión (mt): "))
        DimLon = (dim * (0.00005435/5)) / 5  # Cuantos grados de Lon es esto
        DimLat = (dim * (0.0000416/5)) / 5 # Cuantos Grados de Lat es esto.

        #Vertice 1:
        vertices[0][0] = int(-((pLon+ DimLon/2) -perimetroLon[1]) / 0.00005435)
        vertices[0][1] = int(-((pLat+ DimLat/2) - perimetroLat[2]) / 0.0000416 )
        # Vertice 1:
        vertices[1][0] = int(-((pLon+ DimLon/2) -perimetroLon[1]) / 0.00005435)
        vertices[1][1] = int(-((pLat- DimLat/2) - perimetroLat[2]) / 0.0000416 )
        # Vertice 1:
        vertices[2][0] = int(-((pLon- DimLon/2) -perimetroLon[1]) / 0.00005435)
        vertices[2][1] = int(-((pLat+ DimLat/2) - perimetroLat[2]) / 0.0000416 )
        # Vertice 1:
        vertices[3][0] = int(-((pLon- DimLon/2) -perimetroLon[1]) / 0.00005435)
        vertices[3][1] = int(-((pLat- DimLat/2) - perimetroLat[2]) / 0.0000416 )

        x1= vertices[0][0]-1
        y1= vertices[0][1]-1
        y2= vertices[0][1]-1
        x2= vertices[0][0]-1

        for x in vertices:
            if x[0]!=x1:
                if x[0]<x1:
                    x2= x1
                    x1= x[0]
                else:
                    x2= x[0]
            if x[1]!=y1:
                if x[1]<y1:
                    y2=y1
                    y1=x[1]
                else:
                    y2=x[1]
            #Realizar los cambios
        print("X1: ", x1, " x2: ", x2, " y1: ", y1, " y2: ", y2)
        while x1<= x2:
            print("x1 vale: ", x1)
            if x1>=0 and x1<ancho:
                aux= y1
                while aux<=y2:
                    if aux>=0 and aux<largo:
                        if alturaObs < AltMax:
                                print("x: ", x1, "y: ", aux)
                                Grid[x1][aux] = 3
                        else:
                                Grid[x1][aux] = 1
                    aux+=1
            x1 += 1

        i+=1


        #Cambiar los valores entre vertices por 1 o 2 si se puede sobrevolar!
    return vertices

"""LOGICA DE EVACIÓN DE OBSTACULOS"""


"""Ejecutar Giros"""
def girarDerecha():
    global dron
    dir= dron[2]
    if dir==1:
        dron[2]= 4
    if dir==2:
        dron[2]= 3
    if dir==3:
        dron[2]= 1
    if dir==4:
        dron[2]= 2

def girarIzquierda():
    global dron
    dir= dron[2]
    if dir==1:
        dron[2]= 3
    if dir==2:
        dron[2]= 4
    if dir==3:
        dron[2]= 2
    if dir==4:
        dron[2]= 1

def avanzar():
    global dron
    dir = dron[2]
    if dir == 1:
        dron[0] -= 1
    if dir == 2:
        dron[0] += 1
    if dir == 3:
        dron[1] -= 1
    if dir == 4:
        dron[1] += 1
    if Grid[dron[0]][dron[1]]==3:
        dron[3]=AltMax
    else:
        dron[3]=Alt
"""¿Es posible Girar/Avanzar?"""
def puedoGirarDerecha():
    dir= dron[2]
    if dir==1:
        if dron[1] < largo-1:
            if Grid[dron[0]][dron[1]+1]==0 or Grid[dron[0]][dron[1]+1]==3:
                return True
    if dir==2:
        if dron[1] > 0:
            if Grid[dron[0]][dron[1] - 1] == 0 or Grid[dron[0]][dron[1] - 1] == 3:
                return True
    if dir==4:
        if dron[0]< ancho-1:
            if Grid[dron[0] + 1][dron[1]] == 0 or Grid[dron[0] + 1][dron[1]]==3:
                return True
    if dir==3:
        if dron[0] > 0:
            if Grid[dron[0]-1][dron[1]] == 0 or Grid[dron[0]-1][dron[1]]==3:
                return True
    else:
        return False

def puedoGirarIzquierda():
    dir= dron[2]
    if dir==1:
        if dron[1]>0:
            if Grid[dron[0]][dron[1]-1]==0 or Grid[dron[0]][dron[1]-1]==3:
                return True
    if dir==2:
        if dron[1] <largo-1:
            if Grid[dron[0]][dron[1] + 1] == 0 or Grid[dron[0]][dron[1] + 1] == 3:
                return True
    if dir==4:
        if dron[0] > 0:
            if Grid[dron[0] - 1][dron[1]] == 0  or Grid[dron[0] - 1][dron[1]] == 3:
                return True
    if dir==3:
        if dron[0] < ancho-1:
            if Grid[dron[0] +1][dron[1]] == 0 or Grid[dron[0] +1][dron[1]] == 3:
                return True
    else:
        return False

def puedoAvanzar():
    dir= dron[2]
    if dir==1:
        if dron[0] > 0:
            if Grid[dron[0]-1][dron[1]]==0 or Grid[dron[0]-1][dron[1]]==3:
                return True
    if dir==2:
        if dron[0] < ancho-1:
            if Grid[dron[0]+1][dron[1]] == 0 or Grid[dron[0]+1][dron[1]]==3:
                return True
    if dir==3:
        if dron[1] > 0:
            if Grid[dron[0]][dron[1]-1] == 0 or Grid[dron[0]][dron[1]-1] == 3:
                return True
    if dir==4:
        if dron[1] < largo-1:
            if Grid[dron[0]][dron[1]+1] == 0 or Grid[dron[0]][dron[1]+1] == 3:
                return True
    else:
        return False

"""PARA VOLVER ATRAS"""
def traerDron(x, y, h):
    global dron
    global trayectoria
    xi=dron[0]  #Pocición actual.
    yi=dron[1]
    dron[0] = x #Reasigno la posición del Dron
    dron[1] = y
    tray= trayectoria.copy()
    tray.reverse()#Invertir lista de puntos coordenados para recorrer al reves
    print("TRAYECTORIA DE RETORNO")
    meta= tray.index((x, y, h)) #Ultima ocurrencia del punto de destino
    actual=0

    while actual<meta:
        a= tray[actual][0] #Revisar desde donde estoy ahora
        b= tray[actual][1]
        j= actual + 1
        atajo=False
        while j<=meta:
            t=tray[j][0]
            v=tray[j][1]
            if puedoLlegar(t,v,a,b):    #Si puedo llegar lo cambio.
                actual=j
                atajo=True
            j+=1
        if atajo==False:
            actual+=1
        print(tray[actual], "    ")
        trayectoria.append((tray[actual][0],tray[actual][1],AltMax ))

def puedoLlegar(x,y,a,b):
    if a+1==x and b==y:
        return True
    if a-1==x and b==y:
        return True
    if a==x and b+1==y:
        return True
    if a==x and b-1==y:
        return True
    else:
        return False



    dron[0]=x
    dron[1]=y

"""AREA A RECORRER"""
def calcularArea():
    i=0
    global area
    while i<ancho:
        j=0
        while j< largo:
            if Grid[i][j]==0 or Grid[i][j]==3:
                area+=1
            j+=1
        i+=1

"""Función que recorre la Grid y genera la trayectoria"""
def recorrerGrid():
    global Grid
    x= dron[0]
    y= dron[1]
    a= x
    b= y
    h=0
    if Grid[x][y]==3:
        h = AltMax
    else:
        h= Alt

    trayectoria.append((x,y,h)) #Agrego el punto en que estoy a los puntos recorridos
    Grid[x][y]= 2  #Marco el punto en que estoy.<<
    global completitud
    completitud+=1
    if puedoAvanzar():  #Verifico si puedo avanzar.
        avanzar()       #Si puedo, Avanzo.
        if Grid[dron[0]][dron[1]]==3 and h==Alt:
            trayectoria.append((a, b, AltMax))  #Puede que haya que crear esto
        recorrerGrid()  #Llamo recursivamente a la función.
        if(completitud!=area):
            traerDron(x, y, h)
    if puedoGirarDerecha(): #Verifico si puedo girar a la derecha.
        print("giro derecha")
        girarDerecha()  #Si puedo, Giro.
        avanzar()
        if Grid[dron[0]][dron[1]] == 3 and h == Alt:
            trayectoria.append((a, b, AltMax))  # Puede que haya que crear esto
        recorrerGrid()  #Llamo recursivamente a la función.
        if (completitud != area):
            traerDron(x, y, h)
    if puedoGirarIzquierda(): #Verifico si puedo girar a la derecha.
        print("giro izquierda")
        girarIzquierda() #Si puedo, Giro.
        avanzar()
        if Grid[dron[0]][dron[1]] == 3 and h == Alt:
            trayectoria.append((a, b, AltMax))  # Puede que haya que crear esto
        recorrerGrid()   #Llamo recursivamente a la función.
    return

""" MAIN """

Grid= ConstruirGrid()
Waypoints= GenerarWaypoints()
"""EscribirWaypoints("puntosGeneradosPython.waypoints", Waypoints)"""
"""vertices= IngresarObtaculo()"""
IngresarObtaculo()
print(Grid)
calcularArea()
recorrerGrid()
print(Grid)
print(trayectoria)
waypoints = GenerarWaypoints()
EscribirWaypoints("Magia.waypoints", waypoints)
print("end")