import pygame
from random import randint

TAILLE_GRILLE = 5
TAILLE_FENETRE = 600

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
        self.imageDos = pygame.image.load('ressources/images/dosCases.png')

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
                screen.blit(self.imageDos, (x*120, y*120))


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
        self.K = 5
        pygame.init()
        self.screen = pygame.display.set_mode((TAILLE_FENETRE + 200, TAILLE_FENETRE))
        pygame.display.set_caption("Démineur")
        self.grille = Grille(TAILLE_GRILLE, self.K)
        self.player = Player()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.initialiserGrille()
        self.multiplicateur = 1
        self.M = TAILLE_GRILLE * TAILLE_GRILLE
        self.caseTrouvees = 0
        
        self.sonEncaisser = pygame.mixer.Sound('ressources/sounds/encaisser.wav')
        self.sonTirer = pygame.mixer.Sound('ressources/sounds/tirer.wav')
        self.sonExplosion = pygame.mixer.Sound('ressources/sounds/explosion.wav')
        self.sonRetourner = pygame.mixer.Sound('ressources/sounds/retourner.wav')
        
        self.imageBombe = pygame.image.load('ressources/images/bombe.png')
        self.imagePiece = pygame.image.load('ressources/images/piece.png')
        
        self.sonExplosion.set_volume(0.5)
        self.sonRetourner.set_volume(0.7)
        
        self.perdu = False
        self.aEncaisser = False
        self.aCommencer = False
        self.boutonJouer = Bouton((TAILLE_FENETRE) // 2, TAILLE_FENETRE // 2 + 100, 150, 50, "Jouer", BLANC, ROUGE, VERT)
        self.boutonEncaisser = Bouton(TAILLE_FENETRE+25, TAILLE_FENETRE-100, 150, 50, "Encaisser", BLANC, ROUGE, VERT)
        
        self.boutonAugmenterMise = Bouton(TAILLE_FENETRE + 60, 120, 25, 25, "+", BLANC, ROUGE, VERT)
        self.boutonDiminuerMise = Bouton(TAILLE_FENETRE + 110, 120, 25, 25, "-", BLANC, ROUGE, VERT)
        self.boutonDoublerMise = Bouton(TAILLE_FENETRE + 60, 170, 25, 25, "x", BLANC, ROUGE, VERT)
        self.boutonDiviserMise = Bouton(TAILLE_FENETRE + 110, 170, 25, 25, "/", BLANC, ROUGE, VERT)
        
        self.boutonAugmenterNombreDeMines = Bouton(35, 70, 25, 25, "+", BLANC, ROUGE, VERT)
        self.boutonDiminuerNombreDeMines = Bouton(85, 70, 25, 25, "-", BLANC, ROUGE, VERT)
        
        self.gain = self.player.mise
        
        self.casesRevelees = []
        self.calculerProchainMultiplicateur()
        self.afficherProchainMultiplicateur()        

    def reveler(self, screen, x, y):
        if (x, y) in self.casesRevelees:
            self.afficherProchainMultiplicateur()
            return False
        else:
            self.casesRevelees.append((x, y))

        if self.grille.grille[x][y] == 0:
            self.sonRetourner.play()
            image = self.imagePiece
            self.grille.casesRestantes -= 1
        else:
            image = self.imageBombe
            self.sonExplosion.play()
            screen.blit(image, (x * 120, y * 120))
            pygame.display.update()
            return True
        screen.blit(image, (x * 120, y * 120))
        pygame.display.update()
        self.calculerProchainMultiplicateur()
        self.afficherProchainMultiplicateur()
        return False
    
    def afficherArgent(self):
        argentText = self.font.render(f"{self.player.tune}", True, BLANC)
        argentRect = argentText.get_rect()
        argentRect.topright = (TAILLE_FENETRE + 150, 20)
        self.screen.blit(argentText, argentRect)
    
    def afficherMise(self):
        miseText = self.font.render(f"Mise : {self.player.mise}", True, BLANC)
        miseRect = miseText.get_rect()
        miseRect.topright = (TAILLE_FENETRE + 150, 70)
        self.screen.blit(miseText, miseRect)       
    
    def afficherNombreDeMines(self):
        nombreDeMinesText = self.font.render(f"Mines : {self.K}", True, BLANC)
        nombreDeMinesRect = nombreDeMinesText.get_rect()
        nombreDeMinesRect.topright = (120, 20)
        self.screen.blit(nombreDeMinesText, nombreDeMinesRect)
    
    def afficherProchainMultiplicateur(self):
        multiplicateurText = self.font.render(f"Next : x{self.multiplicateur}", True, BLANC)
        multiplicateurRect = multiplicateurText.get_rect()
        multiplicateurRect.topright = (TAILLE_FENETRE + 150, 120)
        self.screen.blit(multiplicateurText, multiplicateurRect)       
    
    def afficherGain(self):
        gainText = self.font.render(f"{self.gain}", True, BLANC)
        gainRect = gainText.get_rect()
        gainRect.center = (TAILLE_FENETRE + 100, TAILLE_FENETRE - 120)
        self.screen.blit(gainText, gainRect)
    
    def calculerProchainMultiplicateur(self):
        self.gain = round((self.player.mise * self.multiplicateur) * 0.99, 2)
        self.multiplicateur = round(self.multiplicateur * ((self.M - self.caseTrouvees) / self.grille.casesRestantes), 2)
        if self.multiplicateur > 100:
            round(self.multiplicateur)
        self.caseTrouvees += 1
    
    def initialiserGrille(self):
        self.screen.fill(NOIR)
        self.grille.dessiner(self.screen)
        pygame.display.flip()
    
    def perdre(self):
        pygame.time.delay(250)
        
        if self.player.mise > self.player.tune:
            self.player.mise = self.player.tune

        self.multiplicateur = 1
        self.caseTrouvees = 0
        self.grille.casesRestantes = self.M
        self.casesRevelees = []
    
        self.perdu = True

        pygame.display.flip()     
    
    def encaisser(self):
        self.player.tune = round(self.gain + self.player.tune, 2)
        
        self.multiplicateur = 1
        self.caseTrouvees = 0
        self.grille.casesRestantes = self.M
        self.casesRevelees = []
    
        self.aEncaisser = True

        pygame.display.flip()
        
    def executer(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.perdu == False and self.aEncaisser == False and self.aCommencer == True:
                        x = event.pos[0] // TAILLE_CASE
                        y = event.pos[1] // TAILLE_CASE

                        if event.pos[0] <= TAILLE_FENETRE:
                            pygame.draw.rect(self.screen, NOIR, (TAILLE_FENETRE, 0, 200, TAILLE_FENETRE))
                            if self.reveler(self.screen, x, y):
                                self.perdre()
                            pygame.display.flip()
                    else :
                        if self.boutonJouer.estClique(event.pos):
                            self.aCommencer = True
                            self.player.tune = round(self.player.tune - self.player.mise, 2)
                            self.screen.fill(NOIR)
                            self.grille = Grille(TAILLE_GRILLE, self.K)
                            self.multiplicateur = 1
                            self.grille.dessiner(self.screen)
                            self.calculerProchainMultiplicateur()
                            self.afficherGain()
                            self.afficherProchainMultiplicateur()
                            self.perdu = False
                            self.aEncaisser = False
                        elif self.boutonAugmenterMise.estClique(event.pos):
                            self.sonTirer.play()
                            if self.player.tune >= self.player.mise + 10:
                                self.player.mise += 10
                            else:
                                self.player.mise = self.player.tune
                        elif self.boutonDiminuerMise.estClique(event.pos):
                            self.sonTirer.play()
                            if self.player.mise >= 10:
                                self.player.mise -= 10
                            else:
                                self.player.mise = 0
                        elif self.boutonDiviserMise.estClique(event.pos):
                            self.sonTirer.play()
                            self.player.mise = round(self.player.mise/2)
                            if self.player.mise < 10:
                                if self.player.tune < 10:
                                    self.player.mise = self.player.tune
                                else:
                                    self.player.mise = 10
                        elif self.boutonDoublerMise.estClique(event.pos):
                            self.sonTirer.play()
                            if self.player.tune >= self.player.mise*2:
                                self.player.mise *= 2
                            else:
                                self.player.mise = self.player.tune
                        elif self.boutonAugmenterNombreDeMines.estClique(event.pos):
                            self.sonTirer.play()
                            if self.K < TAILLE_GRILLE*TAILLE_GRILLE - 1:
                                self.K += 1
                        elif self.boutonDiminuerNombreDeMines.estClique(event.pos):
                            self.sonTirer.play()
                            if self.K > 1:
                                self.K -= 1
                        
                    if self.boutonEncaisser.estClique(event.pos):
                        self.sonEncaisser.play()
                        self.encaisser()

            if self.perdu or self.aEncaisser or not self.aCommencer:
                self.screen.fill(NOIR)
                self.boutonJouer.dessiner(self.screen)
                self.boutonAugmenterMise.dessiner(self.screen)
                self.boutonDiminuerMise.dessiner(self.screen)
                self.boutonDoublerMise.dessiner(self.screen)
                self.boutonDiviserMise.dessiner(self.screen)
                self.boutonAugmenterNombreDeMines.dessiner(self.screen)
                self.boutonDiminuerNombreDeMines.dessiner(self.screen)
                self.afficherMise()
                self.afficherArgent()
                self.afficherNombreDeMines()
                if self.perdu:
                    perdreText = self.font.render("Vous avez perdu !", True, BLANC)
                    perdreRect = perdreText.get_rect()
                    perdreRect.center = ((TAILLE_FENETRE + 200)//2, TAILLE_FENETRE//2)
                    self.screen.blit(perdreText, perdreRect)
                elif self.aEncaisser:
                    beneficeText = self.font.render(f"+{self.gain}", True, VERT)
                    beneficeRect = beneficeText.get_rect()
                    beneficeRect.center = ((TAILLE_FENETRE + 200) // 2, TAILLE_FENETRE //2)
                    self.screen.blit(beneficeText, beneficeRect)
            else:
                self.boutonEncaisser.dessiner(self.screen)
                self.afficherProchainMultiplicateur()
                self.afficherGain()

            self.afficherArgent() 
            
            pygame.display.update()

jeu = Jeu()
jeu.executer()