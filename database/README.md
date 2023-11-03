# Database

A database of json files for all os info will describe the signatures of every os and its versions.
There are several types of signatures, each json file will include signatures of every os we configured.

The following format will be used to all OS types
``` json
{
  /* tcp.json file */
  "os-type": {
    "tcp-sig":  ["signature-list"],
  },

  /* mtu.json file */  
  "link-type": {
    "mtu": ["signature-list"],
  },
  
  /* http.json */
  "web-server": {
    "http": ["signature-list"]
  },
}
```

Each signature will have the following format 
* mtu sig  = link | mtu
* tcp sig  = version | ttl | options-len | mss | windwos-size, scale | options | flags | payload
* http sig = version | headers | no-headers | desc 
