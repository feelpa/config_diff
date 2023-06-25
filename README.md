# config_diff
Script that rearranges the contents of two fortigate firewall configuration files so you can do an easy-to-read `diff`.
## usage
```
python main.py -o OLD_FILE_PATH -n NEW_FILE_PATH
```
The newly generated files will be saved in the source file folder.