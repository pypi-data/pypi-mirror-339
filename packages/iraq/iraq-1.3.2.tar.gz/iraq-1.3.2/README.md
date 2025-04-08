# iraq - Gmail Temporary API Client

This Python library allows you to generate temporary Gmail addresses and check for new messages .

## Installation

To install this package, simply :
```bash
pip install iraq
```

run - (1) :
```python
iraq.gen(EmailType=2)
```
run - (2) :
```python
iraq.message(EmailCheck='<email>')
```
run - (3) :
```python
iraq.message(EmailCheck='<email>',whileTrue=True)
```