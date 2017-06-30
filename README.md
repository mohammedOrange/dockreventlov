# dockreventlov
Dock to measure the map streaming

## Platform

![Security](/images/BasicDiagram.jpg)

## Install

* libssl-dev

All install process will be made with ```pip3```
* mitmproxy

## Mplayer

``` sh
$ livestreamer https://www.youtube.com/watch?v=rq4na2o3aCM  360p -v -p mplayer --http-proxy http://127.0.0.1:8080 --https-proxy http://127.0.0.1:8080 --http-no-ssl-verify
```
