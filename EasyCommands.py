"""
    Easy Commands
    ~ Easy to deploy commands base script.
"""
class cmd( object ):
    def __init__( self ):
        self.cmdlist = {};
        global modules;
        for object in modules:
            if( object[0:4] == "cmd_" ):
                self.cmdlist[object[4:]] = "%s(" % object;
        return self.input();
    
    def input( self ):
        while True:
            cmdText = input( "> " );
            params = cmdText.split();
            self.processCmd( params );
        
    def processCmd( self, params ):
        for cmd in self.cmdlist:
            if( cmd == params[0] ):
                eval( "%s params[1:])" % self.cmdlist[cmd] );

"""
    All the commands are here.
"""

#def cmd_[the command the user inputs]( the parameters );
def cmd_mycommand( params ):
    print( 'cmd_mycommand( params ) passed with: %s.' % params );
    return 1;

"""
    Initalize the class' object, get the list of modules.
"""
modules = dir();
__cmd__ = cmd();
