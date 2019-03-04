# Using TNT
## How to run

Start TNT with `python test_net.py` or, on Linux and Mac, simply `./test_net.py`.

When you first start TNT it automatically calls the `init` command and the `info` command.

Then, TNT prints a list of available commands, and continues to accept and run commands until
a blank line is entered at the top level, which exits TNT. Commands which accept additional input
will usually be canceled if a blank line is entered, but that doesn't exit TNT -- just the command.
If an unrecognized command is entered, the initial list of commands is displayed again.

## First, a note about TNT Commands
There are currently 2 kinds of commands in TNT: SelectCommands and regular Commands.

### Select Command
A SelectCommand operates on one or more of the configured `INSTANCES`, as specified by the user.

If a SelectCommand is called with no additional input (e.g. `start`), it will prompt for which instances to operate on:
it lists the available instances by name, and you can specify one or more of those (space-delimited),
or `all` to operate on all of them.

If one or only a few instances are specified when a SelectCommand prompts, it will run for the instances
specified and then prompt again; a blank line will cancel additional runs of the SelectCommand.
If `all` is specified, or if all instances are manually specified, a SelectCommand will not prompt for additional
instances once it completes.

Once you get comfortable using TNT and are familiar with which commands are SelectCommands, you can specify
instances inline with the command to avoid multiple prompts (e.g. `start bootstrap`).

SelectCommands sort the instance names provided to it before running, so if `all` is specified, for example,
`bootstrap` will be run first, followed by `node-1`, then `node-2`, etc.

### Command
Regular Commands are less common in TNT; they generally do not operate on the INSTANCES, or, if they do,
they always operate on all of them.

## TNT Commands
### init

_Implemented in `init.py`_

`init` is a regular Command that prompts you for the information needed to set up the instances that will be used to run TNT.
It fills in the `INSTANCES` global state (held in `tnt_config.py`) which is how TNT talks to the instances
it uses for running nodes.

Then, once INSTANCES is configured, it "starts" the instances -- calls into the instance platform to ensure that each
instance is running so that TNT can interact with it later on.

`init` automatically generates local names for the instances. It names the first one `bootstrap`, the next one `node-1`,
then `node-2`, etc.

**WARNING:** The name generator currently does **not** gracefully handle taking down a single node and bringing it back up.
There are notes/TODOs about this in `init.py`.

`init` has 2 modes:

#### automatic
In this mode, you will be prompted for:

- whether you want this run to use cloud instances or local ones
    - currently cloud/local cannot be used together, but they may be made compatible in the future
    - these options are currently hardcoded; it may be useful to pull them out into a configuration
- how many of those instances you want to use for this run
    - it combines the configured instance lists of the specified platform group (from `tnt_config`), then "checks out" (removes)
    the specified number of nodes from the combined list. This usually results in the platforms being used serially rather than mixed
    (i.e. all of the Google instances will be used before any of the Amazon ones, etc).
    In the future, we may find it useful to change the implementation to choose more randomly.

#### manual (currently disabled)
In this mode, you will be prompted repeatedly (until a blank line is entered) for:

- what platform you want this instance to use - current options are: `google`, `amazon`, `local`
    - these options are currently hardcoded; it may be useful to pull them out into a configuration

In manual mode, the first instance in the specified platform list is used.
In the future, we should prompt for which instance to use by name to allow for better coordination between concurrent TNT users.

### info

_Implemented in `info.py`_

`info` is a regular Command that waits for each instance (in `INSTANCES`) to report its ip address, then prints it out.
**WARNING:** It does not currently check whether the instance is running before waiting (forever) for the ip address.
There is a note about this in `info.py` and it should probably be corrected.

### update

_Implemented in `update.py`_

`update` is a SelectCommand that uploads new binaries for `SubstratumNode` and `dns_utility` to the instance(s) specified.
It currently looks for the binaries in the same directory as the TNT, and **be warned:** it is not graceful when they are not found.
It will crash if the binaries are not found.

### start

_Implemented in `start.py`_

`start` is a SelectCommand that starts SubstratumNode on the instance(s) you specify.

The `bootstrap` node must always be started first.
If you try to start any other node before `bootstrap`, `start` will complain.

`start` will also complain if you try to start `bootstrap` more than once.
However, it does not prevent you from starting any other node more than once.

If nodes are started in an acceptable order, the `start` command will call the relevant `instance.py` function:
`start_bootstrap_node` or `start_node` (sending in the `bootstrap` node descriptor).

The first thing `start` does is remove any existing `SubstratumNode.log` file.
This is to ensure that the log will only contain the current node descriptor.

Once the previous log is removed, SubstratumNode is started with the following parameters:
- `--dns_servers 1.1.1.1`
- `--log_level trace`
- `--port_count 1`
- `--home /tmp`
- `--ip <ip addr of the instance>`
- `--wallet_address <fake address calculated from ip address>`
- either `--type bootstrap` or `--neighbor <bootstrap descriptor>`

Once SubstratumNode is started, `start` waits for the node descriptor to appear in the logs before completing.
This is particularly important for the `bootstrap` node, since all the other nodes will require its descriptor to start.

### tail

_Implemented in `instance.py`_

_Linux-only_

`tail` is a SelectCommand that calls `tail -f` the `SubstratumNode.log` of the instance(s) specified in a new terminal window (per specified instance).

### subvert

_Implemented in `instance.py`_

`subvert` is a SelectCommand that subverts the DNS of the instance(s) specified.
This means that any traffic originating from the instance(s) will be routed through the SubstratumNetwork;
it is equivalent to the `consuming` state in the GUI.

### curl

_Implemented in `instance.py`_

`curl` is a SelectCommand that generates some internet traffic on the instance(s) specified.
It prompts for how many times you want to run `curl` on each instance;
each `curl` retrieves `https://www.piday.org/million/`.

The website used for curl is hardcoded in `instance.py`.
It might be useful to pull this out into a configuration, or prompt the user for the website they wish to curl.

### wget

_Implemented in `instance.py`_

`wget` is a SelectCommand that generates some internet traffic on the instance(s) specified.
It starts `wget` on each instance, retrieving each of the following websites:
- nyan.cat
- substratum.net
- amplifyexchange.com
- google.com
- youtube.com
- wikipedia.org
- reddit.com
- yahoo.com
- amazon.com

These websites are currently hardcoded in `instance.py`.
It might be useful to pull these out into a configuration.

### verify

_Implemented in `instance.py`_

`verify` is a SelectCommand that displays the current status of any pending `wget` and/or `curl` commands running
on the instance specified. Perhaps they have not started yet; perhaps they have started but not finished; perhaps
they have failed; or perhaps they have produced the expected output. Perhaps several different pending commands are 
in different statuses.

### revert

_Implemented in `instance.py`_

`revert` is a SelectCommand that reverts the DNS of the instance(s) specified.
This means that any traffic originating from the instance(s) will no longer be routed through the SubstratumNetwork;
it is equivalent to the `earning` state in the GUI.

### inspect

_Implemented in `instance.py`_

`inspect` is a SelectCommand that retrieves the current state of the Neighborhood of the instance(s) specified,
and opens a visual graph of the Neighborhood in an image viewer.
It detects how many changes have happened in the Neighborhood by inspecting the `SubstratumNode.log` file of the instance,
and prompts you for which version you would like to see (until a blank line is entered).

### inbound

_Implemented in `instance.py`_

`inbound` is a SelectCommand that retrieves the Neighborhood Gossip messages that the specified instance(s) has received,
and opens a visual graph of the Gossip in an image viewer.
It detects how many messages have been received by inspecting the `SubstratumNode.log` file of the instance,
and prompts you for which one you would like to see (until a blank line is entered).

### outbound

_Implemented in `instance.py`_

`outbound` is a SelectCommand that retrieves the Neighborhood Gossip messages that the specified instance(s) has sent,
and opens a visual graph of the Gossip in an image viewer.
It detects how many messages have been sent by inspecting the `SubstratumNode.log` file of the instance,
and prompts you for which one you would like to see (until a blank line is entered).

### stop

_Implemented in `instance.py`_

`stop` is a SelectCommand that shuts down SubstratumNode on the instance(s) specified.
For each instance specified, It will:
- revert DNS
- kill the SubstratumNode process
- kill any traffic (`wget` or `curl`) that was being generated
- clear out any stale state (e.g. node descriptor) in the TNT instance

### finish

_Implemented in `finish.py`_

`finish` is a regular Command that downloads the `SubstratumNode.log` for all instances into a local directory and calls `stop` on each instance.
It prompts for a directory name to put the logs into; it will accept a name that contains no spaces and does not already exist.
If it receives invalid input, it will reprompt; a blank line will cancel the command.

### shell

_unix-only_

`shell` is a SelectCommand that will open a shell into the instance(s) specified in a new terminal window (per specified instance)

### kill

_Implemented in `kill.py`_

`kill` is a SelectCommand that shuts down the instance(s) specified -- not just SubstratumNode, but the whole instance.
The instances that are shut down are removed from the INSTANCES structure and put back into their corresponding "available instances" list based on their platform.

### nfo

_Implemented in `nfo.py`_

`nfo` is a SelectCommand that calls `kill` and then restarts the instance(s) specified.
It can be useful as a last resort if your instances are behaving a little strangely.
It's like toggling the power switch of the machine off and back on.

_Nuke From Orbit -- it's the only way to be sure..._

