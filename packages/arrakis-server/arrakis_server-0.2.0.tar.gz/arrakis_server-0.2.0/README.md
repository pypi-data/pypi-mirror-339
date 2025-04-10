<h1 align="center">arrakis-server</h1>

<p align="center">Arrakis server</p>

<p align="center">
  <a href="https://git.ligo.org/ngdd/arrakis-server/-/pipelines/latest">
    <img alt="ci" src="https://git.ligo.org/ngdd/arrakis-server/badges/main/pipeline.svg" />
  </a>
  <a href="https://ngdd.docs.ligo.org/arrakis-server/">
    <img alt="documentation" src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat" />
  </a>
  <a href="https://pypi.org/project/arrakis-server/">
    <img alt="pypi version" src="https://img.shields.io/pypi/v/arrakis-server.svg" />
  </a>

</p>

---

## Installation

```
pip install arrakis-server
```

## Docker

```
docker run --net=host -it docker://containers.ligo.org/ngdd/arrakis-server:main
```

## Features

TODO

## Quickstart

1. Run `arrakis-server mock`.
2. Make client requests through the [Arrakis client library](https://git.ligo.org/ngdd/arrakis-python).
3. Shut down the server instance with Ctrl-C.
