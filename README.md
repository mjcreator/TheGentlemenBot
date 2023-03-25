# TheGentlemenBot
Repository for my discord test bot

## Requirements
- python3
- python3-venv

## Setting up
To use, set up a virtural enviroment
`python3 -m venv bot-env`

Then inside the enviroment install the bot requirements
`pip install -r requirements.txt`

Create the bot config.py file
```python
client_id = '<APPLICATION_CLIENT_ID>'
token = '<TOKEN_HERE>'

testServers = []

cogs = [
    'cogs.suggestions',
]

#logging settings
logFile = "log.log"
logSize = 64 * 1024 * 1024
logBackupCount = 5
```

Then run
`python3 run.py`
