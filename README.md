# godoist
Could have been called Tithub or Tidbits. Maybe we change later :rofl:

This application was not created by, affiliated with, or supported by Doist.

# Creating the environment
We are currently using python3.7 with conda. You can create the environment using the following commands:
```
conda env create -f environment.yml
```

# Github Api Documentation
- Rest API
https://developer.github.com/v3/
- GraphQL
https://developer.github.com/v4/

# Todoist Api Documentation
https://developer.todoist.com/rest/v8/#overview


# Running scripts
To run some of the scripts, you will need API tokens. Later, we will address whether we want to do 
nice and fancy things for this, but for now I opted for a `config.py` file. `config.py` is in the 
`.gitignore` file, you will have to make it locally. You can see what keys are expected in the 
`config_example.py` file.
