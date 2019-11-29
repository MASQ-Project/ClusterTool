# Explanation of files

## tnt_config.py

Stuff that you will likely have to change to set up your own TNT is configured in `tnt_config.py`.
This currently includes lists of instances that we have configured on various platforms (described in detail in [README](README.md))
as well as platform-specific configuration items ("project", etc).

## config.py

The list of all commands that are available in the TNT is configured in `config.py`. When developing a new command, remember to add it to this list to make it available for use.

## instance.py

TNT commands are mostly implemented within `instance.py`. This is the file that has the ability
to start or stop MASQNode, revert or subvert DNS, start, stop or verify traffic, etc, on the configured
instances.

_The word *instance* is definitely overloaded in TNT. An instance generally refers to a cloud instance or VM, but can also refer to the class `Instance`, defined in this file, that handles all the communication to and from those instances._

This file uses some helper files to accomplish related tasks:

 - node.py: MASQNode related logic
 - dns.py: DnsUtility related logic
 - traffic_handler: traffic generation/verification

### Traffic Files

`wget.py` and `curl.py` are helper classes that make it easier to track the traffic we have requested on
an instance. They share an interface so that we can track them both the same way with `traffic_handles` (in `instance.py`)
when we want to verify the traffic later.

## instance_api.py

InstanceApi defines the required interface for different platform implementations.
For Google, this is implemented in `compute.py`. For Amazon, `ec2.py`. VirtualBox, `virtualbox.py`. Docker, `docker.py`

Each new implementation should extend InstanceApi so that the interface can be enforced.

## command.py

Command and SelectCommand are implemented in `command.py`. All commands listed in `config.py` are one of these two objects.

SelectCommands will prompt you for which of the configured/running INSTANCES you would like to run the command.
They can also accept the additional input at the same time as the command:

`start all`
rather than 
`start` followed by a prompt, and then `all`.

## runner.py

This contains the main loop of the TNT. It prompts the user for the next command they want to run until they indicate
they want to exit with a blank line (or until the TNT blows up :left_shark:).

This is also where the initial `init` command is automatically called, and where we may one day warn you that you are
exiting without shutting down your instances.

## test_net.py

`test_net.py` is just a convenient wrapper around `runner.py` so that you don't have to `python runner.py`
(which has slightly less meaning than `python test_net.py`) and also it's executable so you can really just
`./test_net.py` if you want.

## Other Files

There are several other files that have names that match commands. These are commands that were not simple enough to inline
(like many in `config.py`), so their additional functionality was pulled into their own files.

These files follow what is currently just a convention: 2 public functions, `name` and `command`, that will return what they
sound like they return. You can see how they are used in `config.py`.

**`wget.py` and `curl.py` are exceptions to this.** Even though they are also commands, these files are
_different_. See the **Traffic Files** sub-section under the **instance.py** section above for more detail.
