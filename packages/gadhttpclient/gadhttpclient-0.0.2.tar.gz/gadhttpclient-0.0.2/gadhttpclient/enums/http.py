from enum import Enum


class HTTPMethod(str, Enum):
    get = "get"
    post = "post"
    put = "put"
    patch = "patch"
    delete = "delete"


class HTTPContentType(str, Enum):
    json = "application/json"
    form = "application/x-www-form-urlencoded"
    multipart = "multipart/form-data"
    octet = "application/octet-stream"
    pdf = "application/pdf"
    zip = "application/zip"
    gzip = "application/gzip"
    tar = "application/x-tar"
    xml = "application/xml"

    plain = "text/plain"
    html = "text/html"
    csv = "text/csv"

    png = "image/png"
    jpeg = "image/jpeg"
    gif = "image/gif"
    bmp = "image/bmp"
    svg = "image/svg+xml"
    webp = "image/webp"


class HTTPAttribute(str, Enum):
    header = "header"
    query = "query"
    path = "path"
    cookie = "cookie"
    body = "body"
