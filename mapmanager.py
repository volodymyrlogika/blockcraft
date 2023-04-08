import pickle

class MapManager:
    '''Управління картою'''
    def __init__(self):
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.color = (0, 0.5, 0.13, 1)
        self.colors = [
            (0.5, 0.3, 0.0, 1),
            (0.2, 0.2, 0.3, 1),
            (0.5, 0.5, 0.2, 1),
            (0.0, 0.6, 0.0, 1),
        ]
        self.newLand()

    def getColor(self, num):
        """повертає колір блоку за його номером"""
        if num <=3:
            return self.colors[num]
        else:
            return self.colors[-1]

    def addBlock(self, pos, col = None):
        '''метод для створення блоків'''
        block = loader.loadModel(self.model) #завантажуємо модель
        block.setTexture(loader.loadTexture(self.texture)) #задаємо текстуру
        block.setPos(pos)  #задаємо позицію куба
        if not col:
            col = pos[2]
        self.color = self.getColor(int(col))
        block.setColor(self.color)
        block.reparentTo(self.land)
        block.setTag("pos", str(pos))
        block.setTag("color", str(col))
        

    def newLand(self):
        '''створюємо вузол де будуть всі блоки'''
        self.land = render.attachNewNode('Land')

    def clearMap(self):
        self.land.removeNode() #видаляємо стару локацію
        self.newLand() #створюємо нову локацію

    def loadLand(self, filename):
        self.clearMap()
        '''завантаження карти з текстового файлу'''
        with open(filename, 'r') as file:
            lines = file.readlines()
            y = 0
            for line in lines:
                x = 0
                line_list = line.strip().split(' ')
                nums = list(map(int, line_list))
                for num in nums:
                    for z in range(0, num + 1):
                        self.addBlock((y, x, z))
                    x += 1
                y += 1
            return x, y  
                    
    def findBlocks(self, pos):
        """функція повертає всі блоки в позиції pos"""
        return self.land.findAllMatches("=pos="+str(pos))

    def isEmpty(self, pos):
        """перевіряє чи є блок в точці pos"""
        blocks = self.findBlocks((round(pos[0]), round(pos[1]), round(pos[2])))
        if blocks:
            return False    
        else:
            return True

    def save(self):
        """збереження карти та позиції гравця в бінарний файл"""
        blocks = self.land.getChildren()
        with open("mysave.dat", "wb") as file:
            x, y, z = base.camera.getPos()
            pickle.dump((x, y, z), file)
            pickle.dump(len(blocks), file)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file) #записали координати блоку
                color = block.getTag("color")
                pickle.dump(color, file)


    def load(self):
        """зчитування карти та позиції гравця в бінарний файл"""
        self.clearMap()
        with open("mysave.dat", "rb") as file:
            x, y, z = pickle.load(file) #початкова позиція
            k_blocks = pickle.load(file)
            for i in range(k_blocks):
                pos = pickle.load(file)
                color = pickle.load(file)
                self.addBlock(pos, color)
        return x, y, z
            

