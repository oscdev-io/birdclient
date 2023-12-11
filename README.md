[![pipeline status](https://gitlab.oscdev.io/software/birdclient/badges/master/pipeline.svg)](https://gitlab.oscdev.io/software/birdclient/commits/master)
[![coverage report](https://gitlab.oscdev.io/software/birdclient/badges/master/coverage.svg)](https://gitlab.oscdev.io/software/birdclient/commits/master)

# Python BIRD Client

The `birdclient` Python package provides a BIRD client implemented in Python.

## BIRD Configuration

BIRD must be configured with the below ISO timestamp format...
```
timeformat base iso long;
timeformat log iso long;
timeformat protocol iso long;
timeformat route iso long;
```

