# My IP (TCP)
This is a yet another "get my IP" stuff on TCP socket


## Requirements
* Python 3.5+


## Start daemon
* with info logs:
    ``` sh
    python3 -m my_ip -v
    ```
* with specified listening address and debug logs:
    ``` sh
    python3 -m my_ip -vv --host 0.0.0.0 --port 7071
    ```


## Ask my IP
```sh
echo get-my-ip | nc localhost 7071
```
