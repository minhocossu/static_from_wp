# static_from_wp
Generate static content from a wordpress admin

Wordpress + Python3


## Step one: run all containers

This will get up three containers: wordpress, mysql and html pure (nginx).

````
cp docker-compose.yaml-example docker-compose.yaml
docker-compose up
````

## Step two: configure wordpress

Access http://yourhost:8001 and install wordpress.

Add some content with images in order to test.

## Step three: configure your static website:

In this file you will set things like 'site_name' and other configuration texts.
```
cp conf.py-example conf.py
[edit] conf.py
```

## Step four: deploy the static website

```
python3 main.py

```
