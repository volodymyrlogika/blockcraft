from direct.showbase.ShowBase import ShowBase
from mapmanager import MapManager
from hero import Hero
from menu import Menu

class MyMinecraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.sky = loader.loadModel('sky/skybox')
        self.sky.reparentTo(render)
        self.sky.setScale(100)
        self.land = MapManager()
        self.menu = Menu(save = self.saveGame,
                        new = self.newGame,
                        load = self.loadGame)
       
        base.accept("escape", self.showMenu) # при натисканні ESCAPE - показуємо меню
        self.start  = False

    def showMenu(self):
        """"Показати або сховати меню"""
        if self.menu.menuScreen.isHidden():
            self.menu.show()
        elif self.start:
            self.menu.hide()

    def saveGame(self):
        if self.start  == True: #якщо гра почалася 
            self.land.save() #зберігаємо гру
            self.menu.hide()

    def newGame(self):  #нова гра
        x, y = self.land.loadLand("land.txt")
        x, y, z = 21,10,2
        self.hero = Hero((x,y,z), self.land)
        self.menu.hide()
        self.start  = True
    
    def loadGame(self): # заванатаження збереженої гри
        try:
            x, y, z = self.land.load()
        except (FileNotFoundError, IOError):
            x, y = self.land.loadLand("land.txt")
            x, y, z = 21,10,2
        self.hero = Hero((x,y,z), self.land)
        self.menu.hide()
        self.start  = True
    
    def endGame(self): 
        self.land.save()
        base.userExit() #виходимо з гри


game = MyMinecraft()
game.run()