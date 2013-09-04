# Unix Guest Agent for Openstack

>  This guest agent provides functionality such as configuring the networking for a guest.

### Layout:

```ASCII
src/       -- The main agent daemon code, written in C, which embeds the
              python interpreter
include/   -- Include files for src/
lib/       -- Supporting code for the main agent daemon, along with a
              python module wrapper
plugins/   -- Python plugin modules (for communication and command parsing)
commands/  -- Python modules that implement the real code for commands
tests/     -- Unit tests
scripts/   -- Startup and misc scripts
```
***

### Plug-in Info

There are currently 2 types of plugins, exchanges and parsers.  Exchange plugins are those that handle the low level communication between a client and the daemon.  Parser plugins are those that can decode the communication protocol.

Currently, there's 1 exchange plugin, xscomm.py, and 1 parser plugin, jsonparser.py.  xscomm.py handles communication via XenStore and the parser plugin will decode/encode json for the  requests/responses. 

***

### Exchange Plug-in

Needs to define a class that contains the following methods:

* get_request():
> - Has no arguments
> - Returns some sort of request object

* put_response(request, response):
> - Has request and response arguments
> - Returns None (return value is ignored)

***

### Parser Plug-in

Needs to define a class that contains the following methods:

* parse_request(request):
> - Takes a request object returned from an Exchange plugin's get_request()
> - Returns a response object that will be passed to an Exchange plugin's put_response()

~
***

### Command Modules

commands/__init__.py implements a class called 'CommandBase' that is used to create commands by subclassing it.  This automatic registering of commands via the subclassing occurs via a metaclass.

To create a new command:

> * create a class that derrives from commands.CommandBase
> * define a method in your class that uses this decorator:
> > -   @commands.command_add('<command_name>')
> > -   (obviously replace the decorator argument with the right command name)

***
 
### Misc.

jsonparser.py requires a class instance to be passed on init which defines a 'run_command' method.

When importing 'commands', it replaces the 'commands' module with a wrapper, so you can use the 'commands' attribute directly instead of having to use commands.CommandBase

Call commands.init() to init all of the command classes Pass the result to JsonParser

***

### Example Configuration File

* Needed to register the exchange/parser plugin combiniation with the
> * main daemon
> > - import agentlib

* To get jsonparser and xscomm
> * import plugins

*  Loads 'commands' plus all modules that contain command classes
> * import commands.command_list

*  Not required, as the default is False
> * test_mode = False

* Inits all command classes
> * c = commands.init()

* Creates instance of JsonParser, passing in available commands
> * parser = plugins.JsonParser(c)

* Create the XSComm intance
> * xs = plugins.XSComm()

* Register an exchange/parser combination with the main daemon
> * agentlib.register(xs, parser)

***
