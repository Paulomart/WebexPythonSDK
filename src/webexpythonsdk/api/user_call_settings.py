"""Webex User Call Settings API wrapper.

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
from ..utils import check_type, dict_from_items_with_values


OBJECT_TYPE = "shared_line_appearance_members"


class UserCallSettingsAPI(object):
    """Webex User Call Settings API.

    Wraps the Webex Calling User Call Settings API and exposes the API as
    native Python methods that return native Python objects.
    See: https://developer.webex.com/calling/docs/api/v1/user-call-settings-2-2
    """

    def __init__(self, session, object_factory):
        """Initialize a new UserCallSettingsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.
            object_factory(callable): The factory function to use to create
                Python objects from the returned Webex JSON data objects.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(UserCallSettingsAPI, self).__init__()

        self._session = session
        self._object_factory = object_factory

    def get_shared_line_appearance_members_new(
        self,
        person_id,
        **request_parameters,
    ):
        """Get shared-line appearance members (new).

        Retrieves the shared-line appearance members for a person.
        See: https://developer.webex.com/calling/docs/api/v1/user-call-settings-2-2/
        get-shared-line-appearance-members-new

        Args:
            person_id(str): The ID of the person (user).
            **request_parameters: Additional query parameters (e.g. orgId).

        Returns:
            ImmutableData: The response object (e.g. with members list).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(person_id, str)

        url = "people/{}/features/sharedLineAppearance/members".format(
            person_id
        )

        json_data = self._session.get(url, params=request_parameters)

        return self._object_factory(OBJECT_TYPE, json_data)

    def put_shared_line_appearance_members_new(
        self,
        person_id,
        **request_parameters,
    ):
        """Put (update) shared-line appearance members (new).

        Updates the shared-line appearance members for a person.
        See: https://developer.webex.com/calling/docs/api/v1/user-call-settings-2-2/
        put-shared-line-appearance-members-new

        Args:
            person_id(str): The ID of the person (user).
            **request_parameters: Request body parameters (e.g. members).

        Returns:
            ImmutableData: The response object.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(person_id, str)

        url = "people/{}/features/sharedLineAppearance/members".format(
            person_id
        )

        put_data = dict_from_items_with_values(request_parameters)

        json_data = self._session.put(url, json=put_data)

        return self._object_factory(OBJECT_TYPE, json_data)
