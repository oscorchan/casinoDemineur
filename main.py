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

    def reveler(self, screen, x, y):
        if self.grille[x][y] == 0:
            couleur = VERT
            self.casesRestantes -= 1
        else:
            couleur = ROUGE
        pygame.draw.rect(screen, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.rect(screen, NOIR, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)

class Player:
    def __init__(self) -> None:
        self.tune = 500
        self.mise = 50

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

    def afficherMultiplicateur(self):
        self.multiplicateur = round(self.multiplicateur * (self.grille.K * self.grille.K / self.grille.casesRestantes), 2)
        multiplicateurText = self.font.render(f"x{self.multiplicateur}", True, BLANC)
        multiplicateurRect = multiplicateurText.get_rect()
        multiplicateurRect.topright = (TAILLE_FENETRE + 150, 120)
        self.screen.blit(multiplicateurText, multiplicateurRect)
        print(self.multiplicateur)
        print(self.grille.casesRestantes)


    def initialiserGrille(self):
        self.screen.fill(NOIR)
        self.grille.dessiner(self.screen)
        pygame.display.flip()

    def executer(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0] // TAILLE_CASE
                    y = event.pos[1] // TAILLE_CASE

                    if event.pos[0] <= TAILLE_FENETRE:
                        pygame.draw.rect(self.screen, NOIR, (TAILLE_FENETRE, 0, 200, TAILLE_FENETRE))
                        self.afficherMultiplicateur()
                        self.grille.reveler(self.screen, x, y)
                        pygame.display.flip()

            self.afficherArgent()
            self.afficherMise()
            pygame.display.update()

jeu = Jeu()
jeu.executer()



