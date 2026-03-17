"""Webex Location Call Settings: Voicemail API wrapper.

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

from ..exceptions import MalformedResponse
from ..generator_containers import generator_container
from ..restsession import RestSession
from ..utils import check_type, dict_from_items_with_values


API_ENDPOINT = "telephony/config"
LOCATION_VOICEMAIL_OBJECT_TYPE = "location_voicemail"
VOICEMAIL_GROUP_OBJECT_TYPE = "location_voicemail_group"
VOICEMAIL_GROUP_CREATE_OBJECT_TYPE = "location_voicemail_group_create"
VOICE_PORTAL_OBJECT_TYPE = "location_voice_portal"
VOICE_PORTAL_PASSCODE_RULE_OBJECT_TYPE = "location_voice_portal_passcode_rule"


class LocationCallSettingsVoicemailAPI(object):
    """Webex Location Call Settings: Voicemail API.

    Wraps Webex Calling Location Voicemail settings and exposes operations as
    native Python methods.

    """

    def __init__(self, session, object_factory):
        """Init a new LocationCallSettingsVoicemailAPI object with session.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Webex service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)
        super(LocationCallSettingsVoicemailAPI, self).__init__()
        self._session = session
        self._object_factory = object_factory

    @staticmethod
    def _voicemail_groups_collection_endpoint():
        """Build endpoint for voicemail groups collection operations."""
        return API_ENDPOINT + "/voicemailGroups"

    @staticmethod
    def _location_voicemail_endpoint(locationId):
        """Build endpoint for location voicemail settings."""
        return API_ENDPOINT + "/locations/{}/voicemail".format(locationId)

    @staticmethod
    def _location_voicemail_groups_endpoint(locationId):
        """Build endpoint for location voicemail groups operations."""
        return API_ENDPOINT + "/locations/{}/voicemailGroups".format(locationId)

    @staticmethod
    def _location_voicemail_group_endpoint(locationId, voicemailGroupId):
        """Build endpoint for location voicemail group operations."""
        return (
            API_ENDPOINT
            + "/locations/{}/voicemailGroups/{}".format(
                locationId, voicemailGroupId
            )
        )

    @staticmethod
    def _location_voice_portal_endpoint(locationId):
        """Build endpoint for location voice portal operations."""
        return API_ENDPOINT + "/locations/{}/voicePortal".format(locationId)

    @staticmethod
    def _extract_list(json_data, key):
        """Extract a required list field from a JSON dictionary."""
        assert isinstance(json_data, dict)
        check_type(key, str)

        value = json_data.get(key)
        if value is None:
            error_message = "'{}' key not found in JSON data: {!r}".format(
                key, json_data
            )
            raise MalformedResponse(error_message)

        if not isinstance(value, list):
            error_message = (
                "'{}' key value is not a list in JSON data: {!r}".format(
                    key, json_data
                )
            )
            raise MalformedResponse(error_message)

        return value

    @generator_container
    def list_voicemail_groups(
        self,
        orgId=None,
        locationId=None,
        name=None,
        phoneNumber=None,
        max=None,
        start=None,
        **request_parameters,
    ):
        """Read the list of voicemail groups.

        Args:
            orgId(str): List voicemail groups for this organization.
            locationId(str): List voicemail groups for this location.
            name(str): Filter voicemail groups by name.
            phoneNumber(str): Filter voicemail groups by phone number.
            max(int): Maximum number of items to return.
            start(int): Start index for pagination.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer that yields voicemail
            group objects.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.
            MalformedResponse: If the response does not include a
                ``voicemailGroups`` list.

        """
        check_type(orgId, str, optional=True)
        check_type(locationId, str, optional=True)
        check_type(name, str, optional=True)
        check_type(phoneNumber, str, optional=True)
        check_type(max, int, optional=True)
        check_type(start, int, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
            locationId=locationId,
            name=name,
            phoneNumber=phoneNumber,
            max=max,
            start=start,
        )

        json_data = self._session.get(
            self._voicemail_groups_collection_endpoint(),
            params=params,
        )

        voicemail_groups = self._extract_list(json_data, "voicemailGroups")
        for item in voicemail_groups:
            yield self._object_factory(VOICEMAIL_GROUP_OBJECT_TYPE, item)

    def get_location_voicemail(self, locationId, orgId=None, **request_parameters):
        """Get location voicemail settings.

        Args:
            locationId(str): Get location voicemail settings for this location.
            orgId(str): Get location voicemail settings for this organization.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            ImmutableData: Location voicemail settings.

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

        json_data = self._session.get(
            self._location_voicemail_endpoint(locationId),
            params=params,
        )

        return self._object_factory(LOCATION_VOICEMAIL_OBJECT_TYPE, json_data)

    def update_location_voicemail(
        self,
        locationId,
        voicemailTranscriptionEnabled,
        orgId=None,
        **request_parameters,
    ):
        """Update location voicemail settings.

        Args:
            locationId(str): Update location voicemail settings for this
                location.
            voicemailTranscriptionEnabled(bool): Toggle voicemail
                transcription for the location.
            orgId(str): Update location voicemail settings for this
                organization.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(voicemailTranscriptionEnabled, bool)
        check_type(orgId, str, optional=True)

        params = dict_from_items_with_values(orgId=orgId)

        put_data = dict_from_items_with_values(
            request_parameters,
            voicemailTranscriptionEnabled=voicemailTranscriptionEnabled,
        )

        self._session.put(
            self._location_voicemail_endpoint(locationId),
            params=params,
            json=put_data,
            erc=204,
        )

    def create_voicemail_group(
        self,
        locationId,
        name,
        extension,
        passcode,
        languageCode,
        messageStorage,
        notifications,
        faxMessage,
        transferToNumber,
        emailCopyOfMessage,
        orgId=None,
        phoneNumber=None,
        firstName=None,
        lastName=None,
        directLineCallerIdName=None,
        dialByName=None,
        **request_parameters,
    ):
        """Create a new voicemail group for a location.

        Args:
            locationId(str): Create voicemail group for this location.
            name(str): Voicemail group name.
            extension(str, int): Voicemail group extension.
            passcode(str, int): Voicemail group passcode.
            languageCode(str): Language code for announcements.
            messageStorage(dict): Message storage configuration.
            notifications(dict): Message notification configuration.
            faxMessage(dict): Fax message configuration.
            transferToNumber(dict): Transfer-to-number configuration.
            emailCopyOfMessage(dict): Email-copy-of-message configuration.
            orgId(str): Create voicemail group for this organization.
            phoneNumber(str): Voicemail group phone number.
            firstName(str): Caller ID first name (deprecated by API).
            lastName(str): Caller ID last name (deprecated by API).
            directLineCallerIdName(dict): Direct line caller ID name config.
            dialByName(str): Dial by name value.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            ImmutableData: Object containing the created voicemail group ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(name, str)
        check_type(extension, (str, int))
        check_type(passcode, (str, int))
        check_type(languageCode, str)
        check_type(messageStorage, dict)
        check_type(notifications, dict)
        check_type(faxMessage, dict)
        check_type(transferToNumber, dict)
        check_type(emailCopyOfMessage, dict)
        check_type(orgId, str, optional=True)
        check_type(phoneNumber, str, optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(directLineCallerIdName, dict, optional=True)
        check_type(dialByName, str, optional=True)

        params = dict_from_items_with_values(orgId=orgId)

        post_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            phoneNumber=phoneNumber,
            extension=extension,
            firstName=firstName,
            lastName=lastName,
            passcode=passcode,
            languageCode=languageCode,
            messageStorage=messageStorage,
            notifications=notifications,
            faxMessage=faxMessage,
            transferToNumber=transferToNumber,
            emailCopyOfMessage=emailCopyOfMessage,
            directLineCallerIdName=directLineCallerIdName,
            dialByName=dialByName,
        )

        json_data = self._session.post(
            self._location_voicemail_groups_endpoint(locationId),
            params=params,
            json=post_data,
            erc=201,
        )

        return self._object_factory(VOICEMAIL_GROUP_CREATE_OBJECT_TYPE, json_data)

    def get_voicemail_group(
        self,
        locationId,
        voicemailGroupId,
        orgId=None,
        **request_parameters,
    ):
        """Get a location voicemail group by ID.

        Args:
            locationId(str): Location ID.
            voicemailGroupId(str): Voicemail group ID.
            orgId(str): Organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            ImmutableData: Voicemail group details.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(voicemailGroupId, str)
        check_type(orgId, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
        )

        json_data = self._session.get(
            self._location_voicemail_group_endpoint(locationId, voicemailGroupId),
            params=params,
        )

        return self._object_factory(VOICEMAIL_GROUP_OBJECT_TYPE, json_data)

    def update_voicemail_group(
        self,
        locationId,
        voicemailGroupId,
        orgId=None,
        name=None,
        phoneNumber=None,
        extension=None,
        firstName=None,
        lastName=None,
        enabled=None,
        passcode=None,
        languageCode=None,
        greeting=None,
        greetingDescription=None,
        messageStorage=None,
        notifications=None,
        faxMessage=None,
        transferToNumber=None,
        emailCopyOfMessage=None,
        directLineCallerIdName=None,
        dialByName=None,
        **request_parameters,
    ):
        """Modify a location voicemail group.

        Args:
            locationId(str): Location ID.
            voicemailGroupId(str): Voicemail group ID.
            orgId(str): Organization ID.
            name(str): Voicemail group name.
            phoneNumber(str): Voicemail group phone number.
            extension(str, int): Voicemail group extension.
            firstName(str): Caller ID first name.
            lastName(str): Caller ID last name.
            enabled(bool): Whether voicemail group is enabled.
            passcode(str, int): Voicemail group passcode.
            languageCode(str): Language code.
            greeting(str): Greeting selection.
            greetingDescription(str): Greeting description.
            messageStorage(dict): Message storage config.
            notifications(dict): Notification config.
            faxMessage(dict): Fax config.
            transferToNumber(dict): Transfer config.
            emailCopyOfMessage(dict): Email copy config.
            directLineCallerIdName(dict): Direct line caller ID name config.
            dialByName(str): Dial by name value.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(voicemailGroupId, str)
        check_type(orgId, str, optional=True)
        check_type(name, str, optional=True)
        check_type(phoneNumber, str, optional=True)
        check_type(extension, (str, int), optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(enabled, bool, optional=True)
        check_type(passcode, (str, int), optional=True)
        check_type(languageCode, str, optional=True)
        check_type(greeting, str, optional=True)
        check_type(greetingDescription, str, optional=True)
        check_type(messageStorage, dict, optional=True)
        check_type(notifications, dict, optional=True)
        check_type(faxMessage, dict, optional=True)
        check_type(transferToNumber, dict, optional=True)
        check_type(emailCopyOfMessage, dict, optional=True)
        check_type(directLineCallerIdName, dict, optional=True)
        check_type(dialByName, str, optional=True)

        params = dict_from_items_with_values(orgId=orgId)

        put_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            phoneNumber=phoneNumber,
            extension=extension,
            firstName=firstName,
            lastName=lastName,
            enabled=enabled,
            passcode=passcode,
            languageCode=languageCode,
            greeting=greeting,
            greetingDescription=greetingDescription,
            messageStorage=messageStorage,
            notifications=notifications,
            faxMessage=faxMessage,
            transferToNumber=transferToNumber,
            emailCopyOfMessage=emailCopyOfMessage,
            directLineCallerIdName=directLineCallerIdName,
            dialByName=dialByName,
        )

        self._session.put(
            self._location_voicemail_group_endpoint(locationId, voicemailGroupId),
            params=params,
            json=put_data,
            erc=204,
        )

    # Alias for parity with API wording.
    modify_voicemail_group = update_voicemail_group

    def delete_voicemail_group(
        self,
        locationId,
        voicemailGroupId,
        orgId=None,
        **request_parameters,
    ):
        """Delete a location voicemail group by ID.

        Args:
            locationId(str): Location ID.
            voicemailGroupId(str): Voicemail group ID.
            orgId(str): Organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(voicemailGroupId, str)
        check_type(orgId, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
        )

        self._session.delete(
            self._location_voicemail_group_endpoint(locationId, voicemailGroupId),
            params=params,
            erc=204,
        )

    def list_voicemail_group_available_phone_numbers(
        self,
        locationId,
        orgId=None,
        max=None,
        start=None,
        phoneNumber=None,
        **request_parameters,
    ):
        """Get available phone numbers for voicemail groups in a location.

        Args:
            locationId(str): Location ID.
            orgId(str): Organization ID.
            max(int): Maximum number of numbers to return.
            start(int): Start index for pagination.
            phoneNumber(str): Optional phone-number filter.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            list: Available phone numbers.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.
            MalformedResponse: If the response does not include a
                ``phoneNumbers`` list.

        """
        check_type(locationId, str)
        check_type(orgId, str, optional=True)
        check_type(max, int, optional=True)
        check_type(start, int, optional=True)
        check_type(phoneNumber, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
            max=max,
            start=start,
            phoneNumber=phoneNumber,
        )

        json_data = self._session.get(
            self._location_voicemail_groups_endpoint(locationId)
            + "/availableNumbers",
            params=params,
        )

        return self._extract_list(json_data, "phoneNumbers")

    def list_voicemail_group_fax_message_available_phone_numbers(
        self,
        locationId,
        orgId=None,
        max=None,
        start=None,
        phoneNumber=None,
        **request_parameters,
    ):
        """Get available phone numbers for voicemail group fax message use.

        Args:
            locationId(str): Location ID.
            orgId(str): Organization ID.
            max(int): Maximum number of numbers to return.
            start(int): Start index for pagination.
            phoneNumber(str): Optional phone-number filter.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            list: Available fax-message phone numbers.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.
            MalformedResponse: If the response does not include a
                ``phoneNumbers`` list.

        """
        check_type(locationId, str)
        check_type(orgId, str, optional=True)
        check_type(max, int, optional=True)
        check_type(start, int, optional=True)
        check_type(phoneNumber, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
            max=max,
            start=start,
            phoneNumber=phoneNumber,
        )

        json_data = self._session.get(
            self._location_voicemail_groups_endpoint(locationId)
            + "/faxMessage/availableNumbers",
            params=params,
        )

        return self._extract_list(json_data, "phoneNumbers")

    def get_voice_portal(self, locationId, orgId=None, **request_parameters):
        """Get location voice portal settings.

        Args:
            locationId(str): Location ID.
            orgId(str): Organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            ImmutableData: Voice portal settings.

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

        json_data = self._session.get(
            self._location_voice_portal_endpoint(locationId),
            params=params,
        )

        return self._object_factory(VOICE_PORTAL_OBJECT_TYPE, json_data)

    def update_voice_portal(
        self,
        locationId,
        orgId=None,
        name=None,
        languageCode=None,
        extension=None,
        phoneNumber=None,
        firstName=None,
        lastName=None,
        passcode=None,
        directLineCallerIdName=None,
        dialByName=None,
        **request_parameters,
    ):
        """Update location voice portal settings.

        Args:
            locationId(str): Location ID.
            orgId(str): Organization ID.
            name(str): Voice portal name.
            languageCode(str): Language code.
            extension(str, int): Extension.
            phoneNumber(str): Phone number.
            firstName(str): Caller ID first name.
            lastName(str): Caller ID last name.
            passcode(str, int): Voice portal passcode.
            directLineCallerIdName(dict): Direct line caller ID name config.
            dialByName(str): Dial by name value.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.

        """
        check_type(locationId, str)
        check_type(orgId, str, optional=True)
        check_type(name, str, optional=True)
        check_type(languageCode, str, optional=True)
        check_type(extension, (str, int), optional=True)
        check_type(phoneNumber, str, optional=True)
        check_type(firstName, str, optional=True)
        check_type(lastName, str, optional=True)
        check_type(passcode, (str, int), optional=True)
        check_type(directLineCallerIdName, dict, optional=True)
        check_type(dialByName, str, optional=True)

        params = dict_from_items_with_values(orgId=orgId)

        put_data = dict_from_items_with_values(
            request_parameters,
            name=name,
            languageCode=languageCode,
            extension=extension,
            phoneNumber=phoneNumber,
            firstName=firstName,
            lastName=lastName,
            passcode=passcode,
            directLineCallerIdName=directLineCallerIdName,
            dialByName=dialByName,
        )

        self._session.put(
            self._location_voice_portal_endpoint(locationId),
            params=params,
            json=put_data,
            erc=204,
        )

    def list_voice_portal_available_phone_numbers(
        self,
        locationId,
        orgId=None,
        max=None,
        start=None,
        phoneNumber=None,
        **request_parameters,
    ):
        """Get available phone numbers for a location voice portal.

        Args:
            locationId(str): Location ID.
            orgId(str): Organization ID.
            max(int): Maximum number of numbers to return.
            start(int): Start index for pagination.
            phoneNumber(str): Optional phone-number filter.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            list: Available voice-portal phone numbers.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex cloud returns an error.
            MalformedResponse: If the response does not include a
                ``phoneNumbers`` list.

        """
        check_type(locationId, str)
        check_type(orgId, str, optional=True)
        check_type(max, int, optional=True)
        check_type(start, int, optional=True)
        check_type(phoneNumber, str, optional=True)

        params = dict_from_items_with_values(
            request_parameters,
            orgId=orgId,
            max=max,
            start=start,
            phoneNumber=phoneNumber,
        )

        json_data = self._session.get(
            self._location_voice_portal_endpoint(locationId)
            + "/availableNumbers",
            params=params,
        )

        return self._extract_list(json_data, "phoneNumbers")

    def get_voice_portal_passcode_rule(
        self, locationId, orgId=None, **request_parameters
    ):
        """Get location voice portal passcode rules.

        Args:
            locationId(str): Location ID.
            orgId(str): Organization ID.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            ImmutableData: Voice portal passcode-rule settings.

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

        json_data = self._session.get(
            self._location_voice_portal_endpoint(locationId) + "/passcodeRules",
            params=params,
        )

        return self._object_factory(VOICE_PORTAL_PASSCODE_RULE_OBJECT_TYPE, json_data)
