import pygame
from random import randint

TAILLE_GRILLE = 5
TAILLE_FENETRE = 600

K = 5

TAILLE_CASE = TAILLE_FENETRE // TAILLE_GRILLE

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
VERT_CLAIR = (144, 238, 144)

class Grille :
    def __init__(self, M, K) -> None:
        self.M = M
        self.K = K
        self.grille = self.genererGrille()
        self.casesRestantes = M*M-K

    def genererGrille(self):
        grille = [[0] * self.M for _ in range(self.M)]

        for _ in range(self.K):
            while True :
                x = randint(0, self.M - 1)
                y = randint(0, self.M - 1)
                if grille[x][y] != 1:
                    grille[x][y] = 1
                    break

        return grille
    
    def dessiner(self, screen):
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                couleur = BLANC
                pygame.draw.rect(screen, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
                pygame.draw.rect(screen, NOIR, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)


class Player:
    def __init__(self) -> None:
        self.tune = 500
        self.mise = 50

class Bouton:
    def __init__(self, x, y, l, h, text, textCouleur, couleur, couleurSubbriance) -> None:
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.text = text
        self.textCouleur = textCouleur
        self.couleur = couleur
        self.couleurSubbriance = couleurSubbriance

    def dessiner(self, screen):
        positionSouris = pygame.mouse.get_pos()

        if self.x < positionSouris[0] < self.x + self.l and self.y < positionSouris[1] < self.y + self.h:
            pygame.draw.rect(screen, self.couleurSubbriance, (self.x, self.y, self.l, self.h))
        else :
            pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.l, self.h))

        font = pygame.font.SysFont(None, 36)
        textSurface = font.render(self.text, 1, self.textCouleur)
        textRectangle = textSurface.get_rect(center = (self.x + self.l / 2, self.y + self.h / 2))
        screen.blit(textSurface, textRectangle)

    def dessinerPetit(self, screen):
        positionSouris = pygame.mouse.get_pos()

        if self.x < positionSouris[0] < self.x + self.l and self.y < positionSouris[1] < self.y + self.h:
            pygame.draw.rect(screen, self.couleurSubbriance, (self.x, self.y, self.l, self.h))
        else :
            pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.l, self.h))

        font = pygame.font.SysFont(None, 36)
        textSurface = font.render(self.text, 1, self.textCouleur)
        textRectangle = textSurface.get_rect(center = (self.x + self.l / 2, self.y + self.h / 2))
        screen.blit(textSurface, textRectangle)

    def estClique(self, positionSouris):
        return self.x < positionSouris[0] < self.x + self.l and self.y < positionSouris[1] < self.y + self.h
    

class Jeu:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((TAILLE_FENETRE + 200, TAILLE_FENETRE))
        pygame.display.set_caption("Démineur")
        self.grille = Grille(TAILLE_GRILLE, K)
        self.player = Player()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.initialiserGrille()
        self.multiplicateur = 1
        self.M = TAILLE_GRILLE * TAILLE_GRILLE
        self.caseTrouvees = 0
        
        self.perdu = False
        self.boutonRecommencer = None
        self.boutonEncaisser = Bouton(TAILLE_FENETRE+25, TAILLE_FENETRE-100, 150, 50, "Encaisser", BLANC, ROUGE, VERT)
        
        self.casesRevelees = []
        self.afficherProchainMultiplicateur()        

    def reveler(self, screen, x, y):
        if (x, y) in self.casesRevelees:
            return False
        else:
            self.casesRevelees.append((x, y))

        if self.grille.grille[x][y] == 0:
            couleur = VERT
            self.grille.casesRestantes -= 1
        else:
            couleur = ROUGE
            pygame.draw.rect(screen, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
            pygame.draw.rect(screen, NOIR, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)
            pygame.display.update()
            return True
        pygame.draw.rect(screen, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(screen, NOIR, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)
        self.afficherProchainMultiplicateur()
        return False

    def afficherArgent(self):
        argentText = self.font.render(f"Argent : {self.player.tune}", True, BLANC)
        argentRect = argentText.get_rect()
        argentRect.topright = (TAILLE_FENETRE + 150, 20)
        self.screen.blit(argentText, argentRect)

    def afficherMise(self):
        miseText = self.font.render(f"Mise : {self.player.mise}", True, BLANC)
        miseRect = miseText.get_rect()
        miseRect.topright = (TAILLE_FENETRE + 150, 70)
        self.screen.blit(miseText, miseRect)

    def afficherProchainMultiplicateur(self):
        self.multiplicateur = round(self.multiplicateur * ((self.M - self.caseTrouvees) / self.grille.casesRestantes), 2)
        self.caseTrouvees += 1
        #self.multiplicateur = round(self.multiplicateur * 1.25, 2)
        multiplicateurText = self.font.render(f"Next : x{self.multiplicateur}", True, BLANC)
        multiplicateurRect = multiplicateurText.get_rect()
        multiplicateurRect.topright = (TAILLE_FENETRE + 150, 120)
        self.screen.blit(multiplicateurText, multiplicateurRect)


    def initialiserGrille(self):
        self.screen.fill(NOIR)
        self.grille.dessiner(self.screen)
        pygame.display.flip()

    def perdre(self):
        pygame.time.delay(1000)
        self.screen.fill(NOIR)
        perdreText = self.font.render("Vous avez perdu !", True, BLANC)
        perdreRect = perdreText.get_rect()
        perdreRect.center = ((TAILLE_FENETRE + 200)//2, TAILLE_FENETRE//2)
        self.screen.blit(perdreText, perdreRect)

        recommencerText = self.font.render("Recommencer", True, BLANC)
        recommencerRect = recommencerText.get_rect()
        recommencerRect.center = ((TAILLE_FENETRE + 200) // 2, TAILLE_FENETRE // 2 + 100)
        self.boutonRecommencer = Bouton(recommencerRect.left, recommencerRect.top, recommencerRect.width, recommencerRect.height, "Recommencer", BLANC, VERT, ROUGE)
        self.boutonRecommencer.dessiner(self.screen)

        self.multiplicateur = 1
        self.caseTrouvees = 0
        self.grille.casesRestantes = self.M
        self.casesRevelees = []
    
        self.perdu = True

        pygame.display.flip()
        
    def executer(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.perdu == False:
                        x = event.pos[0] // TAILLE_CASE
                        y = event.pos[1] // TAILLE_CASE

                        if event.pos[0] <= TAILLE_FENETRE:
                            pygame.draw.rect(self.screen, NOIR, (TAILLE_FENETRE, 0, 200, TAILLE_FENETRE))
                            if self.reveler(self.screen, x, y):
                                self.perdre()
                            pygame.display.flip()
                    elif self.boutonRecommencer and self.boutonRecommencer.estClique(event.pos):
                        self.screen.fill(NOIR)
                        self.grille = Grille(TAILLE_GRILLE, K)
                        self.player = Player()
                        self.multiplicateur = 1
                        self.grille.dessiner(self.screen)
                        self.afficherProchainMultiplicateur()
                        self.perdu = False

            if not self.perdu:
                self.boutonEncaisser.dessiner(self.screen)

            self.afficherArgent()
            self.afficherMise()
            pygame.display.update()

jeu = Jeu()
jeu.executer()