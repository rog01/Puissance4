import numpy as np
import pygame
import time

#Imports, initialisation
import os 


class Connect4():
    
    def init(self, joueur1=1,joueur2=-1,ligne=6,colonne=7 ):
        #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = '/home/roger/anaconda3/projetIA/puissance4/IA_puissance4/IA_puissance4/'
        path = ROOT_DIR
        pygame.init ()
        self.image = pygame.image.load (path+"Grille.png")
        size = self.image.get_size ()
        self.screen = pygame.display.set_mode (size)
        self.screen.blit (self.image, (0,0))
        pygame.display.flip ()

        self.pionjaune = pygame.image.load (path+"PionJaune.png")
        self.pionrouge = pygame.image.load (path+"PionRouge.png")

        self.JetonsJoues = 0
        self.gagnant = 0

        self.ligne = ligne
        self.colonne = colonne
        self.matrice = np.matrix(np.zeros((ligne,colonne)))
        self.joueur1 =joueur1 
        self.joueur2 =joueur2
        self.terminal = False
        return self.terminal

    def play(self, terminal, strategy="random"):
       
        # -> modifier l'état courant (état du plateau) en fonction de l'action `a`
        # -> gagné/terminé ? 
        # -> si non -> faire jouer l'adversaire (avec strategy)
        # -> perdu/terminé ?        
        
        # next_state: état du plateau de jeu après l'application de l'action `a` 
        #             ET de la réponse de l'adversaire (random par exemple)
        #
        # reward (int):
        #    1: gagné
        #    -1: perdu
        #    0: autre cas
        #
        # terminal (Bool): jeux terminé (True) ou en-cours (False) 

        #start(matrice)
        while (terminal == False and self.JetonsJoues < 42):
            # Le joueur joue
            for event in pygame.event.get():
                #Le joueur joue
                if event.type == pygame.MOUSEBUTTONUP :
                    x,y = pygame.mouse.get_pos()
                    #print('x',x)
                    #print('y',y)
                    #print('====================================')
                    joueur = self.joueur1
                    colonne = choisir_colonne(x,y)
                    matrice = add_nouveau_jeton(self, joueur, colonne)
                    next_state = matrice
                    gagnant = verif_gagnant(self)
                    reward = gagnant
                    if reward == 1 or reward == -1:
                        terminal = True
                    #print(matrice)
                    self.JetonsJoues += 1
                    affichage(self,matrice)
                    pygame.display.flip()

                    #réponse random
                    joueur = self.joueur2
                    #print('etape 2')
                    #colonne = np.random.randint(0,7) # debut du random joueur 2
                    #print('colonne du j2',colonne)
                    #matrice = add_nouveau_jeton(joueur2,colonne)
                    if strategy == "random":
                        colonne = strategy_random(self,matrice)
                    else:
                        colonne = attaque_defense(self,matrice)

                    matrice[ligne_vide(self,colonne),colonne] = joueur
                    next_state = matrice
                    gagnant = verif_gagnant(self) 
                    reward = gagnant
                    if reward == 1 or reward == -1:
                        terminal = True    
                    #print(matrice)      
                    self.JetonsJoues += 1

                    affichage(self,matrice)

                    pygame.display.flip()
                    time.sleep (0.5)
                if event.type == pygame.QUIT:
                    sys.exit()

        if gagnant != 0:
            print('Joueur',gagnant,'a gagné !')
        elif JetonsJoues == 42:
            print('Plus de jeton disponible, égalité')
        else:
            print('Jeu interrompu')

        return next_state, reward, terminal
    
    # Affichage
def affichage(self,matrice):
    self.screen.fill((0,0,0))
    self.screen.blit(self.image,(0,0))
    for i in range(self.ligne):
        for j in range(self.colonne):
            if matrice[i,j]==1:
                #print('i,j',i,j)
                self.screen.blit(self.pionrouge,(16+97*j,16+97*i))
                pygame.display.flip()
            if matrice[i,j]==-1:
                #print('i,j',i,j)
                self.screen.blit(self.pionjaune,(16+97*j,16+97*i))
                pygame.display.flip()


# ajout d'un 1 ou  -1 init()dans la 1ere ligne vide &ere colonne partant du bas
def add_jeton_premiere_colonne_gauche(joueur1):
    for i in range(ligne):
        if 0 in matrice[ligne-1-i]:
            _, ind = np.where(matrice[ligne-1-i] == 0)
            col_vide = ind[0] # la 1ere colonne vide
            break
    if col_vide is not None:
        matrice[ligne-1-i,col_vide]=joueur1 # On ajoute un 1 ou -1 dans la 1ere colonne vide
    return matrice

# ajout d'un 1 ou  -1 dans la 1ere ligne vide & 1ere colonne partant du bas
def add_nouveau_jeton(self,joueur1, colonne):
    for i in range(self.ligne):
        if self.matrice[self.ligne-1-i,colonne] == 0:
            self.matrice[self.ligne-1-i,colonne]=joueur1
            #print('add_nouveau_jeton',i)
            break
    return self.matrice

def start_game(joueur1):
    if matrice[ligne-1,col//2]==0:
        matrice[ligne-1,col//2]=joueur1
    else :
        matrice[ligne-1,col//2+1]=joueur1   
    return matrice

# on rajoute un 1 ou -1 au dessus de la colonne contenant deja un 1 ou -1
def next_step(joueur1):
    for i in range(ligne):
        if joueur1 == 1:
            if np.max(matrice[i])==joueur1:
                colonne = np.argmax(matrice[i])
                break
        elif joueur1 == -1:
            if np.min(matrice[i])==joueur1:
                colonne = np.argmin(matrice[i])   
                break 
    if i != 0:
        if matrice[i-1,colonne]==0:
            matrice[i-1,colonne]=joueur1 # on rajoute un 1 ou -1 au dessus de la colonne contenant deja un 1 ou -1
    return matrice

def verif_col(self,matrice):
    matrice_verif = np.matrix(np.zeros((4,1))) # vecteur de 4 zeros
    # verification de la ligne k
    for k in range(self.ligne-3): # decalage sur 2 lignes de la matrice 4*4 a verifier
        for j in range(self.colonne-3): # decalage sur 3 colonnes de la matrice 4*4 a verifier
            for i in range(self.colonne-3):
                # verification de la colonne i dans la matrice 4*4 a verifier
                matrice_verif[i,0] = 1
                res = matrice[0+k:4+k,0+j:4+j]*matrice_verif
                res = [1,1,1,1]*res
                if res[0,0] == 4:
                    print('Le joueur',1,'a gagné sur une colonne')
                    self.gagnant = self.joueur1
                elif res[0,0] == -4:
                    print('Le joueur',2,'a gagné sur une colonne')
                    self.gagnant = self.joueur2
                    break
                matrice_verif = np.matrix(np.zeros((4,1)))  
            if res[0,0] == 4 or res[0,0] == -4:
                break
        if res[0,0] == 4 or res[0,0] == -4:
            break
    return self.gagnant

def verif_ligne(self,matrice):
    matrice_verif = np.matrix(np.zeros((1,4))) # matrice 1*4 de 4 zeros
    # verification de la ligne k
    for k in range(self.ligne-3): # decalage sur 2 lignes de la matrice 4*4 a verifier
        for j in range(self.colonne-3): # decalage sur 3 colonnes de la matrice 4*4 a verifier
            for i in range(self.colonne-3):
                # verification de la colonne i dans la matrice 4*4 a verifier
                matrice_verif[0,i] = 1
                res = matrice_verif * matrice[0+k:4+k,0+j:4+j]
                res = res * np.matrix(np.ones((4,1)))
                if res[0,0] == 4:
                    print('Le joueur',1,'a gagné sur une ligne')
                    self.gagnant = self.joueur1
                    break
                elif res[0,0] == -4:
                    print('Le joueur',2,'a gagné sur une ligne')
                    self.gagnant = self.joueur2
                    break
                matrice_verif = np.matrix(np.zeros((1,4)))   
            if res[0,0] == 4 or res[0,0] == -4:
                break
        if res[0,0] == 4 or res[0,0] == -4:
            break
    return self.gagnant

def verif_diagonal_principale(self,matrice):
    for k in range(self.ligne-2): # decalage sur 2 lignes de la matrice 4*4 a verifier
        for j in range(self.colonne-3): # decalage sur 3 colonnes de la matrice 4*4 a verifier
            # verification de la colonne i dans la matrice 4*4 a verifier
            res = np.trace(matrice[0+k:4+k,0+j:4+j])
            if res == 4:
                print('Le joueur',1,'a gagné sur une diagonale principale' )
                self.gagnant = self.joueur1
                break
            elif res == -4:
                print('Le joueur',2,'a gagné sur une diagonale principale')
                self.gagnant = self.joueur2
                break
        if res == 4 or res == -4:
            break
    return self.gagnant

def verif_diagonal_sec(self,matrice):
    for k in range(self.ligne-3): # decalage sur 2 lignes de la matrice 4*4 a verifier
        for j in range(self.colonne-3): # decalage sur 3 colonnes de la matrice 4*4 a verifier
            # verification de la colonne i dans la matrice 4*4 a verifier
            mat = np.matrix(np.zeros((4,4)))
            mat[:,0] = matrice[0+k:4+k,3+j]
            mat[:,3] = matrice[0+k:4+k,0+j]
            mat[:,1] = matrice[0+k:4+k,2+j]
            mat[:,2] = matrice[0+k:4+k,1+j]
            #print('matrice inversee',mat)
            res = np.trace(mat)
            #print('res',res)
            if res == 4:
                print('Le joueur',1,'a gagné sur une diagonale secondaire')
                self.gagnant = self.joueur1
                break
            elif res == -4:
                print('Le joueur',2,'a gagné sur une diagonale secondaire')
                self.gagnant = self.joueur2
                break
        if res == 4 or res == -4:
            break
    return self.gagnant

# verification du gagnant
def verif_gagnant(self):
    gagnant = verif_col(self,self.matrice)
    if gagnant == 0:
        gagnant = verif_ligne(self,self.matrice)
        if gagnant == 0:
            gagnant = verif_diagonal_principale(self,self.matrice)
            if gagnant == 0:
                gagnant = verif_diagonal_sec(self,self.matrice)
    return gagnant

# Organisaton du jeu
# 2 joueurs, choix des colonnes au hasard

def start(matrice):
    global gagnant
    gagnant = 0
    matrice = start_game(joueur1)
    print('le joueur 1 joue au centre')# le joueur 1 joue au centre
    print(matrice)
    matrice = start_game(joueur2)
    print('le joueur 2 joue juste à droite') # le joueur 2 joue juste à droite
    print(matrice)
    matrice = next_step(joueur1) # le joueur 1 joue au au dessus du 1er jeton
    print('le joueur 1 joue au au dessus du 1er jeton')
    print(matrice)
    matrice = next_step(joueur2) # le joueur 2 joue au au dessus du 1er jeton
    print('le joueur 2 joue au au dessus du 1er jeton')
    print(matrice)
    for i in range(22):
        if gagnant == 0:
            #colonne = np.random.randint(0,7) # debut du random joueur 1
            #print('joueur 1 joue en colonne : ',colonne)
            colonne = input("Quelle colonne ?   ")
            matrice = add_nouveau_jeton(joueur1,int(colonne))
            print(matrice)        
            gagnant = verif_gagnant()
        else :
            break
        if gagnant == 0:
            colonne = np.random.randint(0,7) # debut du random joueur 2
            print('joueur 2 joue en colonne : ',colonne)
            matrice = add_nouveau_jeton(joueur2,colonne)
            print(matrice)
            verif_gagnant()
        else:
            break  

def choisir_colonne(x,y):
    '''Cette fonction retourne la colonne demandee par le joueur 1 suivant où il a cliqué'''
    colonne=x-16
    colonne=int(colonne/97)  
    #print('colonne du j1',colonne)
    return colonne

# verifie si la ligne est vide et renvoi la ligne
def ligne_vide(self,colonne):
    ligne_vide = 0
    for i in range(self.ligne):
        if self.matrice[self.ligne-1-i,colonne] == 0:
            ligne_vide  = self.ligne-1-i
            break
        else:
            ligne_vide = -1
    return ligne_vide

def colonne_disponible(self,matrice,col):
    '''retourne vrai ou faux suivant si la colonne est disponible'''
    vide = False
    for i in range(self.ligne):
        if matrice[self.ligne-1-i,col] == 0:
            vide = True
            break
    return vide

def strategy_random(self,matrice):
    col = np.random.randint(0,7)
    if colonne_disponible(self,matrice,col) == True:
        col_rand = col
    return col_rand

def attaque_defense(self,matrice):
    '''vérifie si on peut gagner quelque part et y joue, sinon on essaie de bloquer l'adversaire'''
    col = -1
    for j in range(7):
        # l IA joue en mettant -1 pour gagner
        #if verif_colonne(j) == j: #si on peut jouer sur cette colonne
        if colonne_disponible(self,matrice,j) == True: #si on peut jouer sur cette colonne
            matrice[ligne_vide(self,j),j] = -1
            print('m',matrice)
            if verif_gagnant(self) == -1:
                col = j
                matrice[ligne_vide(self,j)+1,j] = 0 # On remets à zéro la ligne que l'on vient de modifier
                self.gagnant = 0 # On remest gagant à zero
                break
            matrice[ligne_vide(self,j)+1,j] = 0 # On incremente l indice de ligne pour effacer ce que l on vient d ecrire car 
            self.gagnant = 0                    # car en rajoutant un element , la derniere ligne vide est décalée au dessus
            print('ligne_vide(j)',ligne_vide(self,j))
            print('matrice[ligne_vide(j),j]',matrice[ligne_vide(self,j),j])
    # l IA bloque en mettant -1  la ou l adversiare peur gagne avec un 1
    # on n 'a pas trouvé de coup gagnant si col = -1 
    if col == -1:
        for j in range(7):
            if colonne_disponible(self,matrice,j) == True: #si on peut jouer sur cette colonne
                matrice[ligne_vide(self,j),j] = 1
                print('======================================')
                print('M',matrice)
                # ajout d un break pour sortir quand on a trouve une menace
                if verif_gagnant(self) == 1:
                    col = j
                    print('colonne',col)
                    matrice[ligne_vide(self,j)+1,j] = 0
                    self.gagnant = 0
                    break  
                matrice[ligne_vide(self,j)+1,j] = 0
                self.gagnant = 0                                 
        if col == -1:
            if colonne_disponible(self,matrice,j) == True:
                col = j                
    return col 

game = Connect4()
term = game.init()
next_state, reward, terminal = game.play(term, strategy="attaque_defense")
#next_state, reward, terminal = game.play(term, strategy="random")
print(next_state)
print('reward',reward)
print('terminal',terminal)