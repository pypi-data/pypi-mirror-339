# Thumbor HTTP Loader Prefix

Add a prefix to the HTTP Loader so that you don't have to pass the entire URL

## Installation

```bash
# master branch
pip install -e git+https://github.com/jcord04/thumbor-http-load-prefix.git@master#egg=tc_http_loader_prefix

# latest stable
pip install tc_http_loader_prefix
```

## Running Test
in the project root, run 

```pytest```

## Configuration

```python
# thumbor.conf
LOADER = 'tc_http_loader_prefix.loader'

TC_HTTP_LOADER_PREFIX = 'https://your-domain/'

# When making a request like this
https://domain.example/unsafe/400x400/image.jpg

#The image is fetched from 
https://your-domain/image.jpg

```