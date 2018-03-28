![rsynco](https://bytebucket.org/centurix/rsynco/raw/9bd6b2f693cf39b4b50d195612277583a8ae32af/assets/logo/rsynco_600x133.png?token=9c32fec74cecc6749ec1a2f5bee55f02d415e6be)

Web based rsync management tool

This project aims to be a comprehensive rsync management tool for systems where data has to be transferred using rsync on a regular basis. Using this tool you can:

* Setup rsync jobs with schedules
* Create lists of remote hosts
* Use the built in SSH configuration for remote hosts
* Start/Stop/Pause rsync tasks
* Monitor rsync transfer statuses
* Monitor overall rsync transfer progress
* Monitor rsync transfer speed between systems
* Run rsync tasks asyncronously
* Monitor multiple computers with a single rsynco activity screen
* Provide transfer statuses to various monitoring tools like Splunk
* Provide a REST API for controlling rsync jobs

**Todo**
* Improve the scheduler
* Add auth
* Test coverage
* Blueprint the API

**Python package requirements**

```
configobj
cherrypy
jsonschema
schedule
psutil (Which requires compiling on CentOS, so you'll need gcc, python-devel)
```

**Building**

```
cd web
npm install
npm run build
```
