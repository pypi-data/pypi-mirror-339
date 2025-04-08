"""
Just for ping

When you use a free service to host your Discord bot (or anything else) that
service may require activity for keeping your bot alive, this is where
"justforping" comes in, no need for extra packages (like flask and fastapi)
for just "uptimerobot" to ping your app for keeping your app alive.

No extra resource usage just for keeping your bot/app alive 24/7
"""

from wsgiref.simple_server import make_server, WSGIServer


def justforping_wsgi_app(environ, start_response):
    """
    WSGI web application just made for pinging
    """

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    return ["%s: %s" % (key, environ[key]).encode("utf-8") for key in environ]


def make_justforping_server(host: str, port: int) -> WSGIServer:
    """Make a WSGI JustForPing server

    Args:
        host (str): Server IP address
        port (int): Server TCP port

    Returns:
        WSGIServer: A WSGI server based on http.server
    """

    return make_server(host, port, justforping_wsgi_app)


def make_and_serve_justforping_server(host: str, port: int) -> None:
    """Make a WSGI JustForPing server and make it serve forever

    Args:
        host (str): Server IP address
        port (int): Server TCP port
    """

    server = make_justforping_server(host, port)

    server.serve_forever()

