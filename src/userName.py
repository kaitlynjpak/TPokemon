import tkinter as tk   #used chatgpt and docs.python.org to help understand 
#tkinter syntax
from tkinter import simpledialog
import platform # i took this stuff from chat because i didnt know how 
#platform worked


def getName(app):      
    # Check if running on macOS
    if platform.system() == 'Darwin': #this is also taken from chat im not 
        #too sure why darwin is needed
        # On macOS, use a simpler approach to avoid UI thread issues
        root = tk.Tk()
        root.withdraw()
        # Use a try-except block to catch any exceptions (idk waht this is???)
        try:
            name = simpledialog.askstring("Name", "Enter your name:")
            root.destroy()
            return name
        except Exception as e:
            print(f"Error in getName: {e}")
            root.destroy()
            return "Player"  # Return a default name if there's an error
    else:
        # On other platforms, use the original approach
        root = tk.Tk()
        root.withdraw()
        name = simpledialog.askstring("Name", "Enter your name:")
        root.destroy()
        return name

