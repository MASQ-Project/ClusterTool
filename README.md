# Test Net Tools

## Dev notes
We used Python 2.7.12 to develop TNT

TNT uses `ssh` to interact with cloud instances or local VirtualBox VMs.
The instances must be set up to use the same user's ssh key.

## Setup
Requires installation of python dependencies (listed in [requirements.txt](requirements.txt))

```
ci/setup.sh
```

Also, GraphViz has to be installed not just for python...
```
sudo apt-get install graphviz
```

_If you want to be able to update the binaries the instances run via the TNT,_
_run the TNT script from a directory that has a `binaries` directory with `MASQNode` and `dns_utility` executables_
_in it._

Create your own modifiable version of `tnt_config.py` based off of `tnt_config_template.py`.
```
cp tnt_config_template.py tnt_config.py
```

Fill in the INSTANCE_USER to match the account needed to connect to your instances.

### **Additional Setup Required for Mac**
Some TNT commands execute commands in new terminal windows.
On a Mac, the default Terminal does not support this, so TNT on Mac relies on iTerm.
The main loop of TNT can be run from a regular Terminal, but in order to `ssh` or `tail`, you must have iTerm installed.

### To use with Google Cloud
Requires installation of python library [`googleapiclient`](https://cloud.google.com/compute/docs/tutorials/python-guide)

Also requires that `GOOGLE_APPLICATION_CREDENTIALS` environment variable be set to point to a JSON file containing credentials for authentication to google cloud.
(This hasn't been checked in.)

Fill in the COMPUTE_CONFIG dictionary in tnt_config.py to match your project and zone configuration.
Fill in the COMPUTE_INSTANCES list in tnt_config.py to include your compute instances i.e. `Google('<name_of_cloud_instance>')`.

We recommend using templates when creating multiple cloud instances. You'll need to setup SSH keys on all the instances
in order for ssh to work without prompting for a password.

### To use with AWS EC2
Requires installation of python library `boto3`

```
sudo -H pip install boto3
```

You'll need to set up your AWS credentials
([see the AWS documentation](https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html)).
Also requires that AWS credentials and config files exist in the `~/.aws/` directory

Fill in the EC2_CONFIG dictionary in tnt_config.py to include your ec2 region.
Fill in the EC2_INSTANCES list in tnt_config.py to include your ec2 instances i.e. `Amazon('<name_of_ec2_instance>')`.

We recommend using templates when creating multiple cloud instances. You'll need to setup SSH keys on all the instances
in order for ssh to work without prompting for a password.

### To use with VirtualBox
In VirtualBox create a VM with Bridged networking (so it will have its own IP)

To create more you can clone the existing VM, but remember to check the box to regenerate the MAC address,
and once it is created, change the hostname (in `/etc/hostname`) to match the VM name. Finally, restart the VM.

Fill in the VIRTUALBOX_INSTANCES list in tnt_config.py to include your virtualbox instances i.e. `VBox('<name_of_vbox_instance>')`.

### To use with Docker

Requires building the docker image

```
ci/setup_docker.sh
```

## Running the Tests
Run the tests with pytest.
```bash
pytest
```

## Running Code Coverage
Install pytest-cov, then run `ci/coverage.sh`

## Other Documentation
- [Code Structure README](CODE_STRUCTURE.md)
- [Usage README](USAGE.md)
