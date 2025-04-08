from enum import Enum


class Permission(str, Enum):
    ADD = "add"
    ADMIN = "admin"
    ANALYST_DATA = "analyst_data"
    AUDIT = "audit"
    AUTH = "auth"
    DECAYING = "decaying"
    DELEGATE = "delegate"
    FULL = "full"
    GALAXY_EDITOR = "galaxy_editor"
    MODIFY = "modify"
    MODIFY_ORG = "modify_org"
    OBJECT_TEMPLATE = "object_template"
    PUBLISH = "publish"
    PUBLISH_KAFKA = "publish_kafka"
    PUBLISH_ZMQ = "publish_zmq"
    REGEXP_ACCESS = "regexp_access"
    SERVER_SIGN = "server_sign"
    SHARING_GROUP = "sharing_group"
    SIGHTING = "sighting"
    SITE_ADMIN = "site_admin"
    SKIP_OTP = "skip_otp"
    SYNC = "sync"
    SYNC_AUTHORITATIVE = "sync_authoritative"
    SYNC_INTERNAL = "sync_internal"
    TAGGER = "tagger"
    TAG_EDITOR = "tag_editor"
    TEMPLATE = "template"
    VIEW_FEED_CORRELATIONS = "view_feed_correlations"
    WARNINGLIST = "warninglist"

    def __str__(self) -> str:
        return str(self.value)
