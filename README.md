# IPObserver
A Daemon Services to update the Public IP of your A Records in Digital Ocean.

## Build Instruction

> docker build . -t mrflobow/ipobserver:0.2 --platform linux/amd64

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


## Release Notes 

### 0.2 
 - Removed miniupnp dependencies. Relies now on api.ipify.org , no longer requires host mode to run.
 - Version 0.1 crashed periodically due to issues with upnp. Improved stability
### 0.1 
Initial release with miniupnp