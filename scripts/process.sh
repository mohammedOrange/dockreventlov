#!/bin/bash

# URL="https://192.168.49.49:644443"
URL=" -k https://192.168.0.2:4443"

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
    IFS=';' read -r -a array <<< "$1"

    video="${array[0]}"
    browser="${array[1]}"
    duration="${array[2]}"

    echo $video
    echo $browser
    echo $duration
    # Start the MITM process
    #start_mitm

    # Start the Selenium process
    #start_selenium $video $browser $duration

    # Wait the send process of Selenium
    #sleep 10

    # Stop the MITM process
    #stop_mitm
}

function getlocal_ipaddress()
{
    IP_address=$(ip route |awk '$1 !~/default/ { print $NF}')
    echo $IP_address 
}

function getpublic_ipaddress()
{
    IP_address=$(curl ipinfo.io/ip)
    echo $IP_address
}

function get_uptime()
{
    uptime=$(stat -c %Z /proc/)
    echo $uptime
}

function get_macaddress()
{
    interface=$(ip route show default | awk '/default/ {print $5}')
    macaddress=$(cat /sys/class/net/$interface/address)
    echo $macaddress
}

function get_ipdns()
{
    list_ipdns=$(cat /etc/resolv.conf | awk ' 
    BEGIN { result="" } 
    $1 ~ /nameserver/ { 
        if ( result !="" ){ 
            result = result ";" $2; 
        } else { 
            result = $2; 
        }
    } 
    END { print result }')

    echo $list_ipdns
}

function run()
{

    data="name=$HOSTNAME"
    data="$data&intip=$(getlocal_ipaddress)"
    data="$data&extip=$(getpublic_ipaddress)"
    data="$data&dns=$(get_ipdns)"
    data="$data&uptime=$(get_uptime)"
    data="$data&macaddress=$(get_macaddress)"
    data="$data&version=1.0"



    #curl_result=$(curl -s --data $data $URL/sdpweatherAPI/getvideo.php)
    echo "curl --data $data $URL/sdpweatherapi/getvideo.php"
    curl_result=$(curl --data $data $URL/sdpweatherapi/getvideo.php)

    #echo $curl_result
    read_file $curl_result
}

# Start the Main Process
run
