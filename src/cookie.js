export default function get_cookie(name) {
    var value;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function (c) {
            var m = c.trim().match(/(\w+)=(.*)/);

            if(m !== undefined && m[1] == name) {
                value = decodeURIComponent(m[2]);
            }
        });
    }
    return value;
}
