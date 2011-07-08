import logging
import tornado.escape
import tornado.websocket

from tornado.options import options
from stormed import Connection


class AMQPHandler(tornado.websocket.WebSocketHandler):

    channel = None
    logger = logging.getLogger('amqp_handler')
    
    @classmethod
    def setup_connection(cls):
        cls.connection = Connection(
            host=options.amqp_host,
            port=options.amqp_port,
            username=options.amqp_username,
            password=options.amqp_password,
            vhost=options.amqp_vhost)
        cls.connection.connect(cls.on_connect)

    @classmethod
    def on_connect(cls):
        cls.logger.info("AMQP connection established")
        cls.channel = cls.connection.channel()

    def open(self):
        self.logger.info("WebSocket connection opened from %s" % self.request.remote_ip)
        if self.channel:
            self.channel.queue_declare(exclusive=True, callback=self.on_queue_declare)
        else:
            raise RuntimeError("AMQP channel not established")
    
    def on_amqp_message(self, msg):
        self.logger.info(
            "AMQP got message '%r' for '%r'" %\
                (msg.body, msg.rx_data.routing_key)
        )
        try:
            self.write_message("%s,%s" % (msg.rx_data.routing_key, msg.body))
        except:
            self.close()
    
    def on_queue_declare(self, qinfo):
        self.logger.info("AMQP queue declared %r" % qinfo.queue)
        self.qinfo = qinfo
        try:
            self.write_message("Queue Declared")
        except:
            self.close()

    def on_message(self, msg):
        self.logger.info("WebSocket got message %r", msg)
        try:
            parsed = tornado.escape.json_decode(msg)
            self.logger.info("AMQP binding to exchange:'%s' with key:'%s'", parsed['exc'], parsed['key'])
            if self.channel:
                self.channel.queue_bind(
                    exchange=parsed['exc'],
                    queue=self.qinfo.queue,
                    routing_key=parsed['key']
                )
                self.channel.consume(self.qinfo.queue, self.on_amqp_message, no_ack=True)
            else:
                raise RuntimeError("AMQP channel not established")
        except:
            self.close()

    def on_close(self):
        if self.channel and self.qinfo:
            self.channel.queue_delete(self.qinfo.queue)
        self.logger.info("WebSocket connection closed to %s" % self.request.remote_ip)
