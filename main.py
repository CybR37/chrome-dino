import pygame
from pygame.locals import *
from classes import *
from constantes import *
from random import randint, choice
from os import environ

dim_ecran = (900,500) #Dimension Ecran
environ['SDL_VIDEO_WINDOW_POS'] = "10, 40" #Détermine la position de la fenetre pour que l'IA lance mette son dispositif de capture à ces positions
pygame.init()

ecran = pygame.display.set_mode(dim_ecran)
bg = pygame.image.load(image_bg).convert()
bg = pygame.transform.scale(bg, dim_ecran) #Adaptation du fond à l'écran

#Icone et titre
icone = pygame.image.load(icon_dino_accueil).convert_alpha()
pygame.display.set_icon(icone)
pygame.display.set_caption("Chrome Dino IA")

dino, pos_nuage, pos_nuage2, pos_nuage3, pos_nuage4, pos_cac, pos_cac2, pos_cac3, cac, cac2, cac3, pos_pte, img_ptero, temps_trigger_n, temps_trigger_obs, pos_sol, vitesse_ptero, hauteurs = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
HIscore = 0
continuer = True
end = True

nuage = pygame.image.load(image_nuage).convert_alpha()

def temps(delay):
    t = pygame.time.get_ticks() + delay*1000
    return t

def write_file(score, colli): #Fonction pour ecrire dans globales.txt
    text = str(score)+","+str(colli) #On ajoute une virgule après le text pour que l'on puisse différencer les deux valeurs
    f = open("globales.txt", "w")
    f.write(text)
    f.close()

def nuage_f(etat): #Sur le jeu original il peut avoir jusqu'à 4 nuages affichés en même temps à l'écran
    global pos_nuage, pos_nuage2, pos_nuage3, pos_nuage4, temps_trigger_n
    if etat == "i": #i pour initial
        pos_nuage = nuage.get_rect(left = dim_ecran[0]+2)
        pos_nuage2 = nuage.get_rect(left = dim_ecran[0]+2)
        pos_nuage3 = nuage.get_rect(left = dim_ecran[0]+2)
        pos_nuage4 = nuage.get_rect(left = dim_ecran[0]+2)

    if etat == "r": #r pour récurrent
        #On définie quels nuages on va bouger (on les "active")
        if pygame.time.get_ticks() >= temps_trigger_n:
            if pos_nuage.x == dim_ecran[0]+2: pos_nuage.topleft = (dim_ecran[0]+1, dino.nuage()) #place les nuages à une position y aléatoire, tout à droite de l'ecran pour qu'ils ne soient pas visible au départ
            elif pos_nuage2.x == dim_ecran[0]+2: pos_nuage2.topleft = (dim_ecran[0] +1, dino.nuage())
            elif pos_nuage3.x == dim_ecran[0]+2: pos_nuage3.topleft = (dim_ecran[0] +1, dino.nuage())
            elif pos_nuage4.x == dim_ecran[0]+2: pos_nuage4.topleft = (dim_ecran[0] +1, dino.nuage())
            temps_trigger_n = temps(randint(1, 4)) #On attend 1 à 3 secondes pour exécuter la fonction

        if pos_nuage.x <= dim_ecran[0]+1: #On fait bouger les nuages "activés"
            pos_nuage = pos_nuage.move(-dino.vitesse_nuage, 0)
            if pos_nuage.x <= -nuage.get_width(): pos_nuage.x = dim_ecran[0]+2 #Si le nuage a une position egale ou inférieure à -(la dimension du nuage) alors on le "desactive" en le mettant à dim_ecran[0]+2
        #Idem pour les autres
        if pos_nuage2.x <= dim_ecran[0]+1:
            pos_nuage2 = pos_nuage2.move(-dino.vitesse_nuage, 0)
            if pos_nuage2.x <= -nuage.get_width(): pos_nuage2.x = dim_ecran[0]+2
        if pos_nuage3.x <= dim_ecran[0]+1:
            pos_nuage3 = pos_nuage3.move(-dino.vitesse_nuage, 0)
            if pos_nuage3.x <= -nuage.get_width(): pos_nuage3.x = dim_ecran[0]+2
        if pos_nuage4.x <= dim_ecran[0]+1:
            pos_nuage4 = pos_nuage4.move(-dino.vitesse_nuage, 0)
            if pos_nuage4.x <= -nuage.get_width(): pos_nuage4.x = dim_ecran[0]+2

        #On ajoute les couches des nuages à l'écran
        ecran.blit(nuage, pos_nuage)
        ecran.blit(nuage, pos_nuage2)
        ecran.blit(nuage, pos_nuage3)
        ecran.blit(nuage, pos_nuage4)

def obs():
    #On a jusqu'a 3 obstacles affichés en meme temps
    global cac, cac2, cac3, pos_cac, pos_cac2, pos_cac3, temps_trigger_obs, pos_pte, vitesse_ptero
    if pygame.time.get_ticks() >= temps_trigger_obs:  #Y a des chances que le programme rate le moment où pygame.time.get_ticks() == temps_trigger_obs alors je préfère mettre >=
        if dino.score >= 450: choix = choice(proba_obs) #Si le dino a passé le cap des 450 points
        else: choix = "cactus"

        if choix == "ptero" and pos_pte.x == dim_ecran[0]+2: #Si le choix tombe sur le ptero et si il est disponible/non activé, si il n'est pas disponible alors on ne fait pas apparaitre d'obstacles et on n'actualise pas le temps ce qui veut dire qu'il n'y a pas de temps d'attente pour le prochain obstacle
            pos_pte = pos_pte.inflate(put_image_dimension_to_rect(pos_pte, img_ptero)) #On ajuste la taille du rect pour qu'il prenne la forme de l'image
            #Au moment de définir la position du ptero sur y on remonte ou on abaisse le ptero en fonction de l'etat de l'animation du ptero
            if dino.etat_p == 1: pos_pte.midleft = (dim_ecran[0]+1, choice(hauteurs)-12)
            else: pos_pte.midleft = (dim_ecran[0]+1, choice(hauteurs)+12)
            vitesse_ptero = randint(round(dino.vitesse_pte_min), round(dino.vitesse_pte_max)) #Sur le vrai jeu la vitesse peut varier
            #On attend entre l'intervalle minimum et maximum secondes pour exécuter la fonction (on ajoute 1 seconde au temps minimal pour eviter qu'un obstacle arrive juste après le ptero, si c'était le cas et que le ptero va moins vite que le sol on ne pourrai ni se baisser ni sauter)
            temps_trigger_obs = temps(randint(tps_apparition_intervalle_obs_min+1, tps_apparition_intervalle_obs_max))

        elif choix == "cactus":
            #On vérifie si l'obstacle 1 est actif, si non on lui donne l'image et le rect, idem pour les autres
            if pos_cac.x == dim_ecran[0]+2: cac, pos_cac = dino.choix_cac()
            elif pos_cac2.x == dim_ecran[0]+2: cac2, pos_cac2 = dino.choix_cac()
            elif pos_cac3.x == dim_ecran[0]+2: cac3, pos_cac3 = dino.choix_cac()

            #On ajuste la taille du rect pour qu'il prenne la forme de l'image
            pos_cac = pos_cac.inflate(put_image_dimension_to_rect(pos_cac, cac))
            pos_cac2 = pos_cac2.inflate(put_image_dimension_to_rect(pos_cac2, cac2))
            pos_cac3 = pos_cac3.inflate(put_image_dimension_to_rect(pos_cac3, cac3))

            temps_trigger_obs = temps(randint(tps_apparition_intervalle_obs_min, tps_apparition_intervalle_obs_max)) #On attend entre l'intervalle minimum et maximum secondes pour exécuter la fonction


    if pos_cac.x <= dim_ecran[0]+1: #On fait bouger les cactus "activés"
        pos_cac = pos_cac.move(-round(dino.vitesse_sol), 0)  #Due au multiplicateur de vitesse dino.vitesse_sol devient un nombre décimal et les rects gèrent mal les nombres décimaux donc je préfère l'arrondir
        if pos_cac.x <= -cac.get_width(): pos_cac.x = dim_ecran[0]+2 #Si l'obstacle a une position egale ou inférieure à -(la dimension de l'obstacle) alors on le "desactive" en le mettant à dim_ecran[0]+2
    #Idem pour les autres
    if pos_cac2.x <= dim_ecran[0]+1:
        pos_cac2 = pos_cac2.move(-round(dino.vitesse_sol), 0)
        if pos_cac2.x <= -cac2.get_width(): pos_cac2.x = dim_ecran[0]+2
    if pos_cac3.x <= dim_ecran[0]+1:
        pos_cac3 = pos_cac3.move(-round(dino.vitesse_sol), 0)
        if pos_cac3.x <= -cac3.get_width(): pos_cac3.x = dim_ecran[0]+2

    if pos_pte.x <= dim_ecran[0]+1: #On fait bouger les pteros "activés"
    #On veut que le ptero change sa position sur y en fonction de l'etat de l'animation mais on veut qu'il la change que une fois par changement d'animation, le dino.etat_p_old est une sorte de sécurité pour s'assurer qu'il la change qu'une fois, si il la change plusieurs fois alors le ptero ferait du +12, +12, +12,..., -12, -12, -12, etc...
    #Alors que l'on veut qu'il fasse du +12, -12, +12, -12, etc...
        if dino.etat_p == 1 and dino.etat_p != dino.etat_p_old: pos_pte.centery = pos_pte.centery -12 #Si l'etat du ptero est 1 et que l'état vient de changer de valeur alors on remonte le ptero sur y
        elif dino.etat_p == 2 and dino.etat_p != dino.etat_p_old: pos_pte.centery = pos_pte.centery +12 #Si l'etat du ptero est 2 et que l'état vient de changer de valeur alors on abaisse le ptero sur y
        pos_pte = pos_pte.inflate(put_image_dimension_to_rect(pos_pte, img_ptero)) #On ajuste la taille du rect pour qu'il prenne la forme de l'image
        pos_pte = pos_pte.move(-vitesse_ptero, 0)
        dino.etat_p_old = dino.etat_p
        if pos_pte.x <= -img_ptero.get_width(): pos_pte.x = dim_ecran[0]+2 #Si l'obstacle a une position egale ou inférieure à -(la dimension de l'obstacle) alors on le "desactive" en le mettant à dim_ecran[0]+2

    #On ajoute les couches des obstacles à l'écran
    ecran.blit(cac, pos_cac)
    ecran.blit(cac2, pos_cac2)
    ecran.blit(cac3, pos_cac3)
    ecran.blit(img_ptero, pos_pte)

def jeu():
    comp = 0
    pygame.key.set_repeat(1,1)
    global continuer, end, dino, temps_trigger_n, pos_cac, pos_cac2, pos_cac3, cac, cac2, cac3, temps_trigger_obs, pos_pte, img_ptero, pos_sol, HIscore, hauteurs
    compteur = 0.05 #correspond à l'accélération
    jauge_jump = 0

    dino = perso(50, dim_ecran[1]*0.95-70) #Crée le dino

    sol = pygame.image.load(image_sol).convert_alpha()  #Définition des deux images "sol"
    pos_sol = sol.get_rect(topleft =(0, round(dim_ecran[1]*0.95))) #On utilise les dimensions de l'ecran avec des multiplications/divisions pour garder une valeur relative à l'ecran
    pos_sol2 = pos_sol.copy() #On copie la première pour faire la seconde
    pos_sol2.topleft = (sol.get_width(), round(dim_ecran[1]*0.95))

    HI = pygame.image.load(image_HI).convert()
    HI.set_colorkey((0, 0, 0)) #Tout ce qui est noir dans l'image HI devient transparent

    temps_trigger_n = temps(0) #Temps avant éxecution de la fonction pour la première fois
    temps_trigger_obs = temps(3) #Temps avant éxecution de la fonction pour la première fois
    tps_anim_d = temps(0) #Temps avant éxecution de la fonction pour la première fois
    tps_anim_p = temps(0) #Temps avant éxecution de la fonction pour la première fois

    #Initialisation
    #On met des images par défaut pour les obstacles meme si elles ne correspondent pas (car on ne les verras pas)
    cac, pos_cac = dino.obs_defaut, dino.pos_obs_defaut
    cac2, pos_cac2 = dino.obs_defaut, dino.pos_obs_defaut
    cac3, pos_cac3 = dino.obs_defaut, dino.pos_obs_defaut
    pos_pte = dino.pos_obs_defaut
    charge_jump = False
    t_charge_depart = 0
    acc = acc_saut_min

    #partie ptero/ le ptero peut apparaitre à 3 niveaux différents: au pieds du dino, à la tete et au dessus de la tete
    h_sol = 441 #ptero1 et 2 font la meme taille donc peu importe => on prends la position sol en enlèvant la hauteur de ptero pour pas que ptero soit sous le sol
    h_tete = 364 #on enlève 15 à la position (prise en haut à gauche) pour aligner le corps du ptero à la tete du dino
    h_ciel = 320 #pour etre sûr que le ptero passe au dessus du Dino
    hauteurs = (h_sol, h_tete, h_ciel) #On forme un tuple pour choisir la hauteur

    #Sur le jeu original il peut avoir jusqu'à 4 nuages affichés en même temps à l'écran
    nuage_f("i")

    #Boucle principale du jeu
    while continuer:
        pygame.time.Clock().tick(160) #On limite la boucle pour qu'elle s'éxecute au maximum 160 fois par secondes
        ecran.blit(bg, (0,0))
        if dino.colli:
             #si on implémente pas de compteur on verrait le dino stoppé qui ne touche pas le cactus alors que pourtant c'est le cas, alors je décide de faire X fois la boucle principale le temps que la position du dino arrive sur le cactus puis on commence la boucle de fin
            """if comp < 10 and dino.pos_jump.colliderect(pos_pte):
                comp += 1
            elif comp < 5 and dino.pos_jump.colliderect(pos_pte) == False:
                comp += 1"""
            #else:
            dino.etat_d = 0 #on met l'état du dino à 0 qui correspond qu'il a percuté un obstacle
            if dino.accroupi: dino.pos_jump.y = dino.y
            dino.pos_jump.y += 5 #Comme l'image du dino quand il est marche et l'image du dino quand il est mort n'est pas la meme on ajuste alors la position du dino
            #On remet les différentes couches d'image dans l'ordre pour enlever les images à la mauvaise taille/mauvaise position
            ecran.blit(dino.img_score1, (dim_ecran[0]-140, 30))
            ecran.blit(dino.img_score2, (dim_ecran[0]-120, 30))
            ecran.blit(dino.img_score3, (dim_ecran[0]-100, 30))
            ecran.blit(dino.img_score4, (dim_ecran[0]-80, 30))
            ecran.blit(dino.img_score5, (dim_ecran[0]-60, 30))
            ecran.blit(sol, pos_sol)
            ecran.blit(sol, pos_sol2)
            ecran.blit(nuage, pos_nuage)
            ecran.blit(nuage, pos_nuage2)
            ecran.blit(nuage, pos_nuage3)
            ecran.blit(nuage, pos_nuage4)
            ecran.blit(cac, pos_cac)
            ecran.blit(cac2, pos_cac2)
            ecran.blit(cac3, pos_cac3)
            ecran.blit(img_ptero, pos_pte)
            ecran.blit(dino.dead, dino.pos_jump)
            if dino.score > HIscore: HIscore = dino.score
            dino.img_pts(HIscore)
            #on déplace les coordonnées HIscore de 120 vers la gauche par rapport au score classique
            #On rend légèrement transparent le HIscore
            dino.img_score1.set_alpha(190)
            dino.img_score2.set_alpha(190)
            dino.img_score3.set_alpha(190)
            dino.img_score4.set_alpha(190)
            dino.img_score5.set_alpha(190)
            HI.set_alpha(190)
            ecran.blit(HI, (dim_ecran[0]-320, 30))
            ecran.blit(dino.img_score1, (dim_ecran[0]-260, 30))
            ecran.blit(dino.img_score2, (dim_ecran[0]-240, 30))
            ecran.blit(dino.img_score3, (dim_ecran[0]-220, 30))
            ecran.blit(dino.img_score4, (dim_ecran[0]-200, 30))
            ecran.blit(dino.img_score5, (dim_ecran[0]-180, 30))
            ecran.blit(dino.gameover, (dim_ecran[0]-625, dim_ecran[1]/2-50))
            ecran.blit(dino.reboot, (dim_ecran[0]/2-25, dim_ecran[1]/2))

            pygame.display.flip() #sert à actualiser les images qu'on a mis pour les images de gameover
            end = True
            while end:  #on entre dans une autre boucle pour que les actions qui suivent dans le programme ne soient plus effectuées

                for event in pygame.event.get():
                    if event.type == QUIT:
                        continuer = False
                        end = False #le end à False termine la boucle ci-dessus tandis que le continuer termine la boucle principale

                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            continuer = False
                            end = False
                        if event.key == K_SPACE or event.key == K_UP: end = False
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        end = False

            break #une fois qu'une touche ci-dessus a été préssée pour mettre continuer à False on quitte la boucle du jeu ca qui arretera le programme

        if end == False:
            dino.img_pts(HIscore)
            #On rend légèrement transparent le HIscore
            dino.img_score1.set_alpha(190)
            dino.img_score2.set_alpha(190)
            dino.img_score3.set_alpha(190)
            dino.img_score4.set_alpha(190)
            dino.img_score5.set_alpha(190)
            HI.set_alpha(190)
            ecran.blit(HI, (dim_ecran[0]-320, 30))
            ecran.blit(dino.img_score1, (dim_ecran[0]-260, 30))
            ecran.blit(dino.img_score2, (dim_ecran[0]-240, 30))
            ecran.blit(dino.img_score3, (dim_ecran[0]-220, 30))
            ecran.blit(dino.img_score4, (dim_ecran[0]-200, 30))
            ecran.blit(dino.img_score5, (dim_ecran[0]-180, 30))

        dino.pts()
        ecran.blit(dino.img_score1, (dim_ecran[0]-140, 30))
        ecran.blit(dino.img_score2, (dim_ecran[0]-120, 30))
        ecran.blit(dino.img_score3, (dim_ecran[0]-100, 30))
        ecran.blit(dino.img_score4, (dim_ecran[0]-80, 30))
        ecran.blit(dino.img_score5, (dim_ecran[0]-60, 30))


        pos_sol = pos_sol.move(-round(dino.vitesse_sol), 0) #Due au multiplicateur de vitesse dino.vitesse_sol devient un nombre décimal et les rects gèrent mal les nombres décimaux donc je préfère l'arrondir
        pos_sol2 = pos_sol2.move(-round(dino.vitesse_sol), 0)
        if pos_sol.x <= -sol.get_width(): #Si l'image a dépassée sa taille (et ducoup entamé la 2nde image) il remet les deux images en place
            pos_sol.x = 0                #cela permet d'avoir une bande défilante infinie et ca ne fait pas de coupure
            pos_sol2.x = sol.get_width()

        ecran.blit(sol, pos_sol)
        ecran.blit(sol, pos_sol2)

        if pygame.time.get_ticks() >= tps_anim_d:
            img_dino = dino.run() #Recupère la bonne image du dino
            tps_anim_d = temps(0.09)
        if pygame.time.get_ticks() >= tps_anim_p:
            img_ptero = dino.ptero() #Recupère la bonne image du ptero
            tps_anim_p = temps(0.2)

        dino.jump(compteur, jauge_jump) #Saut avec une certaine accélération (de base 0.05)
        dino.update_difficulty()

        nuage_f("r")
        obs()

        ecran.blit(img_dino, (dino.pos_jump)) #Envoie la bonne image du dino en train de courir

        pygame.display.flip()

        dino.check_colli(pos_cac, pos_cac2, pos_cac3, pos_pte) #si on détecte une collision on met dino.colli à True
        write_file(dino.score, dino.colli) #met la valeur de la variable collision dans globales.txt

        keys = pygame.key.get_pressed()     #Récupère les touches préssées pour savoir si la touche flèche bas est préssée
        if keys[K_DOWN] or keys[K_s]: dino.accroupi = True
        else: dino.accroupi = False

        acc_moy = (acc_saut_min + acc_saut_max)/2 #on fait la moyenne des accélérations extrêmes pour utiliser cette moyenne afin de définir si on a fait un saut long ou court
        charge_jump_old = charge_jump #charge_jump_old prend la valeur que possède charge_jump
        if (keys[K_UP] or keys[K_SPACE] or keys[K_d]) and dino.accroupi == False and dino.pos_jump.y == dino.sol: #Si l'une des trois touches est préssée
            charge_jump = True
            if t_charge_depart == 0: #On définit un temps de départ pour le jaugeage des touches de saut
                t_charge_depart = pygame.time.get_ticks() -1 #Pour eviter la division par 0 plus bas
        if charge_jump: #Si on est en saut
            t_charge = pygame.time.get_ticks() - t_charge_depart #On enlève au temps actuel le temps de départ pour obtenir le temps qu'il s'est passé depuis t_charge_depart
            #Comme on atteindra quasiment jamais les valeurs de temps en dessous de 25 ticks (on est pas assez réactif) alors on dit que la valeur la plus basse est 25 (donc dans le calcul ci-dessous c'est 1/25 la plus haute)
            acc = convert_grandeur(1/t_charge, 1/1280, 1/28, acc_saut_max, acc_saut_min) #On inverse toutes les valeurs car on souhaite avoir une accélération décroissante en fonction d'un temps croissant

        if (keys[K_UP] == False and keys[K_SPACE] == False and keys[K_d] == False and charge_jump_old) or acc < acc_moy: #Si les touches ne sont plus préssées ou que l'accélération max est quasiment atteinte (on ne charche pas l'acc max car on mettra beaucoup de temps avant de l'atteindre)
            charge_jump = False
            #Si la valeur de l'accélération est dans la partie haute (donc si on a pas appuyé longtemps) alors on applique l'accélération maximale, sinon on applique la minimale
            if acc_saut_min > acc > acc_moy:
                acc = acc_saut_min
                jauge_jump = 0 #Et on donne la valeur 0 à jauge_jump (0 = Petit saut, 1 = Grand saut)
            elif acc_moy > acc > acc_saut_max:
                acc = acc_saut_max
                jauge_jump = 1
            compteur = acc #Le compteur prend la valeur de acc et remet acc à 0.0135
            acc = acc_saut_min
            dino.jump_init() #On initialise au passage le saut pour
            dino.jump(compteur, jauge_jump) #On effectue le saut pour la première fois
            t_charge_depart = 0 #On remet à 0 le temps de départ

        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: continuer = False

                """if event.key == K_SPACE and dino.accroupi == False:
                    if dino.pos_jump.y == dino.sol:
                        dino.jump_init()
                        compteur = acc_hauteur_min #acc correspondant à hauteur min
                        print(compteur)
                    if compteur > acc_hauteur_max and dino.vy > 0: #acc correspondant à hauteur max
                        compteur -= variation_acc #variation de l'acc (permet de connaitre la durée de ESPACE préssé et de varier acc en conséquence)
                        print(compteur)

                if event.key == K_UP and dino.accroupi == False:
                    if dino.pos_jump.y == dino.sol:
                        t_charge_depart = 0
                        dino.jump_init()
                        compteur = acc_hauteur_min #acc correspondant à hauteur min
                    if compteur > acc_hauteur_max and dino.vy > 0: #acc correspondant à hauteur max
                        compteur -= variation_acc #variation de l'acc (permet de connaitre la durée de FLECHE_HAUT préssé et de varier acc en conséquence)"""
                        #Trouver le moyen de doser correctement la longue de pression de ESPACE
                        #Problème: ne va pas très haut car il applique d'abord 0.05 d'acc puis un peu moins, etc...
                        #Je me dis que si on faisait un graph de l'acc en fct du temps on obtiendrait un logarithme néperien
                        #Faut ptet essayer une fonction exponentielle pour contre-balancer
while continuer:
    jeu()
pygame.quit()
