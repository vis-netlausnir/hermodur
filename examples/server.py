from tornado import web

from tornadio2 import TornadioRouter, SocketServer
from hermodur import HermodurConnection


class SocketIOHandler(web.RequestHandler):
    def get(self):
        self.render('../socket.io.js')

# We use the defaults localhost:5672 and guest:guest on vhost '/'
HermodurConnection.setup_connection()

# Use the routes classmethod to build the correct resource
HermodurRouter = TornadioRouter(HermodurConnection)

# configure the Tornado application
application = web.Application(
	HermodurRouter.urls,
	socket_io_port = 8001
)

if __name__ == '__main__':
	import logging
	logging.getLogger().setLevel(logging.DEBUG)

	# Create and start tornadio server
	SocketServer(application)
