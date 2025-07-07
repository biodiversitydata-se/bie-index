# Bie-index

## Setup

Create data directory at `/data/bie-index` and populate as below (it is easiest to symlink the config files to the ones in this repo):
```
mats@xps-13:/data/bie-index$ tree
.
├── config
│   ├── bie-index-config.yml -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/bie-index-config.yml
│   ├── conservation-lists.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/conservation-lists.json
│   ├── image-lists.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/image-lists.json
│   ├── locality-keywords.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/locality-keywords.json
│   └── vernacular-lists.json -> /home/mats/src/biodiversitydata-se/bie-index/sbdi/data/config/vernacular-lists.json
└── data
    └── sitemap
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

The solr search index can be built locally from the [GBIF Backbone Taxonomy](https://www.gbif.org/dataset/d7dddbf4-2cf0-4f39-9b2a-bb099caae36c) using the [gbif-taxonomy-for-la](https://github.com/biodiversitydata-se/gbif-taxonomy-for-la) project.

* Clone the [gbif-taxonomy-for-la](https://github.com/biodiversitydata-se/gbif-taxonomy-for-la) repo
* Run (change to current date):
  ```
  ./gbif-taxonomy-for-la-docker --backbone --filter_lang=en,sv --name-authors --namematching-distri=4.3 --namematching-index --dwca 2024-02-16
  ```
* Unpack the file `target/gbif-backbone-2024-02-16.zip`
* Start bie-index locally (`make run`)
* Go to the /ws/admin page and select **DwCA Import** and import from `/home/mats/src/biodiversitydata-se/gbif-taxonomy-for-la/target/gbif-backbone-2024-02-16` (~2:15h)
* Go to the /ws/admin page and select **Create Links** and run:
  * **Denormalise taxa** (~8h)
  * **Build link identifiers** (~7h) (not sure if this is necessary)
  * **Build search and suggest weights** (~2:15h)
  * **Build solr suggestion index** (~15min - the application will throw a read timeout exception but indexing will continue to run on Solr)

### Put search index in production
Copy the `data/bie`-directory from the solr data directory to live-manager-1. It should replace the directory `/docker_nfs/var/volumes/data_bie_solr/data/bie`. Restart the `bie-index_bie-solr` service.

### Index other things
The following have been indexed directly in the production environment. Check the *Use online index* checkbox when indexing them. All processes are quite fast.
- Collectory
- Species lists
- Spatial layers
