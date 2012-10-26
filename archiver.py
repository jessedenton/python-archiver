#!/usr/bin/env python
'''
@author: Jesse Denton
@version: 1.02
@date: 24-10-2012

USE:
import archiver
archiver.MyArchiver(r"C:\Foo\Bar\myFile.txt").simpleArchive()

OR:
drag and drop files onto archiver.py

TODO:
1. Add logging function that creates text files in the archive directory for a history of archives
2. Add zipfile and / or tarfile to make archives smaller


'''
import os
import sys
import shutil

DEBUG = False

class PathManager(object):
    '''
    File management class. 
    acquires information from a full file path
    
    eg filePath   = 'C:\Users\Jesse\Desktop\fooBar.py'
       fileDir    = 'C:\Users\Jesse\Desktop'
       fileNameEx = 'fooBar.py'
       fileName   = 'fooBar'
       fileExt    = '.py'
    '''
    def __init__(self, filePath):
        self._filePath = filePath
        self._fileDir = os.path.dirname(self.filePath)
        self._fileNameEx = os.path.basename(self.filePath)
        self._fileName = os.path.splitext(self.fileNameEx)[0]
        self._fileExtension = os.path.splitext(self.fileNameEx)[1]
        
    def _updatePaths(self, newPath):
        '''
        Run when filePath is changed 
        from the setter decorator
        '''
        self._filePath = newPath
        self._fileDir = os.path.dirname(newPath)
        self._fileNameEx = os.path.basename(newPath)
        self._fileName = os.path.splitext(self._fileNameEx)[0]
        self._fileExtension = os.path.splitext(self._fileNameEx)[1]
        
    @property
    def filePath(self):
        return self._filePath
    @filePath.setter
    def filePath(self, path):
        self._updatePaths(path)
        
    @property
    def fileDir(self):
        return self._fileDir
    @property
    def fileNameEx(self):
        return self._fileNameEx
    @property
    def fileName(self):
        return self._fileName
    @property
    def fileExtension(self):
        return self._fileExtension
        
class MyArchiver(PathManager):
    '''
    Archiver class.
    '''    
    _user = os.getenv('USERNAME') or os.getenv('USER')
    def __init__(self, filePath, limit = 10 ):
        super(MyArchiver, self).__init__(filePath)
        self.limit = limit

    def getArchivePath(self):
        '''returns path name for the archive directory'''
        return os.path.join(self.fileDir, "Archive", self.fileName)

    def getArchivedFiles(self):
        '''returns a list of previous archived files'''
        #TODO: add type / extension check to make sure no weird files are in archive folder
        #make check that the archive path exists
        if not os.path.exists(self.getArchivePath()):
            raise IOError, "Archive path doesn't exist %s" % self.getArchivePath()
        
        return  sorted(os.listdir(self.getArchivePath()))
    
    def isArchived(self):
        '''checker to see if a file has been archived previously'''
        return os.path.exists(self.getArchivePath())
    
    def simpleArchive(self):
        '''main archiving function'''
        #check to see if the file is a correct file path
        if not os.path.isfile(self.filePath):
            raise ValueError, "%s is not a valid file path" % self.filePath
        
        #start doing archiving stuff
        #check if the file has archive directories 
        archivePath = self.getArchivePath()
        if not self.isArchived():
            print "Making directory: %s" % archivePath
            os.makedirs(archivePath)

        #find archive version 
        archiveVersion = 001
        archiveFiles = self.getArchivedFiles()
        if len(archiveFiles):
            lastFile = archiveFiles[-1]
            archiveVersion = int(lastFile.split('.')[1]) + 1
        
        #begin copy of file NB just realised the class username should be in here
        newArchiveFile = os.path.join(archivePath, '%s.%03d%s' % (self.fileName, archiveVersion, self.fileExtension))
        try:
            shutil.copyfile(self.filePath, newArchiveFile)
        except:
            print "It failed"
    
    def zipArchive(self):
        return 'not implemented'
    
    @classmethod
    def getUser(cls):
        return cls._user
    @classmethod
    def changeUser(cls, username):
        cls._user = username
        

if __name__ == "__main__":
    
    for path in sys.argv[1:]:
        print "archiving:", path
        MyArchiver(path).simpleArchive()
        
    raw_input("Press any key to exit.")
    sys.exit()
