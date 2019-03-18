```bash
az storage directory create --name osubenchmarks --share-name fileshare --account-name mesnardostorage
az storage file upload --account-name mesnardostorage --share-name fileshare --source run-osu.sh --path osubenchmarks/run-osu.sh
../../../misc/shipyard-driver.sh
mkdir output
az storage file download-batch --source fileshare/osubenchmarks --destination output --account-name mesnardostorage
az-storage-directory-delete --name osubenchmarks --share-name fileshare --account-name mesnardostorage
```
