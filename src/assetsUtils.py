import os

#CHATGPT
baseDirectory = os.path.dirname(__file__)
assetsDirectory = os.path.join(baseDirectory, 'assets')

def assetPath(filename):
    return os.path.join(assetsDirectory, filename)
