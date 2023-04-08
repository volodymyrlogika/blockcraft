from panda3d.core import NodePath

class Hero:
    """ Управління гравцем """
    def __init__(self, pos, land):
        self.color_num = 0
        self.height = 2 #висота камери над землею
        self.start_pos = pos #стартова позиція
        base.disableMouse() #вимикаємо стандартне керування камерою
        base.camera.setPos(self.start_pos) 
        base.camera.setH(180)
        base.camera.reparentTo(render)
        base.camLens.setNear(0.2)
        base.camLens.setFov(90)
        
        self.key_step = 0.15 # крок клавіші
        self.mouse_step = 0.2 #крок мишки

        self.x_center = base.win.getXSize()//2
        self.y_center = base.win.getYSize()//2

        base.win.movePointer(0, self.x_center, self.y_center)

        self.heading = 180 #напрямок вліво-вправо
        self.pitch = 0 # нахил вверх-вниз
        self.land = land

        self.ground = True # стоїмо на землі
        self.can_move = True  #можемо рухатися
        self.jump_power = 0.4
        self.fall_speed = 0
        self.acceleration = 0.025

        self.point = NodePath("point") #точка перед камерою
        self.point.reparentTo(render)

        #створюємо словник з станом кнопок
        self.keys = {}
        for key in ["mouse3", "mouse1", "w", "a", "s", "d", "space"]:
            self.keys[key] = 0
        #прив'язуємо функції до натискання кнопок
        base.accept("mouse1", self.build)
        base.accept("mouse2", self.destroy)
        base.accept("wheel_up", self.changeColor, ['wheel_up'])
        base.accept("wheel_down", self.changeColor, ['wheel_down'])
        
        base.accept("f", self.destroy)
        base.accept("mouse3", self.press_right_btn)
        base.accept("mouse3" + "-up", self.unpress_right_btn)
        
        base.accept("w", self.set_key, ["w", 1])
        base.accept("w"+"-up", self.set_key, ["w", 0])
        base.accept("s", self.set_key, ["s", 1])
        base.accept("s" + "-up", self.set_key, ["s", 0])
        base.accept("a", self.set_key, ["a", 1])
        base.accept("a"+"-up", self.set_key, ["a", 0])
        base.accept("d", self.set_key, ["d", 1])
        base.accept("d" + "-up", self.set_key, ["d", 0])
        base.accept("space", self.set_key, ["space", 1])
        base.accept("space" + "-up", self.set_key, ["space", 0])
        
        taskMgr.doMethodLater(0.02, self.movement, 'movement-task')
        #додаємо звуки
        self.buildSound = base.loader.loadSfx("wood03.ogg")
        self.destroySound = base.loader.loadSfx("gravel.ogg")

    
    def press_right_btn(self):
        self.keys['mouse3'] = 1
        base.win.movePointer(0, self.x_center, self.y_center)

    def unpress_right_btn(self):
        self.keys['mouse3'] = 0 
    
    def set_key(self, key_name, value):
        """задаємо стан кнопки 1 - натиснуто, 0- ні """
        self.keys[key_name] = value

    def movement(self, task):
        """функція контролю руху камери"""
        if self.keys['mouse3']:
            pointer = base.win.getPointer(0)
            new_x, new_y = pointer.getX(), pointer.getY()
            self.x_center = base.win.getXSize()//2
            self.y_center = base.win.getYSize()//2
            if base.win.movePointer(0, self.x_center, self.y_center):
                self.heading = self.heading - (new_x - self.x_center) *  self.mouse_step
                self.pitch = self.pitch - (new_y - self.y_center) * self.mouse_step
                if self.pitch < -30:
                    self.pitch = -30
            base.camera.setHpr(self.heading, self.pitch, 0)
        #перевірка чи є щось в точці перед камерою
        self.point.setPos(base.camera, (0, 1, -1))
        pos1 = self.point.getPos()
        self.point.setPos(base.camera, (0, 1, 0))
        pos2 = self.point.getPos() 
        if self.land.isEmpty(pos1) and self.land.isEmpty(pos2): # якщо в точці пусто
            self.can_move = True #можна рухатися
        else:
            self.can_move = False
        #стрибки
        pos = base.camera.getPos()
        under_pos = (pos[0], pos[1], pos[2] - self.height)
        if self.land.isEmpty(under_pos): # якщо під нами пусто
            self.ground = False
        else:
            self.ground = True
            self.fall_speed = 0
        #перевірка чи над нами пусто
        pos = base.camera.getPos()
        over_pos = (pos[0], pos[1], pos[2] + 2)
        if self.keys['space'] and self.ground and self.land.isEmpty(over_pos):
            self.fall_speed = -self.jump_power
            self.ground = False
            
        if not self.ground: #якщо падаємо
            pitch = base.camera.getP()
            base.camera.setP(0) # при падінні - нахил камери скидаємо до 0
            self.fall_speed += self.acceleration 
            move_x = (self.keys["d"]-self.keys["a"]) * self.key_step/2
            move_y = (self.keys["w"]-self.keys["s"]) * self.key_step/2
            base.camera.setPos(base.camera, move_x, move_y, -self.fall_speed)
            base.camera.setP(pitch)

            if base.camera.getZ() < -30:
                base.camera.setPos(self.start_pos)
                base.camera.setZ(10)

        if self.can_move and self.ground:
            pitch = base.camera.getP()
            base.camera.setP(0) # при русі - нахил камери скидаємо до 0
            move_x = (self.keys["d"]-self.keys["a"]) * self.key_step
            move_y = (self.keys["w"]-self.keys["s"]) * self.key_step
            base.camera.setPos(base.camera, (move_x, move_y, 0))
            base.camera.setP(pitch) #повертаємо нахил камери (щоб не рухатися вниз і вгору)

        return task.again

    def build(self):
        """будівництво блоку в точці перед камерою"""
        self.point.setPos(base.camera, (0, 3, 0))
        pos = self.point.getPos() #координати точки перед нами
        new_pos = (round(pos[0]), round(pos[1]), round(pos[2]))
        if self.land.isEmpty(new_pos):
            self.land.addBlock(new_pos)
            self.buildSound.play()

    def destroy(self):
        """видалення блоку в точці перед камерою"""
        self.point.setPos(base.camera, (0, 3, 0))
        pos = self.point.getPos() #координати точки перед нами
        new_pos = (round(pos[0]), round(pos[1]), round(pos[2]))
        blocks = self.land.findBlocks(new_pos) #знаходимо блок в точці
        for block in blocks:
            block.removeNode() #видаляємо блок з рендеру
            self.destroySound.play()

    def changeColor(self, wheel):
        """зміна кольору блоку в точці перед камерою"""
        if wheel == "wheel_up":
            self.color_num += 1
            if self.color_num > len(self.land.colors)-1:
                self.color_num = 0
        else:
            self.color_num -= 1
            if self.color_num < 0:
                self.color_num = len(self.land.colors)-1

        self.point.setPos(base.camera, (0, 3, 0))
        pos = self.point.getPos() #координати точки перед нами
        new_pos = (round(pos[0]), round(pos[1]), round(pos[2]))
        blocks = self.land.findBlocks(new_pos) #знаходимо блок в точці
        for block in blocks:
            block.setColor(self.land.getColor(self.color_num))
            block.setTag("color", str(self.color_num))
