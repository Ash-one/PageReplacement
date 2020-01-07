class Page():
    def __init__(self, num: int):
        self.Number = num
        self.time = 0

    def clear(self):
        self.time = 0
        return self

class Disk():
    def __init__(self,pagelist:list):
        self.VirtualMemory = pagelist

    def addPage(self,page:Page):
        self.VirtualMemory.append(page)
        
    def removePage(self,num:int):
        for page in self.VirtualMemory:
            if page.Number == num :
                self.VirtualMemory.remove(page)
                return page

class Memory():
    def __init__(self, len: int, disk:Disk):
        self.MemoryLength = len
        self.MemoryBlocks = []
        self.ExtenalStorage = disk
        self.SwapCounter = 0

    def print(self):
        pages = [block.Number for block in self.MemoryBlocks]
        print('SwapTime:',self.SwapCounter,pages)

    def removePage(self,num:int):
        for page in self.MemoryBlocks:
            if page.Number == num :
                self.MemoryBlocks.remove(page)
                return page

    def isFree(self):
        if len(self.MemoryBlocks) < self.MemoryLength:
            return True
        else:
            return False

    def isPageIn(self,num:int):
        if len(self.MemoryBlocks) == 0:
            return False
        for block in self.MemoryBlocks:
            if isinstance(block, Page) == True and block.Number == num:
                return True
        return False

    def Tick(self):
        for block in self.MemoryBlocks:
            block.time += 1

    def AccessPage(self,num:int,mode='FIFO'):

        if mode == 'FIFO':
            if self.isPageIn(num):
                return
            else:
                self.SwapIn_FIFO(num)
                self.print()

        elif mode == 'LRU_Register':
            if self.isPageIn(num):
                return
            else:
                self.SwapIn_Register(num)
                self.print()

        elif mode == 'LRU_Stack':
            if self.isPageIn(num):
                page = self.removePage(num)
                self.MemoryBlocks.append(page)
                return
            else:
                self.SwapIn_LRU_Stack(num)
                self.print()
        else:
            print('mode错误')


    def SwapIn_FIFO(self, num:int):
        if self.isFree():
            newpage = self.ExtenalStorage.removePage(num)
            self.MemoryBlocks.append(newpage)

        else:
            self.SwapCounter += 1

            page = self.MemoryBlocks.pop(0)
            newpage = self.ExtenalStorage.removePage(num)
            self.MemoryBlocks.append(newpage)
            self.ExtenalStorage.addPage(page.clear())



    def SwapIn_Register(self, num:int):
        if self.isFree():
            newpage = self.ExtenalStorage.removePage(num)
            self.MemoryBlocks.append(newpage)

        else:
            self.SwapCounter += 1
            self.Register(num)

        self.Tick()


    def Register(self, num:int):
        register = -1
        for block in self.MemoryBlocks:
            if block.time > register:
                register = block.time
        for block in self.MemoryBlocks:
            if block.time == register:
                self.MemoryBlocks.remove(block)
                newpage = self.ExtenalStorage.removePage(num)
                self.MemoryBlocks.append(newpage)
                self.ExtenalStorage.addPage(block.clear())
                break

    def SwapIn_LRU_Stack(self,num:int):
        if self.isFree():
            newpage = self.ExtenalStorage.removePage(num)
            self.MemoryBlocks.append(newpage)

        else:
            self.SwapCounter += 1

            oldpage = self.MemoryBlocks.pop(0)
            newpage = self.ExtenalStorage.removePage(num)
            self.MemoryBlocks.append(newpage)
            self.ExtenalStorage.addPage(oldpage)







    
     
    
if __name__ =='__main__':
    pages = []
    for i in range(10):
        pages.append(Page(i))
    disk = Disk(pages)
    memory = Memory(len=3,disk=disk)

    operateList = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
    for i in operateList:
        memory.AccessPage(i,mode='LRU_Stack')
    memory.print()
