# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
def wrap_with_ssh(user, ip, command_list):
    args = [
        "ssh",
        "-oStrictHostKeyChecking=no",
        "%s@%s" % (user, ip),
        ]
    args.extend(command_list)
    #args.extend(["> /dev/null", "2>&1"])
    return args
