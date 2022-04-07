#-*- coding:utf-8 -*-
from random import seed
from random import randint
"""
1. FUNCIONES
"""

"""
1.1 FUNCIONES GENERALES
"""
def validarEntero (pregunta, minimo, maximo, usoMinimo, usoMaximo):
    validarDeNuevo = 1;
    respuesta = "";
    while (validarDeNuevo == 1):
        validarDeNuevo = 0;
        respuesta = input(pregunta);
        if(len(respuesta) == 0):
          validarDeNuevo = 1;
        else:
          for letra in respuesta:
              esCifra = 0;
              for cifra in range(10):
                  if(letra == str(cifra)):
                      esCifra = 1;
                      break;
              if(esCifra == 0):
                  validarDeNuevo = 1;
          if(validarDeNuevo == 0):
              respuesta = int(respuesta);
              if(usoMinimo != 0):
                  if(minimo > respuesta):
                      validarDeNuevo = 1;
              if(usoMaximo != 0):
                  if(maximo < respuesta):
                      validarDeNuevo = 1;
    return respuesta;

#parametros[0] = índiceAModificar
#parametros[1] = nuevaFila
#parametros[2] = nuevaColumna

def modificarFichas(parametros):
  lista = [];
  for i in range(len(fichas)):
    if(i != parametros[0]):
      lista.append(fichas[i]);
  lista.append([fichas[parametros[0]][0], parametros[1],parametros[2]]);
  return lista;
def modificarFichasEnemigas(parametros):
  lista = [];
  for i in range(len(fichasEnemigas)):
    if(i != parametros[0]):
      lista.append(fichasEnemigas[i]);
  lista.append([fichasEnemigas[parametros[0]][0], parametros[1],parametros[2],0]);
  return lista;

#CORONAR REINA DE BOT
def coronarEnemigas(indice):
  lista = [];
  for i in range(len(fichasEnemigas)):
    if(i != indice):
      lista.append(fichasEnemigas[i]);
  lista.append([True, fichasEnemigas[indice][1],fichasEnemigas[indice][2],0]);
  return lista;

#CORONAR REINA DE JUGADOR
def coronarJugador(indice, nuevaFila, nuevaColumna):
  for i in range(len(fichas)):
    if(i == indice):
      fichas[i][0] = True;
  return [indice, nuevaFila, nuevaColumna];


"""
1.2 FUNCIONES DE INICIALIZACIÓN
"""
def inicializarFichas():
  #formato de fila de fichas:
  ## booleano que indica si es reina (True) o no (False)
  ## columna (0 al 7)
  ## fila (0 al 7)
  ## SOLO EN ENEMIGAS: peso de probabilidad
  for i in range(1,8,2):
    fichas.append([False,6,i]);
    fichasEnemigas.append([False,0,i,0]);
    fichasEnemigas.append([False,2,i,0]);
  for i in range(0,8,2):
    fichas.append([False,7,i]);
    fichas.append([False,5,i]);
    fichasEnemigas.append([False,1,i,0]);

def inicializacionDelResto():
  
  #BIENVENIDA 
  nombreDeUsuario = input("Ingrese su nombre o nickname, por favor: ");
  print("""\nBIENVENIDO %s A NUESTRO JUEGO DE DAMAS
  LAS REGLAS SON LAS SIGUIENTES:

  - El tablero es de 8 x 8 casillas.
  - Se puede comer solo hacia adelante.
  - No hay soplado (si no comes una ficha, no se eliminará la tuya).
  - No se puede comer en cadena (sucesivamente). 
  - Las damas reinas pueden retroceder y moverse por toda la diagonal.

  ESPEREMOS DISFRUTES DE LA EXPERIENCIA
  POSTDATA: NUESTRO AMIG@ CHECKRI ES A VECES UN POCO ESPECIAL, TENLE PACIENCIA.
  """ %(nombreDeUsuario.upper()));
  
  vuelveAPreguntar = True;
  while(vuelveAPreguntar):
    vuelveAPreguntar = False;
    colorDeUsuario = input("Que color de fichas desea N(negras) o B(blancas): ");
    if(len(colorDeUsuario) == 0):
      vuelveAPreguntar = True;
    elif(len(colorDeUsuario) > 1):
      vuelveAPreguntar = True;
    elif (colorDeUsuario[0] != 'n' and colorDeUsuario[0] != 'N' and colorDeUsuario[0] != 'b' and  colorDeUsuario[0] != 'B' ):
      vuelveAPreguntar = True;
  
  if (colorDeUsuario[0] == 'n' or colorDeUsuario[0] == 'N'):
    colorDeUsuario = 1;
    colorDeFichaBot = 0;
  else:
    colorDeUsuario = 0;
    colorDeFichaBot = 1;
    
  return [colorDeUsuario,colorDeFichaBot,nombreDeUsuario];
  

"""
1.3 FUNCIONES DE AI
"""
def sorteaConPesos(listaDePesos):
  #sumarPesos
  totalPesos = 0;
  for peso in listaDePesos:
    totalPesos += peso;
  seed();
  indiceSorteado = randint(0,totalPesos);
  
  #llegar al indice:
  sumador = 0;
  contador = 0;
  while(sumador < indiceSorteado):
    #print(str(sumador) + " < " + str(indiceSorteado) + " -> " + str(contador));
    sumador += listaDePesos[contador];
    contador += 1;
  if(contador != 0):
    indiceSorteado = contador - 1;
  return indiceSorteado;

def verificaCasillaOcupada(fila, columna):
  estadoDeLaFicha = 0;
  for i in range(len(fichas)):
    if (fichas[i][1] == fila and fichas[i][2] == columna):
      estadoDeLaFicha = 1;
      if (fichas[i][0] == True):
        estadoDeLaFicha = 3;
      return [estadoDeLaFicha, i];
  for i in range(len(fichasEnemigas)):
    if (fichasEnemigas[i][1] == fila and fichasEnemigas[i][2] == columna):
      estadoDeLaFicha = 2;
      if (fichasEnemigas[i][0] == True):
        estadoDeLaFicha = 4;
      return [estadoDeLaFicha, i];
       
  ## 0: vacía
  ## 1: dama amiga
  ## 2: dama ENEMIGAS
  ## 3: reina amiga
  ## 4: reina enemiga
  return [estadoDeLaFicha, -1];

def asignaPesosAFichas():
  listaFichasEnemigasADevolver = [];
  for fichaEnemiga in fichasEnemigas:
    #si columna == 0, entonces no podemos movernos más a la izquierda
    #si columna == 7, entonces no podemos movernos más a la derecha
    casillaVerificada1 = 0;
    casillaVerificada2 = 0;
    peso = 0;
    
    if(fichaEnemiga[2] > 0):
      #Verificar casilla abajo a la izquierda
      casillaVerificada1 = verificaCasillaOcupada(fichaEnemiga[1] + 1, fichaEnemiga[2] - 1)[0];
    if(fichaEnemiga[2] < 7):
      #Verificar casilla abajo a la derecha
      casillaVerificada2 = verificaCasillaOcupada(fichaEnemiga[1] + 1, fichaEnemiga[2] + 1)[0];
    
    if(fichaEnemiga[0]):
      #haz cosas de reina
      #verificar si existe riesgo a que te coman
      if(fichaEnemiga[2] > 0):
        if(casillaVerificada1 == 1 or casillaVerificada1 == 3):
          casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] - 1, fichaEnemiga[2] + 1)[0];
          if (casillaVerificada3 == 0 and fichaEnemiga[2] != 7):
            peso += 50000;
          else:
            casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] - 2)[0];
            if(casillaVerificada3 == 0 and fichaEnemiga[2] != 1):
              peso += 50000;
        else:
          if(casillaVerificada1 == 0):
            peso += 1000;
          else:
            casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] - 1, fichaEnemiga[2] - 1)[0];
            if(casillaVerificada3 == 0):
              peso += 1000;
      if(fichaEnemiga[2] < 7):
        if(casillaVerificada2 == 1 or casillaVerificada2 == 3):
          casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] - 1, fichaEnemiga[2] - 1)[0];
          if (casillaVerificada3 == 0 and fichaEnemiga[2] != 0):
            peso += 50000;
          else:
            casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] + 2)[0];
            if(casillaVerificada3 == 0 and fichaEnemiga[2] != 6):
              peso += 50000;
        else:
          if(casillaVerificada2 == 0):
            peso += 1000;
          else:
            casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] - 1, fichaEnemiga[2] + 1)[0];
            if(casillaVerificada3 == 0):
              peso += 1000;
    ####
    #SI NO ES REINA
    ####
    else:
      ###ESTA PARTE ES LA DE LA AI REALMENTE
      if(fichaEnemiga[2] < 7):##Decisión depende solo de casillaVerificada2
        if(casillaVerificada2 == 0):
          peso += 10;
          if(fichaEnemiga[1] > 0):
            peso += 2;
          if(fichaEnemiga[1] > 1):
            peso += 2;
          if(fichaEnemiga[1] > 2):
            peso += 2;
          if(fichaEnemiga[1] > 3):
            peso += 2;
          if(fichaEnemiga[1] > 4):
            peso += 2;
          if(fichaEnemiga[1] > 5):
            peso += 50000;
          casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1], fichaEnemiga[2] + 2)[0];
          casillaVerificada4 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2])[0];
          
          if((casillaVerificada3 == 2 or casillaVerificada3 == 4) and (casillaVerificada4 == 1 or casillaVerificada4 == 3)):
            peso *= 8;
          elif(casillaVerificada3 == 0 and (casillaVerificada4 == 1 or casillaVerificada4 == 3)):
            casillaVerificada5 = verificaCasillaOcupada(fichaEnemiga[1] - 1, fichaEnemiga[2] + 1)[0];
            casillaVerificada6 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] + 2)[0];
            casillaVerificada7 = verificaCasillaOcupada(fichaEnemiga[1] + 1, fichaEnemiga[2] + 3)[0];
            if(casillaVerificada6 == 0 and casillaVerificada7 == 0):
              if (casillaVerificada5 == 2 or casillaVerificada5 == 4):
                  peso *= 6
              elif (casillaVerificada5 == 0):
                peso *= 0.1
        elif((casillaVerificada2 == 1 or casillaVerificada2 == 3) and fichaEnemiga[2] != 6):
          casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] + 2)[0];
          if(casillaVerificada3 == 0):
            peso += 10000;
          if(fichaEnemiga[1] == 6):
            peso *= 0;
      if(fichaEnemiga[2] > 0):##Decisión depende solo de casillaVerificada1
        if(casillaVerificada1 == 0):
          peso += 10;
          if(fichaEnemiga[1] > 0):
            peso += 2;
          if(fichaEnemiga[1] > 1):
            peso += 2;
          if(fichaEnemiga[1] > 2):
            peso += 2;
          if(fichaEnemiga[1] > 3):
            peso += 2;
          if(fichaEnemiga[1] > 4):
            peso += 2;
          if(fichaEnemiga[1] > 5):
            peso += 50000;
          casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1], fichaEnemiga[2] - 2)[0];
          casillaVerificada4 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2])[0];
          
          if((casillaVerificada3 == 2 or casillaVerificada3 == 4) and (casillaVerificada4 == 1 or casillaVerificada4 == 3)):
            peso *= 8;
          elif(casillaVerificada3 == 0 and (casillaVerificada4 == 1 or casillaVerificada4 == 3)):
            casillaVerificada5 = verificaCasillaOcupada(fichaEnemiga[1] - 1, fichaEnemiga[2] - 1)[0];
            casillaVerificada6 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] - 2)[0];
            casillaVerificada7 = verificaCasillaOcupada(fichaEnemiga[1] + 1, fichaEnemiga[2] - 3)[0];
            if(casillaVerificada6 == 0 and casillaVerificada7 == 0):
              if (casillaVerificada5 == 2 or casillaVerificada5 == 4):
                  peso *= 6;
              elif (casillaVerificada5 == 0):
                peso *= 0.1;
        elif((casillaVerificada1 == 1 or casillaVerificada1 == 3) and fichaEnemiga[2] != 1):
          casillaVerificada3 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] - 2)[0];
          if(casillaVerificada3 == 0):
            peso += 10000;
          if(fichaEnemiga[1] == 6):
            peso *= 0;
    ####
    #SI NO ES REINA
    ####
    listaFichasEnemigasADevolver.append([fichaEnemiga[0],fichaEnemiga[1],fichaEnemiga[2],int(peso)]);
  return listaFichasEnemigasADevolver;
  
def determinaMovimientosPosibles(indiceDeFicha):
  listaDeMovimientosPosibles = [];
  #probabilidad
  #tipoDeMovimiento: True si comer, False si es moverse
  #filaCasillaDestino
  #columnaCasillaDestino
  fichaEnemiga = fichasEnemigas[indiceDeFicha];

  if(fichaEnemiga[0]):
    #haz cosas de reina
    caminoLibre = True;
    filaCasillaAnalizada = fichaEnemiga[1];
    columnaCasillaAnalizada = fichaEnemiga[2];
    #dir1: arriba izq
    while(caminoLibre):
      filaCasillaAnalizada-=1;
      columnaCasillaAnalizada-=1;
      if(filaCasillaAnalizada == -1 or columnaCasillaAnalizada == -1):
        caminoLibre = False;
      else:
        casillaAnalizada = verificaCasillaOcupada(filaCasillaAnalizada,columnaCasillaAnalizada)[0];
        if(casillaAnalizada == 0):
          casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada - 1)[0];
          if(casillaAnalizada2 == 1 or casillaAnalizada2 == 3):
            listaDeMovimientosPosibles.append([1,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
          else:
            listaDeMovimientosPosibles.append([10,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
        else:
          caminoLibre = False;
          if((casillaAnalizada == 1 or casillaAnalizada == 3) and filaCasillaAnalizada != 0 and columnaCasillaAnalizada != 0):
            casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada - 1,columnaCasillaAnalizada - 1)[0];
            if (casillaAnalizada2 == 0):
              listaDeMovimientosPosibles.append([100,True,filaCasillaAnalizada-1, columnaCasillaAnalizada-1]);
    
    #dir2: abajo izq
    caminoLibre = True;
    filaCasillaAnalizada = fichaEnemiga[1];
    columnaCasillaAnalizada = fichaEnemiga[2];
    while(caminoLibre):
      filaCasillaAnalizada+=1;
      columnaCasillaAnalizada-=1;
      if(filaCasillaAnalizada == 8 or columnaCasillaAnalizada == -1):
        caminoLibre = False;
      else:
        casillaAnalizada = verificaCasillaOcupada(filaCasillaAnalizada,columnaCasillaAnalizada)[0];
        #print(str(filaCasillaAnalizada) + "-" + str(columnaCasillaAnalizada) + " = " + str(casillaAnalizada));
        if(casillaAnalizada == 0):
          casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada - 1)[0];
          casillaAnalizada3 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada + 1)[0]
          if(casillaAnalizada2 == 1 or casillaAnalizada2 == 3 or casillaAnalizada3 == 1 or casillaAnalizada3 == 3):
            listaDeMovimientosPosibles.append([1,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
          else:
            listaDeMovimientosPosibles.append([10,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
        else:
          caminoLibre = False;
          if((casillaAnalizada == 1 or casillaAnalizada == 3) and filaCasillaAnalizada != 7 and columnaCasillaAnalizada != 0):
            casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada - 1)[0];
            if (casillaAnalizada2 == 0):
              listaDeMovimientosPosibles.append([100,True,filaCasillaAnalizada+1, columnaCasillaAnalizada-1]);
    
    #dir3: arriba der
    caminoLibre = True;
    filaCasillaAnalizada = fichaEnemiga[1];
    columnaCasillaAnalizada = fichaEnemiga[2];
    while(caminoLibre):
      filaCasillaAnalizada-=1;
      columnaCasillaAnalizada+=1;
      if(filaCasillaAnalizada == -1 or columnaCasillaAnalizada == 8):
        caminoLibre = False;
      else:
        casillaAnalizada = verificaCasillaOcupada(filaCasillaAnalizada,columnaCasillaAnalizada)[0];
        if(casillaAnalizada == 0):
          casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada + 1)[0];
          if(casillaAnalizada2 == 1 or casillaAnalizada2 == 3):
            listaDeMovimientosPosibles.append([1,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
          else:
            listaDeMovimientosPosibles.append([10,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
        else:
          caminoLibre = False;
          if((casillaAnalizada == 1 or casillaAnalizada == 3) and filaCasillaAnalizada != 0 and columnaCasillaAnalizada != 7):
            casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada - 1,columnaCasillaAnalizada + 1)[0];
            if (casillaAnalizada2 == 0):
              listaDeMovimientosPosibles.append([100,True,filaCasillaAnalizada - 1, columnaCasillaAnalizada + 1]);
    
    #dir4: abajo der
    caminoLibre = True;
    filaCasillaAnalizada = fichaEnemiga[1];
    columnaCasillaAnalizada = fichaEnemiga[2];
    while(caminoLibre):
      filaCasillaAnalizada+=1;
      columnaCasillaAnalizada+=1;
      if(filaCasillaAnalizada == 8 or columnaCasillaAnalizada == 8):
        caminoLibre = False;
      else:
        casillaAnalizada = verificaCasillaOcupada(filaCasillaAnalizada,columnaCasillaAnalizada)[0];
        if(casillaAnalizada == 0):
          casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada - 1)[0];
          casillaAnalizada3 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada + 1)[0];
          if(casillaAnalizada2 == 1 or casillaAnalizada2 == 3 or casillaAnalizada3 == 1 or casillaAnalizada3 == 3):
            listaDeMovimientosPosibles.append([1,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
          else:
            listaDeMovimientosPosibles.append([10,False,filaCasillaAnalizada, columnaCasillaAnalizada]);
        else:
          caminoLibre = False;
          if((casillaAnalizada == 1 or casillaAnalizada == 3) and filaCasillaAnalizada != 7 and columnaCasillaAnalizada != 7):
            casillaAnalizada2 = verificaCasillaOcupada(filaCasillaAnalizada + 1,columnaCasillaAnalizada + 1)[0];
            if (casillaAnalizada2 == 0):
              listaDeMovimientosPosibles.append([100,True,filaCasillaAnalizada + 1, columnaCasillaAnalizada + 1]);

  else:
    if(fichaEnemiga[2] < 7):
      casillaVerificada = verificaCasillaOcupada(fichaEnemiga[1] + 1, fichaEnemiga[2] + 1)[0];
      if(casillaVerificada == 0):
        listaDeMovimientosPosibles.append([1,False,fichaEnemiga[1] + 1, fichaEnemiga[2] + 1]);
      elif((casillaVerificada == 1 or casillaVerificada == 3) and fichaEnemiga[2] != 6):
        casillaVerificada2 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] + 2)[0];
        if(casillaVerificada2 == 0):
          listaDeMovimientosPosibles.append([99,True,fichaEnemiga[1] + 2, fichaEnemiga[2] + 2]);
    if(fichaEnemiga[2] > 0):
      casillaVerificada = verificaCasillaOcupada(fichaEnemiga[1] + 1, fichaEnemiga[2] - 1)[0];
      if(casillaVerificada == 0):
        listaDeMovimientosPosibles.append([1,False,fichaEnemiga[1] + 1, fichaEnemiga[2] - 1]);
      elif((casillaVerificada == 1 or casillaVerificada == 3) and fichaEnemiga[2] != 1):
        casillaVerificada2 = verificaCasillaOcupada(fichaEnemiga[1] + 2, fichaEnemiga[2] - 2)[0];
        if(casillaVerificada2 == 0):
          listaDeMovimientosPosibles.append([99,True,fichaEnemiga[1] + 2, fichaEnemiga[2] - 2]);
  return listaDeMovimientosPosibles;

"""
1.4 FUNCIONES DE DESPLAZAMIENTO
"""
def eliminarDeFichasJugador(indice):
  listaTemporal = [];
  for i in range(len(fichas)):
    if(i != indice):
      listaTemporal.append(fichas[i]);
  return listaTemporal;

def eliminarDeFichasEnemigas(indice):
  listaTemporal = [];
  for i in range(len(fichasEnemigas)):
    if(i != indice):
      listaTemporal.append(fichasEnemigas[i]);
  return listaTemporal;

"""
1.5 FUNCIONES DE INTERFAZ GRÁFICA
"""

def ubicar(tipo,datos,tablero):
  if(tipo == 0):    
    if(datos[0] == False):
      tablero[datos[1]][datos[2]] = "o";
    else: 
      tablero[datos[1]][datos[2]] = "Q";
    return tablero;
  if(tipo == 1):
    if(datos[0] == False):
      tablero[datos[1]][datos[2]] = "x";
    else:            
      tablero[datos[1]][datos[2]] = "R";        
    return tablero;
  
def pintar(colorUsuario,colorEnemigo,usuario,enemigo):
  lista = [];
  tablero = [];
  for item in range(0,8,1):  
    for item in range(0,8,1):
      lista.append(" ");
    tablero.append(lista);
    lista = [];

  for i in range(1,8,2):
    tablero[0][i] = "/";
    tablero[2][i] = "/";
    tablero[4][i] = "/";
    tablero[6][i] = "/";
  for i in range(0,8,2):
    tablero[1][i] = "/";
    tablero[3][i] = "/";
    tablero[5][i] = "/";
    tablero[7][i] = "/";

  for item in enemigo:
    tablero = ubicar(colorEnemigo,item,tablero);
  for item in usuario:
    tablero = ubicar(colorUsuario,item,tablero);

  pantalla = [];
  for item in range(8): 
    for item2 in range(8):
      pantalla.append(tablero[item][item2]);

  print("    0 " + "  1 " + "  2 " + "  3 " + "  4 " + "  5 " + "  6 " + "  7 ");
  print("   ___" + " ___" + " ___" + " ___" + " ___" + " ___" + " ___" + " ___");

  for item in range(0,64,8):
    print((item//8),"| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} |".format(pantalla[item],pantalla[item+1],pantalla[item+2],pantalla[item+3],pantalla[item+4],pantalla[item+5],pantalla[item+6],pantalla[item+7]));
    print("  " + "|___|" + "___|" + "___|" + "___|" + "___|" + "___|" + "___|" + "___|");

"""
1.6 FUNCIONES DE JUGADOR
"""
#funcionpintar

#Las x representan fichas NEGRAS
#Las o representan fichas blancas
#Las Q representan fichas reinas blancas 
#Las R representan fichas reinas negras


#def moverDamaJugador():
#preguntar al jugador qué ficha quiere mover [validar]
#preguntar adónde quiere moverla [validación]
#a) actualizar posición de la ficha en cuestión
#b) return el índice de la ficha a mover y su nueva posición

#FUNCION PROMEDIO
def promediar(valor1, valor2):
  promedio = (valor1 + valor2)/2;
  return promedio;

#FUNCION ELIMINAR
def eliminarFichaBot(fila,columna, nuevaFila, nuevaColumna):
  opcionDeEliminar = 0;
  estadoDeFichaEliminada = 0;
  filaDeFichaEliminada = 0;
  columnaDeFichaEliminada = 0;
  indice = 0;  

  filaDeFichaEliminada = promediar(fila, nuevaFila);
  columnaDeFichaEliminada = promediar(columna, nuevaColumna);

  estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
  if (estadoDeFichaEliminada == 2 or estadoDeFichaEliminada == 4):
    opcionDeEliminar = 1;
  else:
    opcionDeEliminar = 0;
    
  indice = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[1];
  
  return [opcionDeEliminar, indice];

#FUNCION ELIMINAR CUANDO EL USUARIO ES REINA
def reinaEliminarFichaBot(fila,columna, nuevaFila, nuevaColumna):
  opcionDeEliminar = 0;  # EL 0 ES QUE NO SE ELIMINA, EL 1 SI SE ELIMINA LA FICHA DEL BOT
  estadoDeFichaEliminada = 0;
  filaDeFichaEliminada = 0;
  columnaDeFichaEliminada = 0;
  contador = 0;
  indice = 0;  
  diferencia = abs(fila - nuevaFila);

  if ((nuevaFila < fila) and (nuevaColumna < columna)):  #ARRIBA IZQUIERDA
    for i in range(1,diferencia):
      filaDeFichaEliminada = fila - i;
      columnaDeFichaEliminada = columna - i;
      estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
      if (estadoDeFichaEliminada != 0):
        contador += 1
    if (contador>1):
      opcionDeEliminar = 0;
    elif (contador==0):
      opcionDeEliminar = 1;
    else:
      estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
      if ((filaDeFichaEliminada == nuevaFila + 1) and (columnaDeFichaEliminada == nuevaColumna + 1) and (estadoDeFichaEliminada == 2 or estadoDeFichaEliminada == 4)):
        opcionDeEliminar = 1;
        indice = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[1];
      else:
          opcionDeEliminar = 0;  

  elif ((nuevaFila < fila) and (nuevaColumna > columna)): # ARRIBA DERECHA
    for i in range(1,diferencia):
      filaDeFichaEliminada = fila - i;
      columnaDeFichaEliminada = columna + i;
      estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
      if (estadoDeFichaEliminada != 0):
        contador += 1;
      
    if(contador>1):
      opcionDeEliminar = 0;
    elif (contador==0):
      opcionDeEliminar = 1;
    else:
      estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
      if ((filaDeFichaEliminada == nuevaFila + 1) and (columnaDeFichaEliminada == nuevaColumna - 1) and (estadoDeFichaEliminada == 2 or estadoDeFichaEliminada == 4)):
        opcionDeEliminar = 1;
        indice = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[1];
      else:
          opcionDeEliminar = 0;

  elif ((nuevaFila > fila) and (nuevaColumna < columna)): #ABAJO IZQUIERDA
      for i in range(1,diferencia):
        filaDeFichaEliminada = fila + i;
        columnaDeFichaEliminada = columna - i;
        estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
        if (estadoDeFichaEliminada != 0):
          contador += 1
      if(contador>1):
        opcionDeEliminar = 0;
      elif (contador==0):
        opcionDeEliminar = 1;
      else:
        estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
        if ((filaDeFichaEliminada == nuevaFila - 1) and (columnaDeFichaEliminada == nuevaColumna + 1) and (estadoDeFichaEliminada == 2 or estadoDeFichaEliminada == 4)):
          opcionDeEliminar = 1;
          indice = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[1];
        else:
          opcionDeEliminar = 0;

  elif ((nuevaFila > fila) and (nuevaColumna > columna)):     #ABAJO DERECHA
      for i in range(1,diferencia):
        filaDeFichaEliminada = fila + i;
        columnaDeFichaEliminada = columna + i;
        estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
        if (estadoDeFichaEliminada != 0):
          contador += 1
      if(contador>1):
        opcionDeEliminar = 0;
      elif (contador==0):
        opcionDeEliminar = 1;
      else:
        estadoDeFichaEliminada = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[0];
        if ((filaDeFichaEliminada == nuevaFila - 1) and (columnaDeFichaEliminada == nuevaColumna - 1) and (estadoDeFichaEliminada == 2 or estadoDeFichaEliminada == 4)):
          opcionDeEliminar = 1;
          indice = verificaCasillaOcupada(filaDeFichaEliminada, columnaDeFichaEliminada)[1];
        else:
          opcionDeEliminar = 0;
  return [opcionDeEliminar, indice];

#FUNCIÓN DE MOVER DAMA
def moverDamaJugador():
  estadoDeFicha = 0;
  nuevaCasillaOcupada = 1;
  opcionDeMover = 0;
  indiceDeFichaEliminada = 0;
  listaActualizada = [];
  
  while (nuevaCasillaOcupada != 0):
    
    while((estadoDeFicha == 0) or (estadoDeFicha == 2) or (estadoDeFicha == 4)): # or estadoDeFicha == 3
      fila = validarEntero("\nIngrese fila de la ficha a mover: ", 0, 7, 1, 1);
      columna = validarEntero("Ingrese columna de la ficha a mover: ", 0, 7, 1, 1);
      estadoDeFicha = verificaCasillaOcupada(fila, columna)[0];    
      if (estadoDeFicha == 3):
        return moverReinaJugador(fila,columna);
  
    while (opcionDeMover == 0): 
      nuevaFila = validarEntero("\nIngrese fila de la casilla a la que quiere mover: ", fila - 2, fila - 1, 1, 1);
      
      nuevaColumna = columna;
      while (nuevaColumna == columna or nuevaColumna == -1 or nuevaColumna == 8):
        nuevaColumna = validarEntero("Ingrese columna de la casilla a la que quiere mover: ", columna - 2, columna + 2, 1, 1);
      
      nuevaCasillaOcupada = verificaCasillaOcupada(nuevaFila,nuevaColumna)[0]; 
      
      if(nuevaFila == fila - 2 and nuevaColumna == columna - 2) or (nuevaFila == fila - 2 and nuevaColumna == columna + 2):
        if (eliminarFichaBot(fila, columna, nuevaFila, nuevaColumna)[0] == 1):   
          indiceDeFichaEliminada = eliminarFichaBot(fila, columna, nuevaFila, nuevaColumna)[1]; 
          listaActualizada = eliminarDeFichasEnemigas(indiceDeFichaEliminada); 
          opcionDeMover = 1; #SI SE PUEDE MOVER
        else:
          opcionDeMover = 0; #NO SE PUEDE MOVER

      elif (nuevaFila == fila - 1 and nuevaColumna == columna - 1) or (nuevaFila == fila - 1 and nuevaColumna == columna + 1):
        if (nuevaCasillaOcupada != 0):
          opcionDeMover = 0; #NO SE PUEDE MOVER
        else:
          opcionDeMover = 1; #SI SE PUEDE MOVER
          listaActualizada = fichasEnemigas;

      else:
        opcionDeMover = 0; #NO SE PUEDE MOVER

  return [verificaCasillaOcupada(fila, columna)[1], nuevaFila, nuevaColumna, listaActualizada, fila, columna];

#FUNCIÓN DE MOVER REINA
# 0: vacía
# 1: dama amiga
# 2: dama ENEMIGAS
# 3: reina amiga
# 4: reina enemiga

def moverReinaJugador(fila, columna):
  estadoDeFicha = 0;
  nuevaCasillaOcupada = 1;
  diferencia = 0;
  opcionDeMover = 0;
  indiceDeFichaEliminada = 0;
  listaActualizada = [];
  
  while(estadoDeFicha != 3): 
    estadoDeFicha = verificaCasillaOcupada(fila, columna)[0];    
    
  while (opcionDeMover == 0):  
    nuevaFila = validarEntero("\nIngrese fila de la casilla a la que quiere mover: ", 0, 7, 1, 1);
      
    while (nuevaFila == fila):
      nuevaFila = validarEntero("\nIngrese fila de la casilla a la que quiere mover: ", 0, 7, 1, 1);

    diferencia = abs(fila - nuevaFila);
      
    nuevaColumna = columna;
    while (nuevaColumna == columna or nuevaColumna == -1 or nuevaColumna == 8 ):
      nuevaColumna = validarEntero("Ingrese columna de la casilla a la que quiere mover: ", 0, 7, 1, 1);
      if (nuevaColumna == columna + diferencia or nuevaColumna == columna - diferencia):
        break;
      else:
        nuevaColumna = -1;

    nuevaCasillaOcupada = verificaCasillaOcupada(nuevaFila,nuevaColumna)[0];
    if nuevaCasillaOcupada != 0:
      opcionDeMover = 0;
    elif reinaEliminarFichaBot(fila,columna, nuevaFila, nuevaColumna)[0] == 1:
      opcionDeMover = 1;  
      indiceDeFichaEliminada = reinaEliminarFichaBot(fila, columna, nuevaFila, nuevaColumna)[1]; 
      listaActualizada = eliminarDeFichasEnemigas(indiceDeFichaEliminada); 
    else:
      opcionDeMover = 0;
      listaActualizada = fichasEnemigas;
    
  return [verificaCasillaOcupada(fila, columna)[1], nuevaFila, nuevaColumna, listaActualizada];
"""
2. OBJETOS Y VARIABLES GLOBALES
"""
colorBlanco = 0;
colorNegro = 1;
colorDeFichaUsuario = 0;
colorDeFichaBot = 1;
nadiePerdio = True;
NombreDeUsuario = "";

#listas de fichas
fichas = [];
fichasEnemigas = [];

"""
3. PROGRAMA
"""

"""
3.1 INICIALIZACIÓN DEL JUEGO
"""
inicializarFichas();
nadiePerdio = True;
jugadorPerdio = False;
empate = False;
listaInicializacion = inicializacionDelResto();
colorDeFichaUsuario = listaInicializacion[0];#"o";
colorDeFichaBot = listaInicializacion[1];# = 1;
NombreDeUsuario = listaInicializacion[2];

if(listaInicializacion[0] == 0):
  print("\nNO SUBESTIMES EL PODER DEL LADO OSCURO...");
else:
  print("\nBUENO, YA SABES LO QUE DICEN: PRIMERO LAS DAMAS... ESPERA O_o");

"""
3.2 BUCLE DEL JUEGO
"""
while(nadiePerdio):
  pintar(colorDeFichaUsuario,colorDeFichaBot,fichas,fichasEnemigas);

  if(colorDeFichaUsuario == 0):
    resultadoDeMoverJugador = moverDamaJugador();
  
    if (resultadoDeMoverJugador[1] == 0):
      fichaCoronada = coronarJugador(resultadoDeMoverJugador[0],resultadoDeMoverJugador[1],resultadoDeMoverJugador[2]);
      fichas = modificarFichas(fichaCoronada);
      print("\nBUEN MOVIMIENTO.... SI ASÍ FUERAS EN ANALÍTICA ;)");
    else:
      fichas = modificarFichas(resultadoDeMoverJugador);
      fichasEnemigas = resultadoDeMoverJugador[3];
      sorteo = randint(0,3);
      if(sorteo == 0):
        print("\nTENDRÉ QUE DEJAR DE PLANCHAR, ESTO VA EN SERIO.");
      elif(sorteo == 1):
        print("\nTRANQUILO, ESTO RECIÉN EMPIEZA.");
      else:
        print("\nNO PIENSES QUE TE LA LLEVARÁS FÁCIL.");
  else:
    if(len(fichasEnemigas) == 0):
      nadiePerdio = False;
      break;

    fichasEnemigas = asignaPesosAFichas();
    listaDePesos = [];

    sumaDePesos = 0;
    for ficha in fichasEnemigas:
      #print(ficha);
      listaDePesos.append(ficha[3]);
      sumaDePesos += ficha[3];

    if(sumaDePesos == 0):
      nadiePerdio = False;
      empate = True;
    else:
      fichaMovida = sorteaConPesos(listaDePesos);
      movPosibles = determinaMovimientosPosibles(fichaMovida);
      listaDePesos = [];
      for mP in movPosibles:
        listaDePesos.append(mP[0]);
      movElegido = sorteaConPesos(listaDePesos);
      #print(movElegido);
      #print(str(fichaMovida)+ " - " + str(movPosibles[movElegido]));

      #AQUI ELIMINAR JUGADORES
      if(movPosibles[movElegido][1]):
        #if(fichasEnemigas[fichaMovida][0]):
        #  print("ah, la reina está comiendo");
        if(fichasEnemigas[fichaMovida][1] < movPosibles[movElegido][2]):#si estamos bajando
          filaCasillaJugador = movPosibles[movElegido][2]-1;
        else:#si estamos subiendo
          filaCasillaJugador = movPosibles[movElegido][2]+1;
        if(fichasEnemigas[fichaMovida][2] < movPosibles[movElegido][3]):#si vamos a derecha
          columnaCasillaJugador = movPosibles[movElegido][3]-1;
        else:#si vamos a la izquierda
          columnaCasillaJugador = movPosibles[movElegido][3]+1;
      #  else:
          #filaCasillaJugador = (fichasEnemigas[fichaMovida][1] +movPosibles[movElegido][2])/2;
          #columnaCasillaJugador = (fichasEnemigas[fichaMovida][2]+movPosibles[movElegido][3])/2;
        verifCasilla = verificaCasillaOcupada(filaCasillaJugador, columnaCasillaJugador);
        fichas = eliminarDeFichasJugador(verifCasilla[1]);
        sorteo = randint(0,3);
        if(sorteo == 0):
          print("\nPODEMOS JUGAR EN UN TABLERO DE 3X3... ¿O QUIERES VER EL TUTORIAL?");
        elif(sorteo == 1):
          print("\nGRACIAS POR EL REGALO :D, PERO AUN NO ES NAVIDAD.");
        elif(sorteo == 2):
          print("\nCREO QUE MEJOR VOLVEMOS A EMPEZAR...");
        else:
          print("\n¡JA JA JA!");

      #parametros[0] = índiceAModificar
      #parametros[1] = nuevaFila
      #parametros[2] = nuevaColumna
      fichasEnemigas = modificarFichasEnemigas([fichaMovida, movPosibles[movElegido][2], movPosibles[movElegido][3]]);
      if (movPosibles[movElegido][2] == 7):
        fichasEnemigas = coronarEnemigas(len(fichasEnemigas)-1);
        print("\nYA ESTÁ PS. ¡EN DOS PASOS TE GANO, COMO DIRÍA EL MAESTRO ACOSTA!");

      if(len(fichas) == 0):
        nadiePerdio = False;
        jugadorPerdio = True;
        break;
        
  pintar(colorDeFichaUsuario,colorDeFichaBot,fichas,fichasEnemigas);
  
  if(colorDeFichaUsuario == 0):
    if(len(fichasEnemigas) == 0):
      nadiePerdio = False;
      break;

    fichasEnemigas = asignaPesosAFichas();
    listaDePesos = [];

    sumaDePesos = 0;
    for ficha in fichasEnemigas:
      #print(ficha);
      listaDePesos.append(ficha[3]);
      sumaDePesos += ficha[3];

    if(sumaDePesos == 0):
      nadiePerdio = False;
      empate = True;
    else:
      fichaMovida = sorteaConPesos(listaDePesos);
      movPosibles = determinaMovimientosPosibles(fichaMovida);
      listaDePesos = [];
      for mP in movPosibles:
        listaDePesos.append(mP[0]);
      movElegido = sorteaConPesos(listaDePesos);
      #print(movElegido);
      #print(str(fichaMovida)+ " - " + str(movPosibles[movElegido]));

      #AQUI ELIMINAR JUGADORES
      if(movPosibles[movElegido][1]):
        #if(fichasEnemigas[fichaMovida][0]):
        #  print("ah, la reina está comiendo");
        if(fichasEnemigas[fichaMovida][1] < movPosibles[movElegido][2]):#si estamos bajando
          filaCasillaJugador = movPosibles[movElegido][2]-1;
        else:#si estamos subiendo
          filaCasillaJugador = movPosibles[movElegido][2]+1;
        if(fichasEnemigas[fichaMovida][2] < movPosibles[movElegido][3]):#si vamos a derecha
          columnaCasillaJugador = movPosibles[movElegido][3]-1;
        else:#si vamos a la izquierda
          columnaCasillaJugador = movPosibles[movElegido][3]+1;
      #  else:
          #filaCasillaJugador = (fichasEnemigas[fichaMovida][1] +movPosibles[movElegido][2])/2;
          #columnaCasillaJugador = (fichasEnemigas[fichaMovida][2]+movPosibles[movElegido][3])/2;
        verifCasilla = verificaCasillaOcupada(filaCasillaJugador, columnaCasillaJugador);
        fichas = eliminarDeFichasJugador(verifCasilla[1]);
        sorteo = randint(0,3);
        if(sorteo == 0):
          print("\nPODEMOS JUGAR EN UN TABLERO DE 3X3... ¿O QUIERES VER EL TUTORIAL?");
        elif(sorteo == 1):
          print("\nGRACIAS POR EL REGALO :D, PERO AUN NO ES NAVIDAD.");
        elif(sorteo == 2):
          print("\nCREO QUE MEJOR VOLVEMOS A EMPEZAR...");
        else:
          print("\n¡JA JA JA!");
      #parametros[0] = índiceAModificar
      #parametros[1] = nuevaFila
      #parametros[2] = nuevaColumna
      fichasEnemigas = modificarFichasEnemigas([fichaMovida, movPosibles[movElegido][2], movPosibles[movElegido][3]]);
      if (movPosibles[movElegido][2] == 7):
        fichasEnemigas = coronarEnemigas(len(fichasEnemigas)-1);
        print("\nYA ESTÁ PS. ¡EN DOS PASOS TE GANO, COMO DIRÍA EL MAESTRO ACOSTA!");
      if(len(fichas) == 0):
        nadiePerdio = False;
        jugadorPerdio = True;
        break;
  else:
    resultadoDeMoverJugador = moverDamaJugador();
    if (resultadoDeMoverJugador[1] == 0):
      fichaCoronada = coronarJugador(resultadoDeMoverJugador[0],resultadoDeMoverJugador[1],resultadoDeMoverJugador[2]);
      fichas = modificarFichas(fichaCoronada);
      print("\nBUEN MOVIMIENTO... SI ASÍ FUERAS EN ANALÍTICA ;)");
    else:
      fichas = modificarFichas(resultadoDeMoverJugador);
      fichasEnemigas = resultadoDeMoverJugador[3];
      sorteo = randint(0,3);
      if(sorteo == 0):
        print("\nTENDRÉ QUE DEJAR DE PLANCHAR, ESTO VA EN SERIO.");
      elif(sorteo == 1):
        print("\nTRANQUILO, ESTO RECIÉN EMPIEZA.");
      else:
        print("\nNO PIENSES QUE TE LA LLEVARÁS FÁCIL.");
  #print(sorteaConPesos([3,4,2,5,0,9]));
print("\nFin de partida:");
if(empate):
  print("\n¿AHOGADO? ¡TODOS SABEMOS QUE SOY MEJOR QUE TÚ! >:v");
elif(jugadorPerdio): 
  print("\n¡AHÍ ESTÁAAAA PE SU ÍDOLO!, MUY FÁCIL :D");
else:
  print("\n¿AAAAAALA QUE ASÍ VA A SER? :'( ");