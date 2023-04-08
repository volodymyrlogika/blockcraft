from direct.gui.DirectGui import *
from panda3d.core import *

class Menu:
    def __init__(self, **btns):

        self.font = loader.loadFont('Minecrafter.Alt.ttf')
        self.btn_image = loader.loadTexture("btn.png")
        self.bg_image = loader.loadTexture("menu_bg.jpg")

        self.menuScreen = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    image = self.bg_image,
                                    parent = render2d)
        #список пунктів меню
        self.titleMenu = DirectFrame(frameColor=(0, 0, 0, 0))
        self.title = DirectLabel(text = "BlockCraft",
                                parent =  self.titleMenu,
                                scale = 0.2,
                                pos = (0, 0, 0.6),
                                text_font = self.font,
                                text_fg = (1, 1, 1, 1),
                                relief = None)
        btn = DirectButton(text = "EXIT",
                        command = base.userExit,
                        parent =  self.titleMenu,
                        scale = 0.1,
                        pos = (0, 0, -0.5),
                        text_font = self.font,
                        text_fg = (1, 1, 1, 1),
                        frameTexture = self.btn_image,
                        frameSize = (-5, 5, -1, 1),
                        text_scale = 0.75,
                        text_pos = (0, -0.2),
                        relief = DGG.FLAT,
                        pressEffect = 1
                        )
        btn2 = DirectButton(text = "SAVE",
                        command = btns['save'],
                        parent =  self.titleMenu,
                        scale = 0.1,
                        pos = (0, 0, 0.25),
                        text_font = self.font,
                        text_fg = (1, 1, 1, 1),
                        frameTexture = self.btn_image,
                        frameSize = (-5, 5, -1, 1),
                        text_scale = 0.75,
                        text_pos = (0, -0.2),
                        relief = DGG.FLAT,
                        pressEffect = 1
                        )

        btn2 = DirectButton(text = "new game",
                        command = btns['new'],
                        parent =  self.titleMenu,
                        scale = 0.1,
                        pos = (0, 0, 0),
                        text_font = self.font,
                        text_fg = (1, 1, 1, 1),
                        frameTexture = self.btn_image,
                        frameSize = (-5, 5, -1, 1),
                        text_scale = 0.75,
                        text_pos = (0, -0.2),
                        relief = DGG.FLAT,
                        pressEffect = 1
                        )
        btn2 = DirectButton(text = "load game",
                        command = btns['load'],
                        parent =  self.titleMenu,
                        scale = 0.1,
                        pos = (0, 0, -0.25),
                        text_font = self.font,
                        text_fg = (1, 1, 1, 1),
                        frameTexture = self.btn_image,
                        frameSize = (-5, 5, -1, 1),
                        text_scale = 0.75,
                        text_pos = (0, -0.2),
                        relief = DGG.FLAT,
                        pressEffect = 1
                        )
                                
    def show(self):
        self.menuScreen.show()
        self.titleMenu.show()

    def hide(self):
        self.menuScreen.hide()
        self.titleMenu.hide()

        