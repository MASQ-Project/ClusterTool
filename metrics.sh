#!/usr/bin/env bash

# Find count Gossip Received
echo "Received Gossip"
grep 'Received Gossip: digraph db' /tmp/MASQNode_rCURRENT.log | wc -l


# Find count of gossip sent
echo "Sent Gossip"
grep 'Sending update Gossip about' /tmp/MASQNode_rCURRENT.log | wc -l