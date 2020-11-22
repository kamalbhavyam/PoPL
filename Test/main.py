from game import Game
import threading
import random
import time

def eventmaker(gameObject):
    print("Function Called")
    if gameObject.tilesum!=8:
        if gameObject.tilesum>8:
            # gameObject.tilesum
            print("OVERSHOT!")
            gameObject.gui.event_generate("i")
            gameObject.gui.event_generate("z")
            gameObject.gui.after(1000,eventmaker,gameObject)
        # time.sleep(1)
        else:
            gameObject.gui.event_generate("i")
            ind=random.choices([1,2,3,4])[0]
            print(ind)
            if ind==1:
                gameObject.gui.event_generate("a")
            elif ind==2:
                gameObject.gui.event_generate("d")
            elif ind==3:
                gameObject.gui.event_generate("w")
            elif ind==4:
                gameObject.gui.event_generate("s")
            gameObject.gui.after(1000,eventmaker,gameObject)
    else:
        gameObject.gui.event_generate("i")

    # gameObject.gui.event_generate("i")

def main():
    gameObject=Game()
    gameObject.gui.after(1000,eventmaker,gameObject)
    gameObject.gui.mainloop()

if __name__ == "__main__":
    main()