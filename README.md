# fanfiction

> A fanfic application in vue.js and django

[ ![Codeship Status for delitamakanda/fanfiction](https://app.codeship.com/projects/d6c35540-39a2-0136-2546-36a36e9263f1/status?branch=master)](https://app.codeship.com/projects/289961)

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
