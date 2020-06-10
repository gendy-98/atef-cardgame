import pygame
from pygame.locals import *

from time import sleep

from PodSixNet.Connection import connection, ConnectionListener
    
class Game(ConnectionListener):
    def __init__(self,host,port):
        self.allowUpdate = True
        self.Connect((host, port))
        pygame.init()
        width,height = 1000,700
        pygame.display.set_caption("Virtual Smile")
        self.screen = pygame.display.set_mode((width,height))
        self.clock=pygame.time.Clock()
        self.background = pygame.image.load("ground.jpg")
        self.screen.blit(self.background,(0,0))
        pygame.display.flip()
        name=self.name_pass()
        connection.Send({"action": "nickname", "nickname": name})
    def update(self):
        connection.Pump()
        self.Pump()
        self.clock.tick(60)
        self.screen.fill(0)
        self.screen.blit(self.background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()
    def name_pass(self):
        name = ''
        done = False
        font = pygame.font.Font(None, 50)
        while not done:
            self.screen.blit(self.background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        name += event.unicode
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == K_RETURN:
                        done=True
            block = font.render("Nickname: "+name, True, (0, 0, 0))
            rect = block.get_rect()
            rect.center = self.screen.get_rect().center
            self.screen.blit(block, rect)
            pygame.display.flip()
        return name
    def Network_players(self, data):
        self.allowUpdate = False
        self.Players = data
##        font = pygame.font.Font(None, 50)
##        block = font.render("Players: ".join([p for p in data['players']]), True, (0, 0, 0))
##        rect = block.get_rect()
##        rect.center = self.screen.get_rect().center
##        self.screen.blit(block, rect)
        if len(data['players']) == 3:
            self.allowUpdate = True

    def updatePlayers(self):
        connection.Pump()
        self.Pump()
        self.clock.tick(60)
        self.screen.fill(0)
        self.screen.blit(self.background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        font = pygame.font.Font(None, 50)
        block2 = font.render("Players: "+ ";".join([p for p in self.Players['players']]), True, (0, 0, 0))
        rect = block2.get_rect()
        rect.center = self.screen.get_rect().center
        self.screen.blit(block2, rect)
        pygame.display.flip()
    
    def Network_message(self, data):
        print(data['who'] + ": " + data['message'])
    
    # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()
#cg = Game('localhost', 31425)
cg=Game("localhost",31425)
while 1:
    if cg.allowUpdate:
        cg.update()
    else:
        cg.updatePlayers()
