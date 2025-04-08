# The ipfs-cluster website

[![](https://img.shields.io/badge/made%20by-Protocol%20Labs-blue.svg?style=flat-square)](http://ipn.io)
[![Main project](https://img.shields.io/badge/project-ipfs-cluster-blue.svg?style=flat-square)](http://github.com/ipfs-cluster)
[![Matrix channel](https://img.shields.io/badge/matrix-%23ipfs--cluster-blue.svg?style=flat-square)](https://app.element.io/#/room/#ipfs-cluster:ipfs.io)
[![](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> Official website sources for http://ipfscluster.io

This repository contains the source code for the ipfs-cluster website available at http://ipfscluster.io. If you're looking for the open-source IPFS Cluster project itself, head to https://github.com/ipfs-cluster/ipfs-cluster.

This project builds out a static site to explain ipfs-cluster, ready for deployment on ipfs. It uses `hugo` to glue the html together. It provides an informative, public-facing website. The most important things are the words, concepts and links it presents.

## Install

```sh
git clone https://github.com/ipfs-cluster/ipfs-cluster-website
```

## Usage

To deploy the site ipfscluster.io, run:

```sh
# Build out the optimised site to ./public, where you can check it locally.
make

# Add the site to your local ipfs, you can check it via /ipfs/<hash>
make deploy

# Save your dnsimple api token as auth.token
cat "<api token here>" > auth.token

# Update the dns record for ipfscluster.io to point to the new ipfs hash.
make publish-to-domain
```

The following commands are available:

### `make`

Build the optimised site to the `./public` dir

### `make serve`

Preview the production ready site at http://localhost:1313 _(requires `hugo` on your `PATH`)_

### `make dev`

Start a hot-reloading dev server on http://localhost:1313 _(requires `hugo` on your `PATH`)_

### `make deploy`

Build the site in the `public` dir and add to `ipfs` _(requires `hugo` & `ipfs` on your `PATH`)_

### `make publish-to-domain` :rocket:

Update the DNS record for `ipfscluster.io`.  _(requires an `auto.token` file to be saved in the project root.)_

If you'd like to update the dnslink TXT record for another domain, pass `DOMAIN=<your domain here>` like so:

```sh
make publish-to-domain DOMAIN=tableflip.io
```

---

See the `Makefile` for the full list or run `make help` in the project root. You can pass the env var `DEBUG=true` to increase the verbosity of your chosen command.

## Maintainers

The ipfs-cluster team.

## Contribute

Please do! Check out the [issues](https://github.com/ipfs-cluster/ipfs-cluster-website/issues), or open a PR!

Check out our [contributing document](https://github.com/ipfs-cluster/ipfs-cluster/blob/master/contribute.md) for more information on how we work, and about contributing in general.

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

[MIT](LICENSE) © 2022 Protocol Labs Inc.
