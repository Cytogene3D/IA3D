
## Using a config file in python
```
import yaml
config = yaml.safe_load(open("path/to/config.yml"))
```
see https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settingsconfig-file-in-python

### Sharing a Config dictionnary between different modules
(inspired from Orca load_ressources)

- Use a module named config.py
- Define a function load_config in that module
- This load_config will be called in main()
- Within this load_config function construct a Config dictionnary defined as global (see Orca load_ressources)
- In each module in which you need to access config variables, add the following import 
```python
from config import Config
```
## Call a method based on the string corresponding to its name

see the ObjectAttributesAsString.ipynb notebook





