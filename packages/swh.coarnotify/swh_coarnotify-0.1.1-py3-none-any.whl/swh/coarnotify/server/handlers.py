# Copyright (C) 2025  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information
"""Module dedicated to the handlers of COAR Notifications."""

from importlib.metadata import version
import json
from typing import Callable

from django.conf import settings

from swh.model.model import (
    MetadataAuthority,
    MetadataAuthorityType,
    MetadataFetcher,
    Origin,
    RawExtrinsicMetadata,
)
from swh.storage import get_storage

from .models import InboundNotification, Statuses
from .utils import create_accept_cn, reject, send_cn, to_sorted_tuple, unprocessable

CNHandler = Callable[[InboundNotification], None]


def get_handler(notification: InboundNotification) -> CNHandler | None:
    """Get a CN handler from its type.

    The list of handlers by type is defined in the ``handlers`` dict.

    Args:
        notification: an inbound CN

    Raises:
        UnprocessableException: no handler available for cn

    Returns:
        A COAR Notification handler if one matches
    """
    type_ = to_sorted_tuple(notification.payload["type"])
    try:
        return handlers[type_]
    except KeyError:
        error_message = f"Unable to process {', '.join(type_)} COAR Notifications"
        unprocessable(notification, error_message)
        return None


def mention(notification: InboundNotification) -> None:
    """Handle a mention COAR Notification.

    Validates the payload and send an Accept CN.

    Args:
        cn: an inbound CN

    Raises:
        RejectException: invalid payload
    """

    # validate the payload and extract data or raise unprocessable
    context_data = notification.payload["context"]  # describe the software
    object_data = notification.payload["object"]  # describe the relationship

    origin_url = context_data["id"]
    if origin_url != object_data["as:object"]:
        error_message = (
            f"Context id {origin_url} does not match "
            f"object as:object {object_data['as:object']}"
        )
        reject(notification, error_message)
        return

    context_type = to_sorted_tuple(context_data["type"])
    if "sorg:SoftwareSourceCode" not in context_type:
        error_message = "Context type does not contain sorg:SoftwareSourceCode"
        reject(notification, error_message)
        return

    # TODO: validation
    # relationship = object_data["as:relationship"]  # required
    # subject = object_data["as:subject"]  # required
    # verify cn.payload["origin"]["id"]
    # save metadata

    storage = get_storage(**settings.SWH_CONF["storage"])
    metadata_fetcher = MetadataFetcher(
        name="swh-coarnotify", version=version("swh-coarnotify")
    )
    # TODO try except
    origin = Origin(origin_url)
    swhid = origin.swhid()
    metadata_authority = MetadataAuthority(
        type=MetadataAuthorityType.REGISTRY,  # XXX: use a dedicated type ?
        url=notification.payload["origin"]["id"],
    )

    metadata_object = RawExtrinsicMetadata(
        target=swhid,
        discovery_date=notification.created_at,
        authority=metadata_authority,
        fetcher=metadata_fetcher,
        format="coarnotify-mention-v1",
        metadata=json.dumps(notification.payload).encode(),
    )

    storage.metadata_authority_add([metadata_authority])
    storage.metadata_fetcher_add([metadata_fetcher])
    storage.raw_extrinsic_metadata_add([metadata_object])

    # update cn and send a reply
    notification.status = Statuses.ACCEPTED
    notification.save()
    # XXX should we had an extra context here to return the swhid ?
    accepted_cn = create_accept_cn(notification, summary=f"Stored mention for {swhid}")
    send_cn(accepted_cn)


handlers = {
    ("Announce", "RelationshipAction"): mention,
}
