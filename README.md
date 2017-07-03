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

For each browser to move in */usr/local/bin* directory
* geckodriver
* chromedriver
* ...

## Manual process

1. Initialize the display framebuffer ``Xvfb :99 -ac &`` (we have to be root)
2. Export the Display ``export DISPLAY=:99.0``
3. Enable access to the DISPLAY ``xhost +``

## Mplayer

``` sh
$ livestreamer https://www.youtube.com/watch?v=rq4na2o3aCM  360p -v -p mplayer --http-proxy http://127.0.0.1:8080 --https-proxy http://127.0.0.1:8080 --http-no-ssl-verify
```
