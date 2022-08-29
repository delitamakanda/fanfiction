import moment from 'moment'

export function date (value) {
  return moment(value).format('DD/MM/YYYY')
}

export function uppercase (name) {
  if (typeof name !== "string") {
    throw TypeError("name must be a string")
  }

  return name.toUpperCase()
}

export function lowercase (name) {
  if (typeof name !== "string") {
    throw TypeError("name must be a string")
  }

  return name.toLowerCase()
}

export function removeLastComma (str) {
   return str.replace(/,(\s+)?$/, '');
}

export function readMore(text, length, suffix) {
    return text.substring(0, length) + suffix;
}

export function toFixed(price, limit) {
    return price.toFixed(limit);
}

export function toEuro(price) {
    return `$${price}`;
}

export function json(value) {
    return JSON.stringify(value);
}

// extract a list of property values
export function pluck (objects, key) {
    return objects.map(function(object) {
        return object[key];
    });
}

// return the index
export function at (value, index) {
    return value[index];
}

export function min (values) {
    return Math.min(...values);
}

export function max (values) {
    return Math.max(...values);
}

export function shuffle (values) {
    for (var i = values.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = values[i];
        values[i] = values[j];
        values[j] = temp;
    }
    return values;
}

export function unique (values, unique) {
    return values.filter(function(element, index, self) {
        return index = self.indexOf(element);
    });
}

export function prepend (string, prepend) {
    return `${string}${prepend}`;
}

export function pluralize (word, amount) {
    return amount > 1 ? `${word}s` : word;
}

export function reverse (value) {
    return value.split('').reverse().join('');
}

export function filterBy(list, value) {
    return list.filter(function(item) {
        return item.indexOf(value) > -1;
  });
}

export function findBy(list, value) {
    return list.filter(function(item) {
        return item == value
    });
}
