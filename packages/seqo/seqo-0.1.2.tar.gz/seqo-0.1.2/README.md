# seqo
**A Python package to map strings and numbers sequentially.**  
Easily generate and index custom base-N strings from a given character set.
## Installation

![Publish](https://github.com/enzoconejero/seqo/actions/workflows/deploy-pypi.yml/badge.svg)


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install seqo.
```shell script
pip install seqo
```

## Usage  

```python
from seqo import SequentialString

# Create an instance with a custom character set
ss = SequentialString("ABC")

# Check the character set
print(ss.charset)
# Output: ['A', 'B', 'C']

# Generate the first 10 strings in sequence
sequence = [ss.get(n) for n in range(10)]
print(sequence)
# Output: ['A', 'B', 'C', 'AA', 'AB', 'AC', 'BA', 'BB', 'BC', 'CA']

# Get the numeric index of a string
print(ss.index_of("CABA"))  # Output: 96

# Get the string at a specific index
print(ss.get(96))           # Output: 'CABA'

# Generate all strings between two values
start = "AA"
end = "CC"

strings_between = [
    ss.get(n)
    for n in range(ss.index_of(start), ss.index_of(end))
]

print(strings_between)
# Output: ['AB', 'AC', 'BA', 'BB', 'BC', 'CA', 'CB']
```

## Contributing
Pull requests are welcome!  
For major changes, please open an issue first to discuss what you'd like to change or add.


## License
Distributed under the [GNU GPLv3 License](https://choosealicense.com/licenses/gpl-3.0/).  
See LICENSE for more information.