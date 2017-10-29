## Blueprint

There are many ways to test our production and development json REST api's. 
There are various cases our api's behave differently based on our application state, A developer may want to test various cases in these apis. By combining standed http request with json schema validation provides good procedure to these apis.


## Installation

```
git clone https://github.com/sourcepirate/blueprint.git
cd blueprint

python setup.py develop

```

## Usage

```
usage: blueprint [-h] [-f FILE]

Check your api

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Checks json file

```

Using blueprint need a json config file which lists all checks to be performed against an API.

```json

{
    "cases": [
        {
            "url": "http://jsonplaceholder.typicode.com/posts/1",
            "method": "GET",
            "checks": [
                {
                    "name": "check post",
                    "description": "Tests the post structure",
                    "check": {
                        "type": "object",
                        "properties": {
                            "userId": {"type": "number"},
                            "id": {"type": "number"}
                        }
                    }
                }
            ]
        }
    ]
}

```

## License

MIT
