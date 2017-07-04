#!/bin/bash

# URL="https://192.168.49.49:644443"
URL="https://192.168.0.2:4443"

function start_selenium()
{
    # python3 YoutubeSelenium.py firefox https://www.youtube.com/watch?v=ACsBt3dZzdk 10
    python3 YoutubeSelenium.py $1 $2 $3
}

function start_mitm()
{
    # Start the MITM process
    mitmdump -s ../script_mitm.py > /dev/null 2>&1 &
    export mitmpid
    mitmpid=$!
}

function stop_mitm()
{
    # Stop the MITM process
    kill $mitmpid
}

function read_file()
{
    FS=';' read -r -a array <<< "$1"

    machineid="${array[0]}"
    video="${array[1]}"
    browser="${array[2]}"
    duration="${array[3]}"

    if [ ! -f "/var/cache/machineid" ]
    then
        echo "$machineid" > /var/cache/machineid
    fi

    # Start the MITM process
    start_mitm

    # Start the Selenium process
    start_selenium $video $browser $duration

    # Wait the send process of Selenium
    sleep 10

    # Stop the MITM process
    stop_mitm
}

function send_data()
{
    if [ -f "/var/cache/machineid" ]
    then
        MACHINEID=$(cat /var/cache/machineid)
    else
        MACHINEID=""
    fi 

    export machineid

    data="name=$HOSTNAME"
    data="$data&machineid=$MACHINEID"

    curl_result=$(curl -s --data $data $URL/sdpweatherAPI/getvideo.php)

    read_file $curl_result
}
