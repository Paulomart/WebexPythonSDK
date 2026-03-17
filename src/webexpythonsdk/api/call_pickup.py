"""Webex Features: Call Pickup API wrapper.

Copyright (c) 2016-2024 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ..restsession import RestSession
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


API_ENDPOINT = "features/callPickup"
OBJECT_TYPE = "call_pickup"


class CallPickupAPI(object):
    """Webex Features: Call Pickup API.

    Wraps the Webex Calling Call Pickup API and exposes the API as native
    Python methods that return native Python objects.
    See: https://developer.webex.com/calling/docs/api/v1/features-call-pickup
    """

    def __init__(self, session, object_factory):
        """Initialize a new CallPickupAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.
            object_factory(callable): The factory function to use to create
                Python objects from the returned Webex JSON data objects.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(CallPickupAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    def create(
        self,
        org_id,
        location_id,
        name,
        extension,
        **request_parameters,
    ):
        """Create a call pickup (call pickup group).

        Creates a new call pickup group for the given organization and location.
        See: https://developer.webex.com/calling/docs/api/v1/features-call-pickup/
        create-a-call-pickup

        Args:
            org_id(str): The ID of the organization.
            location_id(str): The ID of the location for the call pickup group.
            name(str): A user-friendly name for the call pickup group.
            extension(str): The extension for the call pickup group.
            **request_parameters: Additional request body parameters (e.g.
                members, etc.).

        Returns:
            ImmutableData: The created call pickup object.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(org_id, str)
        check_type(location_id, str)
        check_type(name, str)
        check_type(extension, str)

        post_data = dict_from_items_with_values(
            request_parameters,
            orgId=org_id,
            locationId=location_id,
            name=name,
            extension=extension,
        )

        json_data = self._session.post(API_ENDPOINT, json=post_data)

        return self._object_factory(OBJECT_TYPE, json_data)
