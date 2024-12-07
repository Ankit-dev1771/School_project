import time
import curses

font = "L O A D I N G . . . "

while True:
    # Print the font string one character at a time
    for i in font:
        time.sleep(0.05)
        print(i, end="", flush=True)
        
    # Remove text one by one (overwrite with spaces)
    for i in range(len(font)):
        time.sleep(0.05)
        print(f"\r{' ' * (i)}", end="", flush=True)

    # Resets cursor to the starting 
    print('\r', end='')
    stdscr.clear()