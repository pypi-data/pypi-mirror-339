# Copyright (C) 2025  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information
import uuid


def notification(id: str | uuid.UUID = "00000000-0000-0000-0000-000000000000") -> dict:
    return {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://coar-notify.net",
        ],
        "actor": {
            "id": "https://research-organisation.org",
            "name": "Research Organisation",
            "type": "Organization",
        },
        "context": {
            "id": "https://another-research-organisation.org/repository/datasets/item/201203421/",  # noqa: B950
            "ietf:cite-as": "https://doi.org/10.5555/999555666",
            "ietf:item": {
                "id": "https://another-research-organisation.org/repository/datasets/item/201203421/data_archive.zip",  # noqa: B950
                "mediaType": "application/zip",
                "type": ["Object", "sorg:Dataset"],
            },
            "type": ["Page", "sorg:SoftwareSourceCode"],
        },
        "id": f"urn:uuid:{id}",
        "object": {
            "as:object": "https://another-research-organisation.org/repository/datasets/item/201203421/",  # noqa: B950
            "as:relationship": "http://purl.org/vocab/frbr/core#supplement",
            "as:subject": "https://research-organisation.org/repository/item/201203/421/",
            "id": "urn:uuid:74FFB356-0632-44D9-B176-888DA85758DC",
            "type": "Relationship",
        },
        "origin": {
            "id": "https://research-organisation.org/repository",
            "inbox": "http://inbox.partner.local",
            "type": "Service",
        },
        "target": {
            "id": "https://swh",
            "inbox": "http://testserver/",
            "type": "Service",
        },
        "type": ["Announce", "coar-notify:RelationshipAction"],
    }
