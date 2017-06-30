# dockreventlov
Dock to measure the map streaming

## Platform

![Security](/images/BasicDiagram.jpg)

## Install

* libssl-dev
* xvfb
* x11-xserver-utils
* scrot
* python3
  * python3-pip
* firefox-esr

All install process will be made with ```pip3```
* mitmproxy
* python3-xlib
* pyautogui
* selenium
* configobj
* psutil

## Mplayer

``` sh
$ livestreamer https://www.youtube.com/watch?v=rq4na2o3aCM  360p -v -p mplayer --http-proxy http://127.0.0.1:8080 --https-proxy http://127.0.0.1:8080 --http-no-ssl-verify
```
