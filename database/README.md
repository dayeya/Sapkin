# Database

A database of json files for all os info will describe the signatures of every os and its versions.
There are several types of signatures, each json file will include signatures of every os we configured.
.json file formats.
tcp.json
```json
  "os-type": ["signature-list"]
```
mtu.json
```json
  "link-type": ["signature-list"]
```
http.json
```json
  "web-server": ["signature-list"]
```

Each signature will have the following format:
* mtu sig  = link:mtu
* tcp sig  = ver:ittl:op_len:mss:win_size,scale:options:flags:payload_size
* http sig = version:headers:no-headers:desc

Credit for p0f.
