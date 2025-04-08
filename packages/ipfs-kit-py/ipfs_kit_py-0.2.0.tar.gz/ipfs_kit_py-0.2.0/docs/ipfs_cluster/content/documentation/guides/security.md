+++
title = "Security and ports"
weight = 30
aliases = [
    "/documentation/security"
]
+++

# Security and ports

This section explores some security considerations when running IPFS Cluster.

There are four types of endpoints in IPFS Cluster to be taken into account when protecting access to the system. Exposing an unprotected endpoint might give anyone control of the cluster. Cluster configuration uses sensible defaults.

* [The cluster secret](#the-cluster-secret)
* [The `trusted_peers` in CRDT mode](#the-trusted-peers-in-crdt-mode)
* [Ports and endpoints overview](#ports-overview)

## The cluster secret

The 32-byte hex-encoded `secret` in the `service.json` file acts as libp2p network protector. This provides additional encryption for all communications between peers (libp2p) using a pre-shared key.

This makes it impossible to communicate with a peer's swarm endpoint (see below) and thus, to send RPC commands to that peer, without knowing the secret in advance.

The secret is a **security requirement for raft-based clusters** which do not enforce any RPC authorization policy. CRDT-based clusters can run with an empty secret as long as `trusted_peers` is correctly set: only the peers in `trusted_peers` can modify the pinset and perform actions.

However, we recommend to set the `secret` in all cases, as it provides network isolation: clusters running without a secret may discover and connect to the main IPFS network, which is mostly useless for the cluster peers (and for the IPFS network).

## The `trusted_peers` in CRDT mode

The `trusted_peers` option in the `crdt` section of the `service.json` file provides access control to the peer RPC endpoints and allows modifications of the pinset issued by the peers in that array (as identified by their peer IDs), but **only apply to clusters running in crdt-mode**.

Trusted peers can:

* Modify the pinset: indirectly trigger pin/unpin operations
* Trigger status sync operations (resulting in `ipfs pin ls`)
* Add content to the peer (resulting in `ipfs block put`)

Non-trusted peers only have access to ID and Version endpoints (returning IPFS and Cluster Peer information).

<div class="tipbox tip"><code>trusted_peers</code> can be set to <code>[ "*" ]</code> to trust every other peer.</div>

## Ports overview

  * Cluster swarm: `tcp:9096` is used by the Cluster swarm and protected by the *shared secret*. It is OK to expose this port (the cluster `secret` acts as password to interact with it).
  * HTTP API: `tcp:9094` can be exposed when [enabling SSL and setting up basic authentication](/documentation/reference/configuration/#restapi)
  * IPFS Pinning API endpoint: `tcp:9097` similar to the HTTP endpoint above.
  * libp2p-HTTP API: when using an alternative [libp2p host](/documentation/reference/configuration/#restapi), for the api, the `libp2p_listen_multiaddress` can be exposed when basic authentication is enabled.
  * IPFS API: `tcp:5001` is the API of the IPFS daemon and should not be exposed to other than `localhost`.
  * IPFS Proxy endpoint: `tcp:9095` should not be exposed without an authentication mechanism on top (`nginx` etc...). By default it provides no authentication nor encryption (similar to IPFS's `tcp:5001`)
  * Prometheus: when metrics are enabled, they are by default exposed on `tcp:8888`.
  * Jaeger: when tracing is enabled, it uses `tcp:6831` by default to expose the Jaeger service.

Read the sections below to get a more detailed explanation.

### Cluster swarm endpoints

The endpoint is controlled by the `cluster.listen_multiaddress` configuration key, defaults to `/ip4/0.0.0.0/tcp/9096` and represents the listening address to establish communication with other peers (via Remote RPC calls and consensus protocol).

As explained above, the *shared secret* controls authorization by locking this endpoint so that only the cluster peers holding the secret can communicate. We recommend to never run with an empty secret.

### HTTP API and IPFS Pinning Service API endpoints

IPFS Cluster peers provide by default an **HTTP API endpoint** and an **IPFS Pinning Service API endpoint** which can be configured with SSL. It also provides a **libp2p API endpoint** for each, which re-uses either the Cluster libp2p host or a specifically configured libp2p host.

These endpoints are controlled by the `*.http_listen_multiaddress` (default `/ip4/127.0.0.1/tcp/9094`) and the `*.libp2p_listen_multiaddress` (if a specific `private_key` and `id` are configured in the `restapi/pinsvcapi` sections).

Note that when no additional libp2p host is configured and running in Raft mode, the Cluster's peer libp2p host (which listens on `0.0.0.0`) is re-used to provide the libp2p API endpoint. As explained, this endpoint is only protected by the *cluster secret*. When running in CRDT mode, the libp2p endpoint is disabled, as the cluster secret may be shared and would otherwise expose an open endpoint to the world. In order to run a lib2p API endpoint when using CRDT mode, configure an additional, separate libp2p host in the `restapi` configuration.

Both endpoints support **Basic Authentication** but are unauthenticated by default.

Access to these endpoints allow to fully control an IPFS Cluster peer, so they should be adecuately protected when they are opened up to other than `localhost`. The secure channel provided by the configurable SSL or libp2p endpoint, along with Basic Authentication, allow to safely use these endpoints for remote administration.

The `restapi/pinsvcapi` configurations offer a number of variables to configure `CORS` headers. By default, `Allow-Origin` is set to `*` and `Allow-Methods` to `GET`. You should verify that this configuration is suitable for your needs, application and environment.

These APIs can be disabled altogether by removing the `restapi/pinsvcapi` sections from the configuration. If the REST API is disabled, `ipfs-cluster-ctl` will be unable to talk to the peer.

### IPFS and IPFS Proxy endpoints

IPFS Cluster peers communicate with the IPFS daemon (usually running on localhost) via plain, unauthenticated HTTP, using the IPFS HTTP API (by default on `/ip4/127.0.0.1/tcp/9095`.

IPFS Cluster peers also provide an unauthenticated HTTP IPFS Proxy endpoint, controlled by the `ipfshttp.proxy_listen_multiaddress` option which defaults to `/ip4/127.0.0.1/tcp/9095`.

Access to any of these two endpoints imply control of the IPFS daemon and of IPFS Cluster to a certain extent. Thus they run on `localhost` by default.

The IPFS Proxy will attempt to mimic CORS configuration from the IPFS daemon. If your application security depends on CORS, you should configure the IPFS daemon first, and then verify that the responses from hijacked endpoints in the proxy look as expected. `OPTIONS` requests are always proxied to IPFS.

The IPFS Proxy API can be disabled altogether by removing the `ipfsproxy` section from the configuration.
