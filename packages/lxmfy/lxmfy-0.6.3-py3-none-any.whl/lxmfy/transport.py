"""
Transport module for LXMFy bot framework.

This module provides transport layer functionality for establishing and managing
network connections using Reticulum Network Stack (RNS). It handles path discovery,
link establishment, and caching of active connections. The Transport class serves
as the main interface for network operations, with support for path and request
handlers.
"""

import logging
import time
from dataclasses import dataclass
from typing import Callable, Optional

import RNS

from .permissions import DefaultPerms


@dataclass
class PathInfo:
    next_hop: Optional[bytes]
    hops: int
    updated_at: int


class Transport:
    def __init__(self, storage):
        self.storage = storage
        self.logger = logging.getLogger(__name__)
        self.cached_links = {}
        self.paths = {}
        self._path_handlers = []
        self._request_handlers = {}

    def register_path_handler(self, handler: Callable):
        self._path_handlers.append(handler)

    def deregister_path_handler(self, handler: Callable):
        if handler in self._path_handlers:
            self._path_handlers.remove(handler)

    def register_request_handler(self, request_type: str, handler: Callable):
        self._request_handlers[request_type] = handler

    def deregister_request_handler(self, request_type: str):
        self._request_handlers.pop(request_type, None)

    def load_paths(self):
        self.paths = self.storage.get("transport:paths", {})

    def save_paths(self):
        self.storage.set("transport:paths", self.paths)

    def establish_link(self, destination_hash: bytes, timeout: int = 15) -> RNS.Link:
        """Establish a link with path discovery"""
        # Check if user has permission to establish links
        sender = RNS.hexrep(destination_hash, delimit=False)
        if not self.bot.permissions.has_permission(sender, DefaultPerms.USE_BOT):
            raise Exception("User does not have permission to establish links")

        self.load_paths()
        try:
            if RNS.Transport.has_path(destination_hash):
                return self._create_link(destination_hash, timeout)

            RNS.Transport.request_path(destination_hash)

            path_timeout = time.time() + timeout
            while time.time() < path_timeout:
                if RNS.Transport.has_path(destination_hash):
                    return self._create_link(destination_hash, timeout)
                time.sleep(0.1)

            raise Exception("Path lookup timed out")

        except Exception as e:
            self.logger.error("Error establishing link: %s", str(e))
            raise
        finally:
            self.save_paths()

    def _create_link(self, destination_hash: bytes, timeout: int) -> RNS.Link:
        """Create and establish a link"""
        try:
            identity = RNS.Identity.recall(destination_hash)
            if not identity:
                raise Exception("Identity not found")

            destination = RNS.Destination(
                identity,
                RNS.Destination.OUT,
                RNS.Destination.SINGLE,
                "nomadnetwork",
                "node",
            )

            link = RNS.Link(destination)

            start_time = time.time()
            while time.time() - start_time < timeout:
                if link.status == RNS.Link.ACTIVE:
                    self.cached_links[destination_hash] = link
                    return link
                time.sleep(0.1)

            raise Exception("Link establishment timed out")

        except Exception as e:
            self.logger.error("Error creating link: %s", str(e))
            raise

    def cleanup(self):
        """Clean up inactive links"""
        for link in list(self.cached_links.values()):
            if link.status != RNS.Link.ACTIVE:
                link.teardown()

        self.cached_links = {
            hash: link
            for hash, link in self.cached_links.items()
            if link.status == RNS.Link.ACTIVE
        }
