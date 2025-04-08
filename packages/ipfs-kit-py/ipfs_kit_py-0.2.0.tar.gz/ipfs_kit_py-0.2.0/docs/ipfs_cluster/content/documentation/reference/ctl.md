+++
title = "ipfs-cluster-ctl"
weight = 30
aliases = [
    "/documentation/ipfs-cluster-ctl"
]
+++

# `ipfs-cluster-ctl`

The `ipfs-cluster-ctl` command line application is a user-friendly REST API client for IPFS Cluster. It allows to perform all the operations supported by a Cluster peer:

* [Pinning](/documentation/guides/pinning#pinning-cids)
* [Unpinning](/documentation/guides/pinning#pinning-cids)
* [Adding](/documentation/guides/pinning#adding-files)
* [Listing items in the pinset](/documentation/guides/pinning#pin-ls-vs-status)
* [Checking the status of pins](/documentation/guides/pinning#pin-ls-vs-status)
* [Listing cluster peers](/documentation/guides/peerset#listing-peers)
* [Removing peers](/documentation/guides/peerset#removing-peers)

## Usage

Usage information can be obtained by running:

```
$ ipfs-cluster-ctl --help
```

You can also obtain command-specific help with `ipfs-cluster-ctl help [cmd]`. The (`--host`) can be used to talk to any remote cluster peer (`localhost` is used by default). In summary, it works as follows:


```
$ ipfs-cluster-ctl id                                                       # show cluster peer and ipfs daemon information
$ ipfs-cluster-ctl peers ls                                                 # list cluster peers
$ ipfs-cluster-ctl peers rm <peerid>                                        # remove a cluster peer
$ ipfs-cluster-ctl add myfile.txt http://domain.com/file.txt                # adds content to the cluster
$ ipfs-cluster-ctl pin add Qma4Lid2T1F68E3Xa3CpE6vVJDLwxXLD8RfiB9g1Tmqp58   # pins a CID in the cluster
$ ipfs-cluster-ctl pin rm Qma4Lid2T1F68E3Xa3CpE6vVJDLwxXLD8RfiB9g1Tmqp58    # unpins a CID from the cluster
$ ipfs-cluster-ctl pin ls [CID]                                             # list tracked CIDs (shared state)
$ ipfs-cluster-ctl status [CID]                                             # list current status of tracked CIDs (local state)
$ ipfs-cluster-ctl sync Qma4Lid2T1F68E3Xa3CpE6vVJDLwxXLD8RfiB9g1Tmqp58      # re-sync seen status against status reported by the IPFS daemon
$ ipfs-cluster-ctl recover Qma4Lid2T1F68E3Xa3CpE6vVJDLwxXLD8RfiB9g1Tmqp58   # attempt to re-pin/unpin CIDs in error state
```

### Authentication

The IPFS Cluster API can be configured with Basic Authentication support.

`ipfs-cluster-ctl --basic-auth <username:password>` will use the given credentials to perform the request.

Note that unless `--force-http` is passed, using `basic-auth` is only supported on HTTPS requests or using the libp2p API endpoint (which uses an encrypted channel).

### Using the libp2p API endpoint

Since `0.3.5`, IPFS Cluster provides a libp2p endpoint for the HTTP API which provides channel security without the need to configure SSL certificates, by either re-using the peer's libp2p host or by setting up a new one with the given parameters in the API configuration.

In order to have `ipfs-cluster-ctl` use a libp2p endpoint, provide the `--host` flag as follows:

`ipfs-cluster-ctl --host /ip4/<ip>/ipfs/<peerID> ...`

or

`ipfs-cluster-ctl --host /dnsaddr/mydomain.com ...` (setting a `_dnsaddr TXT dnsaddr=peer_multiaddress` field in your dns).

If the libp2p peer you're contacting is using a *cluster secret* (a private networks key), you will also need to provide `--secret <32 byte-hex-encoded key>` to the command.

We recommend that you alias the `ipfs-cluster-ctl` command in your shell to something shorter and with the right global options.

### Exit codes

`ipfs-cluster-ctl` will exit with:

* `0`: the request/operation succeeded. The output contains the response data.
* `1`: argument error, network error or any other error which prevented the application to perform a request and obtain a response from the IPFS Cluster API. In such case, the output contains the contents of the error and the HTTP code `0`.
* `2`: IPFS Cluster peer error. The request was performed correctly but the response is an error (HTTP status 4xx or 5xx). In such case, the output contains the contents of the error and the HTTP code associated to it.

### Debugging

`ipfs-cluster-ctl` takes a `--debug` flag which allows to inspect request paths and raw response bodies.

## Download

To download `ipfs-cluster-ctl` check the [downloads page](/download).
