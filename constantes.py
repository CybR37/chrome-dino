import os

#Images Accueil
image_dino_accueil=os.path.join("sprites","Dino","accueil.png")
icon_dino_accueil=os.path.join("sprites","Dino","accueil_icon.png")

#Images Env
image_bg=os.path.join("sprites", "Environnement", "fond.png")
image_sol=os.path.join("sprites", "Environnement", "sol.png")
image_nuage=os.path.join("sprites", "Environnement", "nuage.png")

#Images Obstacles
image_cactus_1p=os.path.join("sprites", "Obstacles", "cactus_1p.png")
image_cactus_2p=os.path.join("sprites", "Obstacles", "cactus_2p.png")
image_cactus_3p=os.path.join("sprites", "Obstacles", "cactus_3p.png")
image_cactus_2p2g=os.path.join("sprites", "Obstacles", "cactus_2p2g.png")
image_cactus_1g=os.path.join("sprites", "Obstacles", "cactus_1g.png")
image_cactus_2g=os.path.join("sprites", "Obstacles", "cactus_2g.png")
image_ptero1=os.path.join("sprites", "Obstacles", "ptero1.png")
image_ptero2=os.path.join("sprites", "Obstacles", "ptero2.png")
obstacles = [image_cactus_1p, image_cactus_2p, image_cactus_3p, image_cactus_2p2g, image_cactus_1g, image_cactus_2g]
proba_obs = ["ptero", "ptero", "cactus", "cactus", "cactus"]

#Images Dino
image_dino_arret=os.path.join("sprites", "Dino", "arret.png")
image_dino_marche1=os.path.join("sprites", "Dino", "marche1.png")
image_dino_marche2=os.path.join("sprites", "Dino", "marche2.png")
image_dino_accroupi1=os.path.join("sprites", "Dino", "accroupi1.png")
image_dino_accroupi2=os.path.join("sprites", "Dino", "accroupi2.png")
image_dino_dead=os.path.join("sprites", "Dino", "dead.png")

#Images Score
image_reboot=os.path.join("sprites", "Score","reboot.png")
image_gameover=os.path.join("sprites", "Score", "gameover.png")
image_0=os.path.join("sprites", "Score", "0.png")
image_1=os.path.join("sprites", "Score", "1.png")
image_2=os.path.join("sprites", "Score", "2.png")
image_3=os.path.join("sprites", "Score", "3.png")
image_4=os.path.join("sprites", "Score", "4.png")
image_5=os.path.join("sprites", "Score", "5.png")
image_6=os.path.join("sprites", "Score", "6.png")
image_7=os.path.join("sprites", "Score", "7.png")
image_8=os.path.join("sprites", "Score", "8.png")
image_9=os.path.join("sprites", "Score", "9.png")
image_HI=os.path.join("sprites", "Score", "HI.png")
img_scores = [image_0, image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9]

vitesse_sol= 5
vitesse_nuage = 1
vitesse_pte_max = 6
vitesse_pte_min = 4
multiplicateur_vitesse = 1.07

tps_apparition_intervalle_obs_max = 2
tps_apparition_intervalle_obs_min = 1

acc_saut_min = 0.0135 #plus la valeur est élévée plus le dino reste cloué au sol => valeur pygame.ticks env 910
h_saut_min = 264 #hauteur maximale du petit saut en y
acc_saut_max = 0.009 #plus la valeur est basse plus le dino peut aller haut  => valeur pygame.ticks env 1280
h_saut_max = 192 #hauteur maximale du grand saut en y
vitesse_y_init = 5.6666667
