
**Note on data format**: The flight segmentation data is provided in YAML files. YAML is a text based
human readable data format that uses python-like indentation for structuring its contents. It is often used for configuration
files and due to its great human readability very suited for version control, which is one reason we wanted to use it here.
For python users, the module [PyYAML](https://pyyaml.org) (included in Anaconda)
offers an easy to use way to read the data from the yaml files into plane python objects like lists and dictionaries.
Here is an example to read a file and print the circle start and end times from that file:

```
import yaml
flightinfo = yaml.load(open("HALO_RF04_20200126_info.yaml"))
print([(c["start"], c["end"]) for c in flightinfo["segments"] if "circle" in c["kinds"]])
```
