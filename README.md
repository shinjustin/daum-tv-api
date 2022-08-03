# Daum TV API

**Daum TV API** is an unofficial daum.net API for Korean TV show metadata.

It is written in Python 3.

## Overview

### Tutorial

```python3
>>> import dta
>>> query = '<query_string>'
>>> show = dta.search(query)
>>> show['program']['title']
'<query_string>'
```

### Structure

The object tree is structured as followed:

```
- program:
    - title: <string>
    - about: <string>
    - is_airing: <boolean>
    - poster: <string>
    - websites:
        name: <string>
        url: <string>
- episode_list:
    - date: <datetime>
    - id: <string>
    - text_name: <string>
    - text_date: <string>
- cast_list:
    - name: <string>
    - role: <string>
    - img: <string>
- crew_list:
    - name: <string>
    - role: <string>
    - img: <string>
```

## Prerequisites

### Dependencies

- python3
- pip3
- BeautifulSoup4
- requests

### Python Virtual Environment

Here is a brief tutorial to set up a virtual environment:

Clone the repository and enter the new directory:

```bash
git clone https://github.com/shinjustin/daum_tv_api
```

```bash
cd daum_tv_api
```

Install `virtualenv`:

```bash
pip install virtualenv
```

Create a new virtual environment:
```bash
virtualenv venv
```

Activate the new environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Disclaimer

This project and its creators are not, in any way, affiliated with daum.net or its owner, Kakao Corp.
