# fanfiction

[![Build Status](https://travis-ci.org/delitamakanda/fanfiction.svg?branch=master)](https://travis-ci.org/delitamakanda/fanfiction)

> A fanfic application in vue.js and django

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


``` bash
# set an virtual env
virtualenv venv -p python3

source venv/bin/activate

pip install -r requirements-dev.txt

python3 manage.py migrate

python3 manage.py runserver
```

## Tests

``` bash
coverage run --source=api ---omit=*/migrations/*  manage.py test

coverage report -m
```

## Asynchronous tasks

``` bash
celery -A backend worker -l info -B
```

## Translation

```bash
django-admin makemessages --ignore=venv/*
django-admin compilemessages
```

## Recommandation engine

```bash
>>> from api.models import Fanfic
>>> fanfic_1 = Fanfic.objects.get(id=1)
>>> fanfic_2 = Fanfic.objects.get(id=2)
>>> fanfic_3 = Fanfic.objects.get(id=3)
>>> fanfic_4 = Fanfic.objects.get(id=4)
>>> from api.recommender import Recommender
>>> print(fanfic_1)
Acchi Kocchi - Ben-To Crossover
>>> print(fanfic_2)
Jusqu'à ce que la mort nous sépare...
>>> print(fanfic_3)
Nature
>>> print(fanfic_4)
Elementary
>>> r = Recommender()
>>> print(r)
<api.recommender.Recommender object at 0x10f5de1d0>
>>> r.fanfics_liked([fanfic_1, fanfic_2])
>>> r.fanfics_liked([fanfic_2, fanfic_3])
>>> r.fanfics_liked([fanfic_4, fanfic_1])
>>> r.fanfics_liked([fanfic_1, fanfic_3])
>>> r.fanfics_liked([fanfic_3, fanfic_4])
>>> r.suggest_fanfics_for([fanfic_1])
[<Fanfic: Elementary>, <Fanfic: Nature>, <Fanfic: Jusqu'à ce que la mort nous sépare...>]
>>> r.suggest_fanfics_for([fanfic_2])
[<Fanfic: Nature>, <Fanfic: Acchi Kocchi - Ben-To Crossover>]
>>> r.suggest_fanfics_for([fanfic_3])
[<Fanfic: Elementary>, <Fanfic: Jusqu'à ce que la mort nous sépare...>, <Fanfic: Acchi Kocchi - Ben-To Crossover>]
>>> r.suggest_fanfics_for([fanfic_4])
[<Fanfic: Nature>, <Fanfic: Acchi Kocchi - Ben-To Crossover>]
>>> r.suggest_fanfics_for([fanfic_4, fanfic_1])
[<Fanfic: Nature>, <Fanfic: Jusqu'à ce que la mort nous sépare...>]
>>> r.suggest_fanfics_for([fanfic_1, fanfic_2])
[<Fanfic: Nature>, <Fanfic: Elementary>]
```
