# sample scripts fro creating config and batch starting a watchfolder


### create-watchfolder-config.sh
#### Usage
- edit the defaults VARs in top of file for source ftp and dest ftp

#### Run

``` 
sh  create-watchfolder-config.sh -i or_id -p y -o config.yaml

```

#### opts:

  -p read mets for dest path y to enable
  
  -i the org id
  
  -o the output file path for config.yml

### run_watchers_from_csv.sh

```
sh run_watchers_from_csv.sh

```

### config
 - create a csv file with or-id,y/n `orgs.csv`
 
```
OR-4x54g1p,y
OR-154dn75,y
OR-z31nn3s,y
OR-v97zq9j,n
OR-gh9b857,y
OR-3x83k1b,y
OR-1j9772n,y
OR-0z70w1b,y
 ```
#### Description

- creates a dir with OR_ID pust a config in it 

- starts the watchfolder from this dir

- record PID in scriptdir PID.pid eg `OR-z31nn3s.pid`

- daemon, keeps running

- kill all pids when hitting ctrl +c 

## NOTES


Use this script to make a systemd unit file

