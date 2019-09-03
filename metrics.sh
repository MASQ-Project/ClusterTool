#!/usr/bin/env bash

# Find count Gossip Received
echo "Received Gossip"
grep 'Received Gossip: digraph db' /tmp/SubstratumNode_rCURRENT.log | wc -l


# Find count of gossip sent
echo "Sent Gossip"
grep 'Sending update Gossip about' /tmp/SubstratumNode_rCURRENT.log | wc -l