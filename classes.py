import pygame
from pygame.locals import *
from constantes import *
from random import randint, choice

class perso:
    def __init__(self, pos_x = 0, pos_y = 0):
        self.dim_ecran = (900,500)
        #On charge les images du dino, du ptero et game over
        self.arret = pygame.image.load(image_dino_arret).convert_alpha()
        self.marche1 = pygame.image.load(image_dino_marche1).convert_alpha() #etat 1
        self.marche2 = pygame.image.load(image_dino_marche2).convert_alpha() #etat 2
        self.accroupi1 = pygame.image.load(image_dino_accroupi1).convert_alpha() #etat 1
        self.accroupi2 = pygame.image.load(image_dino_accroupi2).convert_alpha() #etat 2
        self.dead = pygame.image.load(image_dino_dead).convert_alpha()

        self.ptero1 = pygame.image.load(image_ptero1).convert_alpha() #etat 1
        self.ptero2 = pygame.image.load(image_ptero2).convert_alpha() #etat 2

        self.gameover = pygame.image.load(image_gameover).convert_alpha()
        self.reboot = pygame.image.load(image_reboot).convert_alpha()

        s_defaut = pygame.Surface((10, 10)) #surface par défaut, la taille sera changée plus tard par la fonction "put_image_dimension_to_rect"
        s_defaut.set_alpha(0) #cette surface par défaut est transparente pour etre sur qu'elle ne soit pas vue

        self.x = round(pos_x) #On est obligé d'arrondir pour que il n'y ait pas d'incertitude
        self.y = round(pos_y) # sur le pixel que va prendre rect pour faire les dimensions
        self.pos_jump = self.arret.get_rect(topleft = (self.x, self.y)) #Image modèle pour faire le rect par défaut
        self.pos_accroupi = self.accroupi1.get_rect(topleft = (self.x - 15, self.y + 17)) #Image modèle pour faire le rect pour le dino accroupi
        self.obs_defaut = s_defaut
        self.pos_obs_defaut = s_defaut.get_rect(left = self.dim_ecran[0]+2) #Image modèle pour faire le rect pour l'obstacle par défaut (inutile mais nécéssaire pour la première boucle)
        self.etat_d = 1 #etat du Dino
        self.etat_p = 1 #etat du ptero
        self.etat_p_old = self.etat_p
        self.accroupi = False
        self.ti=0
        self.sens_jump = 1
        self.vy = 0
        self.vy_initial = vitesse_y_init
        self.sol= self.y
        self.vitesse_nuage = vitesse_nuage
        self.vitesse_sol = vitesse_sol
        self.vitesse_pte_max = vitesse_pte_max
        self.vitesse_pte_min = vitesse_pte_min
        self.temps_start_jeu = pygame.time.get_ticks()
        self.score = 0
        self.HIscore = 0
        self.colli = False
        self.affiche_score3_old = "0"

    def run(self):
        if self.ti != 0:
            return self.arret
        if self.accroupi == True:
            if self.etat_d == 1:
                self.etat_d = 2
                self.pos_jump.y = self.dim_ecran[1]*0.999-59 #On définie les coordonnées d'affichage du dino
                return self.accroupi1
            elif self.etat_d == 2:
                self.etat_d = 1
                self.pos_jump.y = self.dim_ecran[1]*0.999-59 #On définie les coordonnées d'affichage du dino
                return self.accroupi2
        else:
            if self.etat_d == 1:
                self.etat_d = 2
                self.pos_jump.y = self.y #On définie les coordonnées d'affichage du dino
                return self.marche1
            elif self.etat_d == 2:
                self.etat_d = 1
                self.pos_jump.y = self.y #On définie les coordonnées d'affichage du dino
                return self.marche2

    def ptero(self):
        self.etat_p_old = self.etat_p
        if self.etat_p == 1:
            self.etat_p = 2
            return self.ptero1
        elif self.etat_p == 2:
            self.etat_p = 1
            return self.ptero2

    def jump_init(self): #Sert à initialiser le saut (est éxécutée qu'une fois au moment du relachement de la touche espace/flèche haut)
        self.ti=pygame.time.get_ticks()
        self.sens_jump = 1

    def jump(self, a, jauge): #Est éxécutée en boucle mais ne s'active réellement que quand le saut a été initialisé
        if self.ti!=0:
            if self.sens_jump == 0:
                acc = a*2
            elif self.sens_jump == 1:
                acc = a
                if self.vy_initial != 0: #Si vy_initial n'a pas été mis à 0 (par la touche flèche bas) alors on continue de faire monter le dino
                    self.vy_initial = vitesse_y_init*1.35
            if self.accroupi: #Si la touche flèche bas ou s est préssée alors on accélère la descente et on stoppe toute montée
                acc = a*4.5
                self.vy_initial = 0
            t=pygame.time.get_ticks()
            dift=(t-self.ti) #delta T
            self.vy = acc * dift - self.vy_initial #Formule MTRUV SI (les valeurs sont à l'opposé de ce que l'on a l'habitude de voir)
            self.pos_jump = self.pos_jump.move(0, self.vy) #Déplacement du rect avec la vitesse obtenue
            if (jauge == 0 and self.pos_jump.y <= h_saut_min) or (jauge == 1 and self.pos_jump.y <= h_saut_max): self.sens_jump = 0 #sens du dino (0 = vers le bas, 1 = vers le haut)
            if self.pos_jump.y > self.sol: #Donc si pos_jump y est en dessous du sol
                self.pos_jump.y = self.sol
                self.vy_initial = vitesse_y_init
                self.ti=0
                self.vy= 0

    def nuage(self):
        nuage_y = randint(int(self.dim_ecran[1]*0.26), int(self.dim_ecran[1]*0.7)) #Renvoie des coordonnées y aléatoires
        return nuage_y

    def choix_cac(self):
        obstacle_choisi = choice(obstacles) #On choisi un obstacle parmi la liste d'obstacles prévue dans constantes
        #On récupère l'image et le rect de cet obstacle
        img_obstacle_choisi = pygame.image.load(obstacle_choisi).convert_alpha()
        pos_obstacle_choisi = img_obstacle_choisi.get_rect(bottomleft = (self.dim_ecran[0]+1, self.dim_ecran[1]+2)) #On ajuste les positions pour que les cactus soient à la bonne place sur l'écran
        return img_obstacle_choisi, pos_obstacle_choisi

    def pts(self):
        temps_jeu = pygame.time.get_ticks() - self.temps_start_jeu #Mesure le temps depuis le lancement du jeu
        self.score = round(temps_jeu * 0.01) #On le divise par 100 puis on l'arrondi pour obtenir notre score (ce qui correspond à 1 point tous les 1 dixième de seconde)
        self.img_pts(self.score)

    def img_pts(self, score):
        nbr_zero = ("0000", "000", "00", "0") #Tuple qui permet d'ajouter le nombre de 0 nécéssaire pour avoir 5 caractères
        #On ajoute l'élement de la liste nbr_zero auquel la position correspond au nombre de caractères de self.score (ex: si self.score a 1 caractère on prend l'élément à la position 0 de la liste c'est à dire "0000")
        score_str = nbr_zero[len(str(score))-1] + str(score)
        #premier caractère à gauche
        self.affiche_score1 = score_str[0] #affiche_score1 prend la valeur du premier caractère
        self.affiche_score2 = score_str[1] #affiche_score2 prend la valeur du deuxième caractère
        self.affiche_score3 = score_str[2] #affiche_score3 prend la valeur du troisième caractère
        self.affiche_score4 = score_str[3] #affiche_score4 prend la valeur du quatrième caractère
        self.affiche_score5 = score_str[4] #affiche_score5 prend la valeur du cinquième caractère
        #prend l'élément dans la liste à la postion qui correspond aux affiche_scores
        img_score1 = img_scores[int(self.affiche_score1)]
        img_score2 = img_scores[int(self.affiche_score2)]
        img_score3 = img_scores[int(self.affiche_score3)]
        img_score4 = img_scores[int(self.affiche_score4)]
        img_score5 = img_scores[int(self.affiche_score5)]

        #On ne peut pas utiliser ici le .convert_alpha() car il calcule aussi la transparence pour chaque pixel, chaque pixel a donc une transparence différente
        #set_alpha() est fait pour modifier la transparence générale de l'image, l'utilisation des deux commandes est donc incompatible
        #c'est pour cela que l'on utilise à la place set_colorkey() qui permet de rendre tous les pixels d'une certaine couleur transparents
        #et cette commande fonctionne avec set_alpha()
        self.img_score1 = pygame.image.load(img_score1).convert()
        self.img_score2 = pygame.image.load(img_score2).convert()
        self.img_score3 = pygame.image.load(img_score3).convert()
        self.img_score4 = pygame.image.load(img_score4).convert()
        self.img_score5 = pygame.image.load(img_score5).convert()

        self.img_score1.set_colorkey((0, 0, 0))
        self.img_score2.set_colorkey((0, 0, 0))
        self.img_score3.set_colorkey((0, 0, 0))
        self.img_score4.set_colorkey((0, 0, 0))
        self.img_score5.set_colorkey((0, 0, 0))

        #On remet la transparence par défaut
        self.img_score1.set_alpha(255)
        self.img_score2.set_alpha(255)
        self.img_score3.set_alpha(255)
        self.img_score4.set_alpha(255)
        self.img_score5.set_alpha(255)

    def update_difficulty(self):
        #on veut que les deux derniers caractères soient 00, 01 ou 02 (01 et 02 c'est au cas où si on rate 00), cela permettra d'activer la condition à chaque fois que le score passe une centaine, de plus on active pas la condition si on est encore à 00000/00001/00002 et on veut qu'elle s'éxécute une fois par centaine
        if self.affiche_score4 == "0" and (self.affiche_score5 == "0" or self.affiche_score5 == "1" or self.affiche_score5 == "2") and self.affiche_score3 != self.affiche_score3_old:
            self.vitesse_sol *= multiplicateur_vitesse
            self.vitesse_pte_min *= multiplicateur_vitesse
            self.vitesse_pte_max *= multiplicateur_vitesse
            self.affiche_score3_old = self.affiche_score3

    def check_colli(self, pos_cac, pos_cac2, pos_cac3, pos_pte):
        #Ajuste les dimensions des rects pour la collision
        self.rect_colli_d = self.pos_jump.inflate(-25, -10)
        self.rect_colli_c = pos_cac.inflate(-15, 0)
        self.rect_colli_c2 = pos_cac2.inflate(-15, 0)
        self.rect_colli_c3 = pos_cac3.inflate(-15, 0)
        self.rect_colli_p = pos_pte.inflate(-15, 0)

        rects = (self.rect_colli_c, self.rect_colli_c2, self.rect_colli_c3, self.rect_colli_p)
        if self.accroupi and self.pos_jump.y == self.sol:
            for i in rects: #on prend chaque rect et on vérifie si il chevauche le rect du dino
                 if self.pos_accroupi.colliderect(i): self.colli = True
        else:
            for i in rects: #on prend chaque rect et on vérifie si il chevauche le rect du dino
                 if self.rect_colli_d.colliderect(i): self.colli = True

def convert_grandeur(value, leftMin, leftMax, rightMin, rightMax):
    # Calcule les ordres de grandeurs des deux parties
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convertit la valeur avec l'ordre de grandeur gauche pour donner une valeur entre 0 et 1
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convertit la valeur 0-1 avec l'ordre de grandeur droit pour donner une valeur dans cet ordre
    return rightMin + (valueScaled * rightSpan)

def put_image_dimension_to_rect(rec, img):
    #Renvoie la différence de dimension entre le rect et l'image pour qu'elle soit utilisée avec inflate
    diff_size = [0, 0]
    diff_size[0] = img.get_size()[0] - rec.size[0]
    diff_size[1] = img.get_size()[1] - rec.size[1]
    return diff_size
