# EmerSearch

Simple python script/lib to search Emercoin Explorer NVS records.

The script queries [Emercoin NVS Explorer](https://explorer.emercoin.com/nvs) and returns a formatted list of results.



# Usage 

```
usage: emersearch.py [-h] [--type [TYPE]] [--name [NAME]] [--value [VALUE]]
                [--page_size [PAGE_SIZE]] [--include_empty]
                [--include_invalid] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --type [TYPE]         The type of NVS records to search.
  --name [NAME]         The name to search for.
  --value [VALUE]       The value to search for.
  --page_size [PAGE_SIZE]
                        The page size for results [25, 50, 100, all]
  --include_empty       Include empty result types
  --include_invalid     Include invalid/expired results.
  -v, --verbose         Include verbose output

```

## Examples 

Query for records with a name of `emer.coin`.  

```
$ ./emersearch.py --name emer.coin
 Found 6 NVS records
Type    Name                            Value                                           Block   Expires 
dns     dns:myemer.coin                 123                                             228752  281252  
dns     dns:Emer.coin                   A=192.227.233.13|TXT=bitway.io                  150997  1900822 
dns     dns:EMER.coin                   A=192.227.233.13|TXT=bitway.io                  150983  1900808 
N/A     emer.coin                       emercoin                                        106541  1856366 
dns     dns:www.emer.coin               A=192.241.241.153|NS=NS1.DIGITALOCEAN.com,
                                        NS2.DIGIA=192.241.241.153|NS=NS1.DIGITALOCEAN.com,
                                        NS2.DIGITALOCEAN.com,NS3.DIGITALOCEAN.com65523   118023  
dns     dns:emer.coin                   A=104.238.236.163|TXT=emercoin.com              59302   1125402 

```

Query for records with a value of `192.168.0.1`

```
python src/emersearch.py --value 192.168.0.1
 Found 19 NVS records
Type    Name                            Value                                           Block   Expires 
dns     dns:cateta.coin                 A=192.168.0.1                                   382411  1021161 
dns     dns:cateta.lib                  A=192.168.0.1                                   382411  1021161 
dns     dns:cateta.eth                  A=192.168.0.1                                   382411  1021161 
dns     dns:cateta.bazar                A=192.168.0.1                                   382411  1021161 
dns     dns:cateta.emc                  A=192.168.0.1                                   382411  1021161 
dns     dns:bloco.eth                   A=192.168.0.1                                   360929  6748429 
dns     dns:bloco.bazar                 A=192.168.0.1                                   360928  6748428 
...
```


## Using as a Lib 

``` 
from emersearch import EmerSearch

es = EmerSearch()
results = es.search(name='emer.coin')

```


# Feedback / Help

There is likely a better way to do this, but I needed something quick that I could automate some simple tracking and
query the explorer results out of a Browser.  

If you have any ideas, bugs or requests please reach out. 


