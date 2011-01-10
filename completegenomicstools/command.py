import optparse

class Commands(dict):
    """
    This is a simple class for storing names of commands and their associated runnables.
    """

class CommandLineProgram:
    """Encapsulate a callable class.

    Use like so:

    import CommandLineProgram
    class abc(CommandLineProgram)
    

    def __init__(self,name=None):
        if(name is not None):
            self.name=name
        else:
            self.name=self.__class__.__name__
        self.options=[]

    def getOptions(self):
        """Return a list of argparser options"""
        return(self.options)

    def __call__(self,opts,args):
        """
        This is the body of the CommandLineProgram.  Put business logic here.
        
        :param opts: list of options after argparse has dealt with them
        :param args: list of positional arguments after argparse has parsed options
        """
        pass
