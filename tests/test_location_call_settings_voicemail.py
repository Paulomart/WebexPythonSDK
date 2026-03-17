"""Unit tests for Location Call Settings: Voicemail API wrapper."""

from unittest.mock import Mock

import pytest

from webexpythonsdk.api.location_call_settings_voicemail import (
    LocationCallSettingsVoicemailAPI,
)
from webexpythonsdk.exceptions import MalformedResponse
from webexpythonsdk.models.dictionary import dict_data_factory
from webexpythonsdk.restsession import RestSession


@pytest.fixture
def voicemail_api():
    session = RestSession(
        access_token="fake-token",
        base_url="https://webexapis.com/v1/",
    )
    return LocationCallSettingsVoicemailAPI(session, dict_data_factory)


def test_get_location_voicemail(voicemail_api):
    voicemail_api._session.get = Mock(
        return_value={"voicemailTranscriptionEnabled": True}
    )

    result = voicemail_api.get_location_voicemail("loc-1", orgId="org-1")

    assert result["voicemailTranscriptionEnabled"] is True
    voicemail_api._session.get.assert_called_once_with(
        "telephony/config/locations/loc-1/voicemail",
        params={"orgId": "org-1"},
    )


def test_list_voicemail_groups(voicemail_api):
    voicemail_api._session.get = Mock(
        return_value={
            "voicemailGroups": [
                {"id": "vg-1", "name": "Support"},
                {"id": "vg-2", "name": "Sales"},
            ]
        }
    )

    result = list(voicemail_api.list_voicemail_groups(orgId="org-1"))

    assert [item["id"] for item in result] == ["vg-1", "vg-2"]
    voicemail_api._session.get.assert_called_once_with(
        "telephony/config/voicemailGroups",
        params={"orgId": "org-1"},
    )


def test_create_voicemail_group(voicemail_api):
    voicemail_api._session.post = Mock(
        return_value={"id": "997e8784-e2e4-4aa3-93d6-679b2b128d8e"}
    )

    result = voicemail_api.create_voicemail_group(
        "loc-1",
        name="Support Voicemail",
        extension=1234,
        passcode=4321,
        languageCode="en_us",
        messageStorage={"storageType": "INTERNAL"},
        notifications={"enabled": False},
        faxMessage={"enabled": False},
        transferToNumber={"enabled": False},
        emailCopyOfMessage={"enabled": False},
        orgId="org-1",
    )

    assert result["id"] == "997e8784-e2e4-4aa3-93d6-679b2b128d8e"

    voicemail_api._session.post.assert_called_once()
    args, kwargs = voicemail_api._session.post.call_args

    assert args[0] == "telephony/config/locations/loc-1/voicemailGroups"
    assert kwargs["params"] == {"orgId": "org-1"}
    assert kwargs["erc"] == 201
    assert kwargs["json"]["name"] == "Support Voicemail"
    assert kwargs["json"]["extension"] == 1234
    assert kwargs["json"]["passcode"] == 4321
    assert kwargs["json"]["languageCode"] == "en_us"


def test_update_location_voicemail(voicemail_api):
    voicemail_api._session.put = Mock()

    voicemail_api.update_location_voicemail(
        "loc-1",
        voicemailTranscriptionEnabled=True,
        orgId="org-1",
    )

    voicemail_api._session.put.assert_called_once_with(
        "telephony/config/locations/loc-1/voicemail",
        params={"orgId": "org-1"},
        json={"voicemailTranscriptionEnabled": True},
        erc=204,
    )


def test_list_voicemail_group_available_phone_numbers(voicemail_api):
    voicemail_api._session.get = Mock(
        return_value={"phoneNumbers": ["+12065550101", "+12065550102"]}
    )

    result = voicemail_api.list_voicemail_group_available_phone_numbers(
        "loc-1", orgId="org-1"
    )

    assert result == ["+12065550101", "+12065550102"]
    voicemail_api._session.get.assert_called_once_with(
        "telephony/config/locations/loc-1/voicemailGroups/availableNumbers",
        params={"orgId": "org-1"},
    )


def test_list_voicemail_group_available_phone_numbers_malformed(voicemail_api):
    voicemail_api._session.get = Mock(return_value={})

    with pytest.raises(MalformedResponse):
        voicemail_api.list_voicemail_group_available_phone_numbers("loc-1")
