from amqpstorm.compatibility import json
from amqpstorm.compatibility import quote
from amqpstorm.management.base import ManagementHandler

API_USER = 'users/%s'
API_USER_PERMISSIONS = 'users/%s/permissions'
API_USER_VIRTUAL_HOST_PERMISSIONS = 'permissions/%s/%s'
API_USERS = 'users'
API_USERS_BULK_DELETE = 'users/bulk-delete'


class User(ManagementHandler):
    def get(self, username):
        """Get User details.

        :param str username: Username

        :raises ApiError: Raises if the remote server encountered an error.
                          We also raise an exception if the user cannot
                          be found.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_USER % username)

    def list(self):
        """List all Users.

        :rtype: list
        """
        return self.http_client.get(API_USERS)

    def create(self, username, password, tags=''):
        """Create User.

        :param str username: Username
        :param str password: Password
        :param str,list tags: Comma-separate list of tags (e.g. monitoring)

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        user_payload = json.dumps({
            'password': password,
            'tags': tags
        })
        return self.http_client.put(API_USER % username,
                                    payload=user_payload)

    def delete(self, username):
        """Delete User or a list of Users.

        :param str,list username: Username or a list of Usernames

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        if isinstance(username, list):
            return self.http_client.post(
                API_USERS_BULK_DELETE,
                payload=json.dumps({'users': username})
            )
        return self.http_client.delete(API_USER % username)

    def get_permission(self, username, virtual_host):
        """Get User permissions for the configured virtual host.

        :param str username: Username
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(API_USER_VIRTUAL_HOST_PERMISSIONS %
                                    (
                                        virtual_host,
                                        username
                                    ))

    def get_permissions(self, username):
        """Get all Users permissions.

        :param str username: Username

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_USER_PERMISSIONS %
                                    (
                                        username
                                    ))

    def set_permission(self, username, virtual_host, configure_regex='.*',
                       write_regex='.*', read_regex='.*'):
        """Set User permissions for the configured virtual host.

        :param str username: Username
        :param str virtual_host: Virtual host name
        :param str configure_regex: Permission pattern for configuration
                                    operations for this user.
        :param str write_regex: Permission pattern for write operations
                                for this user.
        :param str read_regex: Permission pattern for read operations
                               for this user.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        permission_payload = json.dumps({
            "configure": configure_regex,
            "read": read_regex,
            "write": write_regex
        })
        return self.http_client.put(API_USER_VIRTUAL_HOST_PERMISSIONS %
                                    (
                                        virtual_host,
                                        username
                                    ),
                                    payload=permission_payload)

    def delete_permission(self, username, virtual_host):
        """Delete User permissions for the configured virtual host.

        :param str username: Username
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.delete(
            API_USER_VIRTUAL_HOST_PERMISSIONS %
            (
                virtual_host,
                username
            ))
