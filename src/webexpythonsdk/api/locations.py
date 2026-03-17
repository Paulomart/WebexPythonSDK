"""Webex Locations API wrapper.

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
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ..generator_containers import generator_container
from ..exceptions import ApiError
from ..restsession import RestSession
from ..utils import check_type, dict_from_items_with_values


API_ENDPOINT = "locations"
OBJECT_TYPE = "location"
FLOOR_OBJECT_TYPE = "location_floor"


class LocationsAPI(object):
    """Webex Locations API.

    Wraps the Webex Locations API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session, object_factory):
        """Init a new LocationsAPI object with RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)
        super(LocationsAPI, self).__init__()
        self._session = session
        self._object_factory = object_factory

    @staticmethod
    def _location_endpoint(locationId):
        """Build endpoint for location-specific operations."""
        return API_ENDPOINT + "/" + locationId

    @staticmethod
    def _floors_endpoint(locationId):
        """Build endpoint for floor operations."""
        return API_ENDPOINT + "/" + locationId + "/floors"

    @generator_container
    def list(
        self,
        name=None,
        id=None,
        orgId=None,
        max=None,
        **request_parameters,
    ):
        """List locations in your organization.

        Args:
            name(str): List locations matching a location name.
            id(str): List locations by ID.
            orgId(str): List locations for a specific organization.
            max(int): Limit the maximum number of items returned from the
                Webex service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields the locations returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(name, str, optional=True)
        check_type(id, str, optional=True)
        check_type(orgId, str, optional=True)
        check_type(max, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            name=name,
            id=id,
            orgId=orgId,
            max=max,
        )

        # API request - get items
        items = self._session.get_items(API_ENDPOINT, params=params)

        # Yield location objects created from the returned JSON objects
        for item in items:
            yield self._object_factory(OBJECT_TYPE, item)

    def get(self, locationId, orgId=None, **request_parameters):
        """Get location details, by ID.

        Args:
            locationId(str): The location ID.
            orgId(str): The organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Location: A Location object with the details of the requested
            location.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(orgId, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
        )

        # API request
        json_data = self._session.get(
            self._location_endpoint(locationId), params=params
        )

        # Return a location object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def create(
        self,
        name,
        timeZone,
        preferredLanguage,
        announcementLanguage,
        address,
        orgId=None,
        latitude=None,
        longitude=None,
        notes=None,
        **request_parameters,
    ):
        """Create a location.

        Args:
            name(str): The location name.
            timeZone(str): Time zone associated with this location.
            preferredLanguage(str): Preferred language of the location.
            announcementLanguage(str): Announcement language of the location.
            address(dict): The location address.
            orgId(str): The organization ID.
            latitude(str): Latitude value of the location.
            longitude(str): Longitude value of the location.
            notes(str): Notes associated with the location.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            Location: A Location object with the details of the created
            location.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(name, str)
        check_type(timeZone, str)
        check_type(preferredLanguage, str)
        check_type(announcementLanguage, str)
        check_type(address, dict)
        check_type(orgId, str, optional=True)
        check_type(latitude, str, optional=True)
        check_type(longitude, str, optional=True)
        check_type(notes, str, optional=True)

        params = dict_from_items_with_values(orgId=orgId)

        post_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            timeZone=timeZone,
            preferredLanguage=preferredLanguage,
            announcementLanguage=announcementLanguage,
            address=address,
            latitude=latitude,
            longitude=longitude,
            notes=notes,
        )

        # API request
        json_data = self._session.post(
            API_ENDPOINT, params=params, json=post_data, erc=201
        )

        # Return a location object created from the returned JSON object
        return self._object_factory(OBJECT_TYPE, json_data)

    def update(
        self,
        locationId,
        name=None,
        timeZone=None,
        preferredLanguage=None,
        address=None,
        orgId=None,
        **request_parameters,
    ):
        """Update location details, by ID.

        Args:
            locationId(str): The location ID.
            name(str): The location name.
            timeZone(str): Time zone associated with this location.
            preferredLanguage(str): Preferred language of the location.
            address(dict): The location address.
            orgId(str): The organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(name, str, optional=True)
        check_type(timeZone, str, optional=True)
        check_type(preferredLanguage, str, optional=True)
        check_type(address, dict, optional=True)
        check_type(orgId, str, optional=True)

        params = dict_from_items_with_values(orgId=orgId)

        put_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            timeZone=timeZone,
            preferredLanguage=preferredLanguage,
            address=address,
        )

        # API request
        # The endpoint has been observed to return either 204 (no body) or
        # 200 (with body) depending on backend behavior. Accept both.
        try:
            self._session.request(
                "PUT",
                self._location_endpoint(locationId),
                erc=204,
                params=params,
                json=put_data,
            )
        except ApiError as e:
            if e.status_code != 200:
                raise

    def delete(self, locationId, orgId=None, **request_parameters):
        """Delete a location, by ID.

        Args:
            locationId(str): The location ID.
            orgId(str): The organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(orgId, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
        )

        # API request
        self._session.delete(
            self._location_endpoint(locationId), params=params
        )

    @generator_container
    def list_floors(self, locationId, **request_parameters):
        """List floors for a location.

        Args:
            locationId(str): The location ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
            yields location floors returned by the Webex query.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)

        # API request - get items
        items = self._session.get_items(
            self._floors_endpoint(locationId), params=request_parameters
        )

        # Yield floor objects created from the returned JSON objects
        for item in items:
            yield self._object_factory(FLOOR_OBJECT_TYPE, item)

    def get_floor(self, locationId, floorId):
        """Get floor details for a location.

        Args:
            locationId(str): The location ID.
            floorId(str): The floor ID.

        Returns:
            LocationFloor: A LocationFloor object with the requested floor
            details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(floorId, str)

        # API request
        json_data = self._session.get(
            self._floors_endpoint(locationId) + "/" + floorId
        )

        # Return a floor object created from the returned JSON object
        return self._object_factory(FLOOR_OBJECT_TYPE, json_data)

    def create_floor(
        self, locationId, floorNumber, displayName=None, **request_parameters
    ):
        """Create a floor for a location.

        Args:
            locationId(str): The location ID.
            floorNumber(int): The floor number.
            displayName(str): Display name for the floor.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            LocationFloor: A LocationFloor object with the details of the
            created floor.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(floorNumber, int)
        check_type(displayName, str, optional=True)

        post_data = dict_from_items_with_values(
            request_parameters,
            floorNumber=floorNumber,
            displayName=displayName,
        )

        # API request
        json_data = self._session.post(
            self._floors_endpoint(locationId), json=post_data, erc=201
        )

        # Return a floor object created from the returned JSON object
        return self._object_factory(FLOOR_OBJECT_TYPE, json_data)

    def update_floor(
        self,
        locationId,
        floorId,
        floorNumber,
        displayName=None,
        **request_parameters,
    ):
        """Update floor details for a location.

        Args:
            locationId(str): The location ID.
            floorId(str): The floor ID.
            floorNumber(int): The floor number.
            displayName(str): Display name for the floor.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            LocationFloor: A LocationFloor object with the updated floor
            details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(floorId, str)
        check_type(floorNumber, int)
        check_type(displayName, str, optional=True)

        put_data = dict_from_items_with_values(
            request_parameters,
            floorNumber=floorNumber,
            displayName=displayName,
        )

        # API request
        json_data = self._session.put(
            self._floors_endpoint(locationId) + "/" + floorId,
            json=put_data,
        )

        # Return a floor object created from the returned JSON object
        return self._object_factory(FLOOR_OBJECT_TYPE, json_data)

    def delete_floor(self, locationId, floorId):
        """Delete a floor from a location.

        Args:
            locationId(str): The location ID.
            floorId(str): The floor ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(floorId, str)

        # API request
        self._session.delete(self._floors_endpoint(locationId) + "/" + floorId)
