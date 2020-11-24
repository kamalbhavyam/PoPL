from game import Game
from states import State,History
import random
import time

agenthistory=History()
visited=None

def childlist(gameObject):
    ls=[]
    gameObject.checknext()
    if not gameObject.left is None:
        ls.append(gameObject.left)
    if not gameObject.right is None:
        ls.append(gameObject.right)
    if not gameObject.up is None:
        ls.append(gameObject.up)
    if not gameObject.down is None:
        ls.append(gameObject.down)
    return ls

def eventmaker(visited,gameObject):
    if visited is None:
        visited = []

    visited.append(gameObject)
    agenthistory.push(gameObject,None)

    if gameObject.tilesum>8:
        return -1
    if gameObject.tilesum==8:
        print("queue:")
        for x in agenthistory.history:
            print(x[0],x[0].tilesum)
        return 1

    for elem in childlist(gameObject):
        if elem not in visited:
            if eventmaker(visited,elem)==1:
                return 1
    # visited.append(gameObject)
    # queue.append(gameObject)

    # while queue:
    #     s=queue.pop(0)
    #     print(s)

    #     if s.losingstate==True:


    #     if s.tilesum==8:
    #         print("winner element",s)
    #         break
            
    #     if s.tilesum>8:
    #         continue

    #     for elem in childlist(s):
    #         # if elem not in visited:
    #             visited.append(elem)
    #             queue.append(elem)
        
    # print("Function Called")
    # if gameObject.tilesum!=28:
    #     if gameObject.tilesum>24:
    #         # gameObject.tilesum
    #         print("OVERSHOT!")
    #         # gameObject.gui.event_generate("i")
    #         gameObject.gui.event_generate("z")
    #         gameObject.gui.after(50,eventmaker,gameObject)
    #     # time.sleep(1)
    #     else:
    #         available_indices=[1,2,3,4]
    #         # gameObject.gui.event_generate("i")
    #         ind=random.choices(available_indices)[0]
    #         print(ind)
    #         if ind==1:
    #             gameObject.gui.event_generate("a")
    #             available_indices.remove(1)
    #         elif ind==2:
    #             gameObject.gui.event_generate("d")
    #             available_indices.remove(2)
    #         elif ind==3:
    #             gameObject.gui.event_generate("w")
    #             available_indices.remove(3)
    #         elif ind==4:
    #             gameObject.gui.event_generate("s")
    #             available_indices.remove(4)
    #         gameObject.gui.after(50,eventmaker,gameObject)
    # else:
    #     gameObject.gui.event_generate("i")

    # gameObject.gui.event_generate("i")

def main():
    gameObject=Game()
    gameObject.gui.after(200,eventmaker,visited,State(gameObject.matrix,gameObject.score,gameObject.tilesum))
    gameObject.gui.mainloop()

if __name__ == "__main__":
    main()