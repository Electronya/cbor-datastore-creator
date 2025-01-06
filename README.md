# cbor-datastore-encoder
CBOR datastore binary encoder

![test](https://github.com/Electronya/cbor-datastore-creator/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/Electronya/cbor-datastore-creator/graph/badge.svg?token=BNR4z8iMQ7)](https://codecov.io/gh/Electronya/cbor-datastore-creator)

## Development
### Setup
```sh
git clone git@github.com:Electronya/cbor-datastore-creator.git
cd cbor-datastore-creator
python3 -m venv .venv
source .venv/bin/activate
```

### Running the Application
```sh
# Running without debug log
python ./src/app

# Running with debug log
python ./src/app -v [component1],[component2]...
```

### Running Test
```sh
# Run all tests
pytest

# Run a specific test
pytest testSuite.py::testcase

# Run coverage
pytest --cov --cov-report=html
```
