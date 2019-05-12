import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D
import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from entre_direct import PressKey, ReleaseKey, W, S,D
from collections import deque
import random
liste = [0, "False"]

def read_file(): #Fonction utilisée pour lire le texte de globales.txt
    global liste
    l = []
    f = open("globales.txt", "r")
    f_str = f.read()
    f.close()
    l = f_str.split(",")
    if len(l) == 2:
        liste = l
        if liste[1] == "False": liste[1] = False
        elif liste[1] == "True": liste[1] = True
        liste = [int(liste[0]), liste[1]]
        return liste
    else: return liste

#paramètres du jeu
GAMMA = 0.99 # diminution des observations passé original 0.99
OBSERVATION = 500000. # étape de temps avant de commencer l'entrainement
EXPLORE = 100000  # nombre d'images sur lesquelles on diminue epsilon
FINAL_EPSILON = 0.0001 # valeur finale d'epsilon epsilon
INITIAL_EPSILON = 1 # valeur de départ d'epsilon
REPLAY_MEMORY = 50000 # nombre d'essais précedent à se rappeler
BATCH = 32 # taille du mini batch
FRAME_PER_ACTION = 1

def process_img(printscreen):
    new_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY) #passer l'image en noir et banc
    Image = cv2.Canny(new_img, threshold1 = 200, threshold2=500) #détecter les contoures des objet du jeux
    return Image
def screen_record():
    printscreen =  np.array(ImageGrab.grab(bbox=(0,250,900,510))) #Capturer l'image du jeux
    Final_Image = process_img(printscreen) #L'adapter pour l'IA
    #cv2.imshow('window',Image ) #montrer ce que voi l'IA si on veut
    #cv2.moveWindow('window', 0,500) #décaler la fenêtre de vue pour être toujours en dessous de la fenêtre de jeuxs
    return Final_Image
'''
* Game class: les actions pour interagir avec python
* get_crashed() : renvoie vrai si le dino est crashé. récupère une variable globale crée au début et partagé avec le jeux qui la met à jour
* get_playing(): renvoie l'inverse de la varable crash
* restart() : envoie un sigal au jeux pour le redémarrer
* get_score(): récuperrer le score actuel du jeux.
'''
class Game:
    def get_crashed(self):
        colli = read_file()[1]#récuperer la variable de collision écrite par le fichier du jeux
        return colli #renvoyer la valeur de collision
    def restart(self):#c'est pour lancer le jeux si le dino est mort
        print('restart')# renvoyer un message pour voir si le programme à bien demmendé de redemarrer ou si c'est juste la commande du saut qui as fait ça
        pyautogui.press('space')
        time.sleep(0.25)# aucune action n'est possible pendant 0.25 sec car cela fait attendre le model pour qu'il apprenne seulement quand les jeux est lancé
    def get_score(self):
        Score = read_file()[0]#récuperer la variable de score écrite par le fichier du jeux
        return Score #renvoyer la valeur du collision
class DinoAgent:
    def __init__(self,game): #récupère les donné sur le jeux et l'initialise
        self._game = game;
        '''self.jump(); #pour démarrer le jeux on doit sauter une première fois
        time.sleep(.5) #aucne action n'est possible quand le jeux démarre'''
    def is_crashed(self):
        return self._game.get_crashed()
    def jump(self):
        print('saut')# renvoyer un message pour voir si le programme à demandé de sauter
        PressKey(D)
        time.sleep(0.2)
        ReleaseKey(D)
    def duck(self):#appuye est relache la touche pour se baisser
        print('duck')
        PressKey(S)
        time.sleep(0.2)
        ReleaseKey(S)
class Game_state:
    def __init__(self,agent,game):
        self._agent = agent
        self._game = game
    def get_state(self,actions):
        colli = self._game.get_crashed()
        Score = read_file()[0]
        print(colli)
        print(Score)
        score = self._game.get_score()
        reward = score/100 # calcul de récompense dynamique
        is_over = False #game over
        if actions[1] == 1: #sinon se baisser
            self._agent.jump()
            reward = 0.1*score/11
        else:
            self._agent.duck()
        image = screen_record()

        if self._agent.is_crashed():
            self._game.restart()
            reward = -11/score
            is_over = True
        return image, reward, is_over #renvoie l'experience en tuple
LEARNING_RATE = 1e-4
img_rows , img_cols = 900,260
img_channels = 4 #on met les images par groupe de 4
ACTIONS = 2
def buildmodel():
    print("Now we build the model")
    model = Sequential()
    model.add(Conv2D(1024, (8, 8), strides=(4, 4), padding='same',input_shape=(img_cols,img_rows,img_channels)))  #260*900*4
    model.add(Activation('relu'))
    model.add(Conv2D(2048, (4, 4), strides=(2, 2), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(1024, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(512, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(ACTIONS))
    model.add(Activation('relu'))
    adam = keras.optimizers.Adam(lr=LEARNING_RATE)
    model.compile(loss='mse',optimizer=adam)
    print("We finish building the model")
    return model
'''
Parameters:
* model => Keras Model to be trained
* game_state => Game State module with access to game environment and dino
* observe => flag to indicate wherther the model is to be trained(weight updates), else just play
'''
def trainNetwork(model,game_state):
    # on enregistre l'observation précedente dans replay memory
    D = deque() #on charche depuis le système de fichier
    #on récupère le premier état en faisant rien
    do_nothing = np.zeros(ACTIONS)
    do_nothing[0] =1 #0 => ne rien faire,
                     #1=> sauter

    x_t, r_0, terminal = game_state.get_state(do_nothing) # récuperer la prochaine étape après avoir éffectué une action
    s_t = np.stack((x_t, x_t, x_t, x_t), axis=2).reshape(1,260,900,4) # gropuper 4 images pour créer l'input de 1*260*900*4

    OBSERVE = OBSERVATION
    epsilon = INITIAL_EPSILON
    t = 0
    while (True): #boucle sans fin

        loss = 0
        Q_sa = 0
        action_index = 0
        r_t = 0 #on réinitialise la récompense
        a_t = np.zeros([ACTIONS]) # on reset l'action

        #on choisis une action a effectuer
        if  random.random() <= epsilon: #on met une action de manière random
            print("----------Random Action----------")
            action_index = random.randrange(ACTIONS)
            a_t[action_index] = 1
        else: #ou on effectue une action prédit par notre IA
            q = model.predict(s_t)       #envoie le pack de 4 image préparé à notre réseau de neurones pour qu'il les traite
            max_Q = np.argmax(q)         # choisir l'index avec la valeur maximum q
            action_index = max_Q
            a_t[action_index] = 1     # o=> se baisser, 1=> sauter

        #We reduced the epsilon (exploration parameter) gradually
        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        #run the selected action and observed next state and reward
        x_t1, r_t, terminal = game_state.get_state(a_t)
        last_time = time.time()
        x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1) #1x20x40x1
        s_t1 = np.append(x_t1, s_t[:, :, :, :3], axis=3) # append the new image to input stack and remove the first one

        # store the transition in D
        D.append((s_t, action_index, r_t, s_t1, terminal))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        #only train if done observing; sample a minibatch to train on
        if t > OBSERVE:
            trainBatch(random.sample(D, BATCH))
        s_t = s_t1
        t = t + 1
        print("TIMESTEP", t, "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t,"/ Q_MAX " , np.max(Q_sa), "/ Loss ", loss)
def trainBatch(minibatch):
  inputs = np.zeros((BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))   #32, 20, 40, 4
  targets = np.zeros((inputs.shape[0], ACTIONS))                         #32, 2
  loss = 0

  for i in range(0, len(minibatch)):
                state_t = minibatch[i][0]    # 4D stack of images
                action_t = minibatch[i][1]   #This is action index
                reward_t = minibatch[i][2]   #reward at state_t due to action_t
                state_t1 = minibatch[i][3]   #next state
                terminal = minibatch[i][4]   #wheather the agent died or survided due the action
                inputs[i:i + 1] = state_t
                targets[i] = model.predict(state_t)  # predicted q values
                Q_sa = model.predict(state_t1)      #predict q values for next step
                if terminal:
                    targets[i, action_t] = reward_t # if terminated, only equals reward
                else:
                    targets[i, action_t] = reward_t + GAMMA * np.max(Q_sa)

                loss += model.train_on_batch(inputs, targets)
#argument: observe, only plays if true, else trains
def playGame(observe=False):
    time.sleep(2)
    game = Game()
    dino = DinoAgent(game)
    game_state = Game_state(dino,game)
    model = buildmodel()
    trainNetwork(model,game_state)
playGame(observe=False)
