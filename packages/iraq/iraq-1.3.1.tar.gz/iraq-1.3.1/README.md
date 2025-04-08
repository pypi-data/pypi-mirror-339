# akm - Gmail Temporary API Client

This Python library allows you to generate temporary Gmail addresses and check for new messages .

## Installation

To install this package, simply :
```bash
pip install akm```

run - (1) :
```python
akm.gen(EmailType=2)
```
run - (2) :
```python
akm.message(EmailCheck='<email>')
```
run - (3) :
```python
akm.message(EmailCheck='<email>',whileTrue=True)
```