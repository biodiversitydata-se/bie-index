# Bie-index

## Setup

Create data directory at `/data/bie-index` and populate as below (it is easiest to symlink the config files to the ones in this repo):
```
mats@xps-13:/data/bie-index$ tree
.
└── config
    ├── bie-index-config.yml -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/bie-index-config.yml
    ├── conservation-lists.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/conservation-lists.json
    ├── image-lists.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/image-lists.json
    ├── locality-keywords.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/locality-keywords.json
    └── vernacular-lists.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/vernacular-lists.json
```

## Usage

Run locally:
```
make run
```

Build and run in Docker (using Tomcat):
```
make run-docker
```

Make a release. This will create a new tag and push it. A new Docker container will be built on Github.
```
mats@xps-13:~/src/biodiversitydata-se/bie-index (master *)$ make release

Current version: 1.0.1. Enter the new version (or press Enter for 1.0.2): 
Updating to version 1.0.2
Tag 1.0.2 created and pushed.
```

## Build search index

The solr search index can be built from scratch from the [GBIF Backbone Taxonomy](https://www.gbif.org/dataset/d7dddbf4-2cf0-4f39-9b2a-bb099caae36c). Before importing the data it needs to be pre-processed (see [process-backbone.py](./process-backbone.py) for details). 

* Download backbone (to `/data/bie-index/import`):
  ```
  make fetch-backbone
  ```
* Pre-process backbone:
  ```
  make process-backbone
  ```
* Go to the /admin page and select **DwCA Import** and import from `/data/bie-index/import/backbone` (~2:15h)
* Go to the /admin page and select **Create Links** and run:
  * **Denormalise taxa** (~8h)
  * **Build link identifiers** (~7h) (not sure if this is necessary)
  * **Build search and suggest weights** (~2:15h)
  * **Build solr suggestion index** (~15min - the application will throw a read timeout exception but indexing will continue to run on Solr)
