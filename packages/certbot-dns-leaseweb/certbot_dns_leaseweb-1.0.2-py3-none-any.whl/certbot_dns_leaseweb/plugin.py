"""DNS Authenticator plugin for Leaseweb DNS."""

import requests

from certbot import errors
from certbot.plugins import dns_common

from certbot_dns_leaseweb.client import (
    LeasewebClient,
    LeasewebException,
)


class LeasewebAuthenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Leaseweb.

    This Authenticator uses the Leasweb Domains API to complete dns-01
    challenges.
    """

    description = str(
        "Obtain certificates using a DNS TXT record (if using Leaseweb DNS)."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = None
        self.override_domain = None
        self._client = None

    @property
    def client(self):
        """Return a LeasewebClient instance initialised with the supplied
        credentials.
        """

        if self._client is None:
            self._client = self._get_client()
        return self._client

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super().add_parser_arguments(add)
        add("credentials", help="Leaseweb credentials INI file.")
        add(
            "override-domain",
            default="",
            type=str,
            help="Override Leaseweb domain name (to support DNS delegation)",
        )

    def more_info(self) -> str:
        """A human-readable string to inform users of what this plugin does."""
        return (
            "This plugin completes dns-01 challenges using "
            "the Leaseweb Domains API to configure DNS TXT records."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Leaseweb credentials INI file",
            {
                "api_token": str(
                    "an API token obtained from "
                    "'https://secure.leaseweb.com/api-client-management/'"
                ),
            },
        )

    def _perform(self, domain: str, validation_name: str, validation: str):
        try:
            self.client.add_record(
                domain,
                validation_name,
                [validation],
            )
        except (
            requests.ConnectionError,
            LeasewebException,
        ) as exception:
            raise errors.PluginError(exception)

    def _cleanup(self, domain: str, validation_name: str, validation: str):
        self.client.delete_record(
            domain,
            validation_name,
        )

    def _get_client(self):
        return LeasewebClient(
            self.credentials.conf("api_token"), self.conf("override_domain")
        )
