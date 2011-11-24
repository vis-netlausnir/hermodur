import logging

from os import path as op
from tornadio2 import SocketConnection
from stormed import Connection


ROOT = op.normpath(op.dirname(__file__))

logging.getLogger().setLevel(logging.DEBUG)


class HermodurConnection(SocketConnection):

    # Class level variable
    channel = None
    connection = None

    @classmethod
    def setup_connection(cls, host='localhost', port=5672, username='guest', password='guest', vhost='/'):
        """Sets up the connection to the AMQP host."""
        logging.debug('Setting up connection')
        cls.connection = Connection(
            host=host,
            port=port,
            username=username,
            password=password,
            vhost=vhost)
        logging.debug('Making the connection')
        cls.connection.connect(cls.on_connect)
        logging.debug('Connection made')

    @classmethod
    def on_connect(cls):
        """Sets up a channel for the connection."""
        logging.info('AMQP connection established')
        cls.channel = cls.connection.channel()

    def on_open(self, *args, **kwargs):
        """Declares a queue for the client when socket.io connection is made."""
        logging.info('Client connection opened')
        self.send('Hermodur welcomes you.')
        self.channel.queue_declare(exclusive=True,
            callback=self.on_queue_declare)

    def on_message(self, msg):
        """
        Decodes exchange and routing key from submitted JSON. If successful
        then binding and consumption based on parameters is initiated."""
        parsed = tornado.escape.json_decode(msg)
        exchange = parsed['exchange']
        routing_key = parsed['routing_key']
        self.channel.queue_bind(
            exchange=exchange,
            routing_key=routing_key,
            queue=self.qinfo.queue
        )
        logging.info('Consuming on %s for %s:%s' % (
            self.qinfo.queue,
            exchange,
            routing_key
        ))
        self.channel.consume(self.qinfo.queue, self.on_amqp_message,
            no_ack=True)

    def on_close(self):
        """Tries to delete the queue set up for the channel."""
        logging.info('Client connection closed')
        self.channel.queue_delete(self.qinfo.queue)
        # self.warning('Unable to delete queue %s' % self.qinfo.queue)

    def on_queue_declare(self, qinfo):
        """Stores queue information on successful queue declaration"""
        logging.info('AMQP queue declared %r' % qinfo.queue)
        self.qinfo = qinfo

    def on_amqp_message(self, msg):
        """
        Sends the received AMQP message along with routing key to client as
        JSON.
        """
        self.send(tornado.escape.json_encode({
            'routing_key': msg.rx_data.routing_key,
            'message': msg.body
        }))
