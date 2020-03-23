import sys
import os

class FileHelper(object):

    Path = ""
    init = False

    def initPaths():
         if getattr(sys, 'frozen', False):
            FileHelper.Path = sys._MEIPASS              #This is for when the program is frozen
         else:
            FileHelper.Path = ""#os.path.dirname(__file__) 

        
    @staticmethod
    def getPath(path):
            if not FileHelper.init: 
                FileHelper.initPaths()
                FileHelper.init = True
            
            print(FileHelper.Path)
            return os.path.join(FileHelper.Path, path)



