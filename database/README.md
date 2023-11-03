# Database

A Database of JSON files for all OS info will describe the signatures of every OS and its versions.
There are several types of signatures, TCP sig, MTU sig, and HTTP sig. Each JSON file will include every known signature of every OS there is.

The following format will be used to all OS types
``` json
{
  "os-type": {
    "tcp": { "signature-list" },
    "mtu": { "signature-list" },
    "http": { "signature-list" },
  }
}
```

Each signature will have the following format 
* mtu sig  = link | mtu
* tcp sig  = version | ttl | options-len | mss | windwos-size, scale | options | flags | payload
* http sig = version | 
