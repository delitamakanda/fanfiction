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
