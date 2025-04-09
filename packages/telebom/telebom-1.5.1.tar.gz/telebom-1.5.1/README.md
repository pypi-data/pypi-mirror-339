# r - Gmail Temporary API Client

This Python library allows you to reaction post telegram .

## Installation

To install this package , simply :
```bash
pip install telebom
```

run - (1) :
```python
import telebom
telebom.reaction(link='https://t.me/').start
```
run - (2) :
```python
import telebom
telebom.reaction(link='https://t.me/')['while=True'].start
```
run - (3) :
```python
import telebom
telebom.reaction(link='https://t.me/')['while=True']['threading=5'].start
```