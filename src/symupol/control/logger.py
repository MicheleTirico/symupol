import datetime
import os.path

class Logger:

    def __init__(self,config,storeLog):
        self.__config=config
        self.__storeLog=storeLog

    def initStoreLog(self):
        if self.__storeLog:
            if os.path.exists(self.__config.pathLog): os.system("rm "+self.__config.pathLog)
            open(self.__config.pathLog, 'a').close()

    def storeLocal(self,run):
        self.__storeLocal=run
        self.__listMessages=[]

    def storeFile(self):
        with open(self.__config.pathLog, "a") as f:
            f.write("Log of symupol \n")
            for mess in self.__listMessages:
                f.write(mess +"\n")
        self.__storeLocal=False


    def log (self,cl,method,message):
        try:
            if self.__displayLog:
                mess= self.__completeMessage("LOG",cl,method,message)
                print (mess)
            if self.__storeLocal:
                self.__listMessages.append(mess)
            elif self.__storeLog:
                with open(self.__config.pathLog, "a") as f:     f.write(mess+"\n")
        except AttributeError:print ("peppe")

    def setDisplay(self,displayLog,displayWarning,displayError,displayStateSim):
        self.__displayLog=displayLog
        self.__displayWarning=displayWarning
        self.__displayError=displayError
        self.__displayStateSim=displayStateSim


    def error (self,cl,method,message,error):
        try: message+=" (error: "+str(error.__name__)+ ")"
        except AttributeError: message+=" (error: "+error+ ")"
        if self.__displayError:
            mess=self.__completeMessage("ERR",cl,method,message)
            if self.__storeLocal:
                self.__listMessages.append(mess)
            elif  self.__storeLog:
                with open(self.__config.pathLog, "a") as f:     f.write(mess+"\n")
            print (mess)

    """
    doQuit: the whole process end if warning is activated
    doReturn: if warning is active, return True
    """
    def warning (self,cl,method,message,doQuit,doReturn):
        if self.__displayWarning:
            mess =self.__completeMessage("WAR",cl,method,message)
            if self.__storeLocal:
                self.__listMessages.append(mess)
            elif self.__storeLog:
                with open(self.__config.pathLog, "a") as f:     f.write(mess+"\n")
            print (mess)

            if doQuit: quit()
            if doReturn: return True

    def __completeMessage (self,state,cl,method,message):
        time=str(datetime.datetime.now())

        if type(cl)==str: displayCl=cl
        elif cl==None:displayCl="no class"
        else:displayCl=cl.__class__.__name__

        if method==None or method=="":    displayMt="no method"
        else:   displayMt=method.f_code.co_name
        return "{} {} {} {} {} {} {}".format(time,"{0:<4s}".format(state),message,"(class:",displayCl,", method:",displayMt+")")