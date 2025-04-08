+++
title = "REST API"
weight = 10
aliases = [
    "/documentation/developer/api"
]
+++

## REST API Reference

IPFS Cluster peers include an API component which provides HTTP-based access to the peer's functionality. The API attempts to be REST-ful in form and behaviour. It is enabled by default, but it can be disabled by removing its section from the `service.json` configuration file.

We do not maintain ad-hoc API documentation, as it gets easily out of date or, at worst, is inaccurate or buggy. Instead, we provide an easy way to find how to do what you need to do by using the `ipfs-cluster-ctl` command.

Running `ipfs-cluster-ctl --enc=json --debug <command>` will print information about the endpoint, the query options, the request body and raw responses for that command. Use it on a [test cluster](/documentation/quickstart/)!

`ipfs-cluster-ctl` is an HTTP API client to the REST API endpoint with full feature-parity that always works with the HTTP API as offered by a cluster peer on the same version. Anything that `ipfs-cluster-ctl` can do is supported by the REST API. The command flags usually control different request options.

As additional resources:

* All the available API endpoints and their parameters and object formats are supported and documented by the [Go API Client](https://pkg.go.dev/github.com/ipfs-cluster/ipfs-cluster/api/rest/client?tab=doc#Client).
* The [API source code is here](https://github.com/ipfs-cluster/ipfs-cluster/blob/master/api/rest/restapi.go) (the `routes` method is a good place to start).
* There are two Javascript client libraries: [js-cluster-client](https://github.com/ipfs-cluster/js-cluster-client) (old) and [NFT.storage's cluster client](https://github.com/nftstorage/ipfs-cluster) (new).
* The request body for the `/add` endpoint is a bit special, but it works just like the IPFS one. See the section below.

The above should be enough to find out about the existing endpoints, their methods and current supported options.

### Authentication

The REST API supports both Basic and JWT token authentication:

* Basic Authentication credentials are stored in `service.json` configuration file (`basic_auth_credentials`).
* JWT token authentication works by sending requests with an `Authorization: Bearer <JWT-token>` header. The access token can be obtained by querying the `POST /token` endpoint. In order to obtain an access token, the user needs to be part of `basic_auth_credentials` and have an associated password. The JWT token is tied to the user requesting it and signed using their password. The only way to revoke JWT tokens right now is to change or remove the original Basic Auth credentials, which need an ipfs-cluster-service restart.

### The `/add/` endpoint

The `/add` endpoint can be use to upload content to IPFS via the Cluster API. The Cluster peer is in charge of building or extracting the IPLD DAG, which is sent **block by block** to the cluster peers where it should be pinned, which in turn perform `block/put` calls to the IPFS daemon they are connected to. At the end of the process, a Cluster-Pin happens and with it the pinning operation arrives to the IPFS daemons which should already have all the needed blocks.

There are considerations to take into account here:

* Adding content via IPFS Cluster is slower because it replicates to all pinning locations at the same time that it adds.
* The `local=true` query parameter will instruct the cluster peer receiving the request to ingest all blocks locally. This makes adding way faster and the expense of a slower Cluster-pinning: the pinning nodes will have to use IPFS to receive the blocks when they are instructed to pin.
* IPFS garbage collection should be disabled while adding. Because blocks are block/put individually, if a GC operation happens while and adding operation is underway, and before the blocks have been pinned, they would be deleted.

Currently IPFS Cluster supports adding with two DAG-formats (`?format=` query parameter):

* By default it uses the `unixfs` format. In this mode, the request body is expected to be a multipart just like described in [`/api/v0/add` documentation](https://docs.ipfs.tech/reference/kubo/rpc/#api-v0-add). The `/add` endpoint supports the same optional parameters as IPFS does and produces exactly the same DAG as go-ipfs when adding files. In UnixFS, files uploaded in the request are chunked and a DAG is built replicating the desired folder layout. This is done by the cluster peer.
* Alternatively, the `/add` endpoint also accepts a CAR file with `?format=car` format. In this case, the CAR file already includes the blocks that need to be added to IPFS and Cluster does not do any further processing (similarly to `ipfs dag import`). At the moment, the `/add` endpoint will process only a single CAR file and this file must have only one root (the one that will be pinned). CAR files allow adding arbitrary IPLD-DAGs through the Cluster API.

<div class="tipbox warning">Using the <code>/add</code> endpoint with Nginx in front as a reverse proxy may cause problems. Make sure to add <code>?stream-channels=false</code> to every Add request to avoid them.<br /><br />The problems manifest themselves as "connection reset by peer while reading upstream" errors in the logs. They are caused by read after write on the HTTP request/response cycle: Nginx refuses any application that has started sending the response body to read further from the request body (<a href="https://trac.nginx.org/nginx/ticket/1293" target="_blank">see bug report</a>). IPFS and IPFS Cluster send object updates while adding files, therefore triggering the situation, which is otherwise legal per HTTP specs. The issue depends on Nginx internal buffering and may appear very sporadically or not at all, but it exists.</div>

### List of endpoints

As a final tip, this table provides a quick summary of methods available.

|Method      |Endpoint              |Comment                          |
|:-----------|:---------------------|:--------------------------------|
|`GET`       |`/id`                 |Cluster peer information         |
|`GET`       |`/version`            |Cluster version|
|`GET`       |`/peers`              |Cluster peers. Streaming endpoint.|
|`DELETE`    |`/peers/{peerID}`     |Remove a peer|
|`POST`      |`/add`                |Add content to the cluster. Streaming endpoint. See notes above |
|`GET`       |`/allocations`        |List of pins and their allocations (pinset). Streaming endpoint. |
|`GET`       |`/allocations/{cid}`  |Show a single pin and its allocations (from the pinset)|
|`GET`       |`/pins`               |Local status of all tracked CIDs. Streaming endpoint. |
|`GET`       |`/pins/{cid}`         |Local status of single CID|
|`POST`      |`/pins/{cid}`         |Pin a CID|
|`POST`      |`/pins/{ipfs\|ipns\|ipld}/<path>`|Pin using an IPFS path|
|`DELETE`    |`/pins/{cid}`         |Unpin a CID|
|`DELETE`    |`/pins/{ipfs\|ipns\|ipld}/<path>`|Unpin using an IPFS path|
|`POST`      |`/pins/{cid}/recover` |Recover a CID|
|`POST`      |`/pins/recover`       |Recover all pins in the receiving Cluster peer|
|`GET`       |`/monitor/metrics`    |Get a list of metric types known to the peer |
|`GET`       |`/monitor/metrics/{metric}`    |Get a list of current metrics seen by this peer |
|`GET`       |`/health/alerts`       |Display a list of alerts (metric expiration events) |
|`GET`       |`/health/graph`        |Get connection graph |
|`GET`       |`/health/bandwidth`    |Get bandwidth statistics for libp2p protocols |
|`POST`      |`/ipfs/gc`             |Perform GC in the IPFS nodes |
|`POST`      |`/token`               |Generate a new JWT token for current user |
|`GET`      |`/health`               |Returns 204. Does not require auth. |
