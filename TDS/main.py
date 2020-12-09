# Magnes Simon
# Luk Brian
# Gortz Gaetan
# Temmerman François

import numpy
import cv2
import Personne

# Compteur descendant/montant/total
cnt_total = 0
cnt_up = 0
cnt_down = 0

#Chemin vers la video
cap = cv2.VideoCapture('Videos/simon.mp4')

# propriétés vidéo
# TODO Récupérer données automatiquement
h = 480
w = 640
frameArea = h * w
areaTH = frameArea / 250


# trace la ligne de passage
# TODO tracer la ligne à la moitié de l'image
line = int(200)
line_color = (255, 255,0)

pt1 = [0, line];
pt2 = [w, line];
pts_L1 = numpy.array([pt1, pt2], numpy.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))


# Soustracteur d'arrière-plan
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 250, detectShadows=False)

# Eléments structurants pour filtres morphogiques
matriceOuverture = numpy.ones((3, 3), numpy.uint8)
matriceFermeture = numpy.ones((11, 11), numpy.uint8)

# Variables
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

while (cap.isOpened()):
    # Lit une image de la video
    ret, frame = cap.read()

    # augmente le temps mémoire pour chaque objet personness
    for i in persons:
        i.temps_memoire()

    # Pré-traitement
    # Appliquer le filtre de soustraction
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    #Binaire pour supprimer les ombres (color gris)
    try:
        ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        ret, imBin2 = cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)
         # erosion suivi de dilatation pour enlever le bruit
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, matriceOuverture)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, matriceOuverture)
         # dilatation suivi d'erosion pour enlever les points noirs dans l'objet detecté
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, matriceFermeture)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, matriceFermeture)
    except:
        print('Fin du fichier')
        break

    # Contours
    # Garder les contours extremes et pas les petits à l'intérieur
    contours0, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:
            # Tracking
            # coordonées des gens (point rouge)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # rectangle contour
            x, y, w, h = cv2.boundingRect(cnt)

            new = True

            for i in persons:
                if abs(x - i.x) <= w and abs(y - i.y) <= h:
                    # l'objet est proche de celui qui a déjà été détecté auparavant
                    new = False
                    i.updateCoordonnees(cx, cy)  # met à jour les coordonnées dans personnes
                    if i.going_UP(line) == True:
                        cnt_up += 1;
                        cnt_total += 1;
                    elif i.going_DOWN(line) == True:
                        cnt_down += 1;
                        cnt_total -= 1;
                    break

                if i.done:
                    # supprimer i de la liste des personnes
                    index = persons.index(i)
                    persons.pop(index)
                    del i  # retire i de la mémoire
            if new == True:
                p = Personne.MyPerson(pid, cx, cy, max_p_age)
                persons.append(p)
                pid += 1

            # Dessins
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Desssin des pistes
    for i in persons:
        cv2.putText(frame, str(i.i), (i.x, i.y), font, 0.3, [i.R, i.G, i.B], 1, cv2.LINE_AA)

    # Images
    str_up = 'In: ' + str(cnt_up)
    str_down = 'Out: ' + str(cnt_down)
    str_total = 'Total: ' + str(cnt_total)
    frame = cv2.polylines(frame, [pts_L1], False, line_color, thickness=2)
    cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, str_down, (10, 60), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, str_total, (10, 80), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    # temps de refresh
    k = cv2.waitKey(15) & 0xff
    # appuyez sur ESC pour quitter
    if k == 27:
        break

# Libère fichier de lecture et ferme les fenetres
cap.release()
cv2.destroyAllWindows()

