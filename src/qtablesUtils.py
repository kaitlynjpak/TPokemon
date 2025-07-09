import os

#CHATGPT
baseDirectory = os.path.dirname(__file__)
qtablesDirectory = os.path.join(baseDirectory, 'qtables')

def qtablePath(filename):
    return os.path.join(qtablesDirectory, filename)