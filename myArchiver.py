#!/usr/bin/env python
'''
##############################################################
 
    myArchiver v1.01
    ---------------------------
    @author Jesse Denton
    @email jesse.denton@hotmail.com
    @date 17-10-2012
    ------------------------------------------------------------------------------------------------------------
    simple archiver written as an example for Luma Stuios

    *archives selected file under the given file directory with the User and file as sub catagories
    *added command line arguments (-f , --file) to specify they file path and (-l, --linit) to specify the limit 
    of archives to keep.

    NB use of @property and setter as an example only. It added 7 additional lines that didnt need
    to be there. It was only used in line 82 (setter), could have used self.limit instead.
##############################################################

'''
import os,re,shutil, sys

class myArchiver(object):
    def __init__(self, path = None, limit = 10):
    
        self.filePath = path
        self.limit = limit
        self.__name = None
        self.__extension = None
        self.__archivePath = None
        
    def makeArchiveDir(self):
        '''
        creates archive directory files
        '''
        if not os.path.exists(self.__archivePath):
            os.makedirs(self.__archivePath)
            
    def reslovePaths(self):
        '''
        updates the init variables with correct data
        '''
        if not os.path.isfile(self.filePath):
            raise StandardError('supplied path is not a valid file path')
        self.filePath = os.path.normpath(self.filePath)
        self.__name, self.__extension = self.getFileNameExt()
        self.__archivePath = os.path.join(os.path.dirname(self.filePath), "archive", self.getUser(), self.__name )

    def getArchivePath(self):
        return self.__archivePath
            
    def getFileNameExt(self):
        return os.path.splitext(os.path.basename(self.filePath))
            
    def getArchiveFiles(self):
        if os.path.exists(self.__archivePath):
            return  sorted(os.listdir(self.__archivePath))
            
    def getUser(self):
        return os.getenv('USERNAME') or os.getenv('USER')
        
    @property
    def archiveLimit(self):
        return self.limit
        
    @archiveLimit.setter
    def archiveLimit(self, value):
        if value:
            self.limit = value
            
    def getNewNumber(self, oldList):
        '''
        finds the last version number from the archive list and adds 1
        *oldList : List of archive fils in archive folder
        '''
        if oldList:
            newNumber = re.search('(?<=\.)\d{3}', oldList[-1:][0])
            if newNumber:
                return '%03d' % (int(newNumber.group(0)) +1)
            else:
                raise StandardError("Error reading version number of last archived file")
        else:
            return '001'
            
    def parseArgs(self):
        '''
        parse command line arguments
        '''
        import getopt
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hf:nl:n", ["help", "file=", "limit="])
            for o,a in opts:
                if o in ("-f", "--file") :
                    self.filePath = a
                    
                elif o in ("-l", "--limit"):
                    if a.isdigit():
                        self.archiveLimit = int(a)
                    else:
                        print "Limit flag requires a number; using default limit"
                    
                elif o in ("-h","--help"):
                    self.argsHelp()
                    sys.exit()
                else:
                    assert False, "unhandled option"
                
        except getopt.GetoptError, err:
            print str(err)
            sys.exit(2)
    
    def argsHelp(self):
        '''
        printer for command line help
        '''
        print '''
            command list : \t-f (--file)
                                -h (--help)
                                -l (--limit)

            --------------------------------------------------------
            --------------A file path MUST be specified-------------
            --------------------------------------------------------
            The (-f) or (--file) flag must be used.
            This specifies the exact path file to be archived

            The (-l) or (--limit) flag is optional.
            This will limit the total number of archived files'''
                    
    def archive(self):
        '''
        main archiveing method
        '''
        self.parseArgs()
        
        if not self.filePath:
            sys.exit("no file found to archive")
        self.reslovePaths()
        self.makeArchiveDir()
        
        archiveList = self.getArchiveFiles()
        
        n = self.getNewNumber(archiveList)
        newArchiveFile = os.path.join(self.__archivePath, '%s.%s%s' % (self.__name, n, self.__extension))
        shutil.copyfile(self.filePath, newArchiveFile)
        
        #WARNING: using folder Limit will destroy archived files.
        while len(archiveList) >= self.limit:
            os.remove(os.path.join(self.__archivePath, archiveList[0]))
            archiveList.pop(0)
            print 'Destroying old archive: %s' % archiveList[0]
            
        print 'Archived successfully: (v.%03d) of file %s%s\n' % ( int(n), self.__name, self.__extension)
        raw_input("Press any key to exit.")
if __name__ == '__main__':
    myArchiver().archive()
    
