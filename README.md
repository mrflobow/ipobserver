# IPObserver
A Daemon Services to update the Public IP of your A Records in Digital Ocean.

## Build Instruction

> docker build . -t mrflobow/ipobserver:0.1 --platform linux/amd64

## Docker Environment Variables

```
API_TOKEN - Digital Ocean API Key
DOMAIN - Your Domain in Digital Ocean
SUBDOMAINS - A list of subdomains (optional) 
INTERVAL_M - Interval in Minutes to check Public IP - default 5min
```

> If SUBDOMAINS is not provided @ will be used

Sample .env 
```
API_TOKEN=myapitoken_12345
DOMAIN=mydomain.com
SUBDOMAINS=@;www;vpn
```

## Limitations

Will not work at Docker Desktop on Mac. The UPNP Discovery works under Linux.
If you have a solution please contact me.