import inspect
import pkgutil
from typing import List, Type

from schema import CareerEvent
from connectors import __path__ as connectors_path
from connectors import __name__ as connectors_package
from connectors.base import CareerConnector


CONNECTOR_LOAD_ORDER = ["gmail", "linkedin", "dice", "clearancejobs"]


class ConnectorManager:

    def __init__(self):
        self.connectors = [
            connector_class()
            for connector_class in self._discover_connector_classes()
        ]

    def _discover_connector_classes(self) -> List[Type[CareerConnector]]:
        """
        Discover concrete connector classes from the connectors package.
        """
        connector_classes = []

        for module_info in sorted(
            pkgutil.iter_modules(connectors_path),
            key=lambda info: info.name,
        ):
            if module_info.name == "base":
                continue

            module = __import__(
                f"{connectors_package}.{module_info.name}",
                fromlist=[""],
            )

            for _, candidate in inspect.getmembers(module, inspect.isclass):
                if not issubclass(candidate, CareerConnector):
                    continue
                if candidate is CareerConnector or inspect.isabstract(candidate):
                    continue
                if candidate.__module__ != module.__name__:
                    continue

                connector_classes.append(candidate)

        return sorted(connector_classes, key=self._connector_sort_key)

    def _connector_sort_key(self, connector_class: Type[CareerConnector]) -> tuple:
        """
        Sort connectors in the product load order, then by source name.
        """
        source_name = connector_class.source_name

        if source_name in CONNECTOR_LOAD_ORDER:
            return (CONNECTOR_LOAD_ORDER.index(source_name), source_name)

        return (len(CONNECTOR_LOAD_ORDER), source_name)

    def load_all_events(self) -> List[CareerEvent]:
        events: List[CareerEvent] = []

        for connector in self.connectors:

            print(f"Loading {connector.source_name}...")

            events.extend(connector.load_events())

        return events
