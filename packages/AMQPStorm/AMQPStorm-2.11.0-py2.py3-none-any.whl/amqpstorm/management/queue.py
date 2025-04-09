from amqpstorm.compatibility import json
from amqpstorm.compatibility import quote
from amqpstorm.management.base import ManagementHandler

API_QUEUE = 'queues/%s/%s'
API_QUEUE_BIND = 'bindings/%s/e/%s/q/%s'
API_QUEUE_BINDINGS = 'queues/%s/%s/bindings'
API_QUEUE_PURGE = 'queues/%s/%s/contents'
API_QUEUE_UNBIND = 'bindings/%s/e/%s/q/%s/%s'
API_QUEUES = 'queues'
API_QUEUES_VIRTUAL_HOST = 'queues/%s'


class Queue(ManagementHandler):
    def get(self, queue, virtual_host='/'):
        """Get Queue details.

        :param queue: Queue name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
                          We also raise an exception if the queue cannot
                          be found.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(
            API_QUEUE % (
                virtual_host,
                queue
            )
        )

    def list(self, virtual_host='/', show_all=False,
             name=None, page_size=100, use_regex=False):
        """List Queues.

        :param str virtual_host: Virtual host name
        :param bool show_all: List Queues across all virtual hosts
        :param name: Filter by name
        :param use_regex: Enables regular expression for the param name
        :param page_size: Number of elements per page

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        if show_all:
            return self.http_client.list(
                API_QUEUES,
                name=name, use_regex=use_regex, page_size=page_size,
            )
        virtual_host = quote(virtual_host, '')
        return self.http_client.list(
            API_QUEUES_VIRTUAL_HOST % virtual_host,
            name=name, use_regex=use_regex, page_size=page_size,
        )

    def declare(self, queue='', virtual_host='/', passive=False, durable=False,
                auto_delete=False, arguments=None):
        """Declare a Queue.

        :param str queue: Queue name
        :param str virtual_host: Virtual host name
        :param bool passive: Do not create
        :param bool durable: Durable queue
        :param bool auto_delete: Automatically delete when not in use
        :param dict,None arguments: Queue key/value arguments

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        if passive:
            return self.get(queue, virtual_host=virtual_host)

        queue_payload = json.dumps(
            {
                'durable': durable,
                'auto_delete': auto_delete,
                'arguments': arguments or {},
                'vhost': virtual_host
            }
        )
        return self.http_client.put(
            API_QUEUE % (
                quote(virtual_host, ''),
                queue
            ),
            payload=queue_payload)

    def delete(self, queue, virtual_host='/'):
        """Delete a Queue.

        :param str queue: Queue name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.delete(API_QUEUE %
                                       (
                                           virtual_host,
                                           queue
                                       ))

    def purge(self, queue, virtual_host='/'):
        """Purge a Queue.

        :param str queue: Queue name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.delete(API_QUEUE_PURGE %
                                       (
                                           virtual_host,
                                           queue
                                       ))

    def bindings(self, queue, virtual_host='/'):
        """Get Queue bindings.

        :param str queue: Queue name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(API_QUEUE_BINDINGS %
                                    (
                                        virtual_host,
                                        queue
                                    ))

    def bind(self, queue='', exchange='', routing_key='', virtual_host='/',
             arguments=None):
        """Bind a Queue.

        :param str queue: Queue name
        :param str exchange: Exchange name
        :param str routing_key: The routing key to use
        :param str virtual_host: Virtual host name
        :param dict,None arguments: Bind key/value arguments

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        bind_payload = json.dumps({
            'destination': queue,
            'destination_type': 'q',
            'routing_key': routing_key,
            'source': exchange,
            'arguments': arguments or {},
            'vhost': virtual_host
        })
        virtual_host = quote(virtual_host, '')
        return self.http_client.post(API_QUEUE_BIND %
                                     (
                                         virtual_host,
                                         exchange,
                                         queue
                                     ),
                                     payload=bind_payload)

    def unbind(self, queue='', exchange='', routing_key='', virtual_host='/',
               properties_key=None):
        """Unbind a Queue.

        :param str queue: Queue name
        :param str exchange: Exchange name
        :param str routing_key: The routing key to use
        :param str virtual_host: Virtual host name
        :param str properties_key:

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        unbind_payload = json.dumps({
            'destination': queue,
            'destination_type': 'q',
            'properties_key': properties_key or routing_key,
            'source': exchange,
            'vhost': virtual_host
        })
        virtual_host = quote(virtual_host, '')
        return self.http_client.delete(API_QUEUE_UNBIND %
                                       (
                                           virtual_host,
                                           exchange,
                                           queue,
                                           properties_key or routing_key
                                       ),
                                       payload=unbind_payload)
