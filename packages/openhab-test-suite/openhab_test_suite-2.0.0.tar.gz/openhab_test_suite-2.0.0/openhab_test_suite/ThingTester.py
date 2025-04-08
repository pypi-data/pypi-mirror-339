from openhab import OpenHABClient, Things
import json

class ThingTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ItemTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.thingsAPI = Things(client)

    def _getThingStatus(self, thingUID: str) -> str:
        """
        Retrieves the status of a Thing based on its UID.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            str: The status of the Thing (e.g., "ONLINE", "OFFLINE", etc.). Returns "UNKNOWN" if status cannot be determined.
        """
        thing = self.thingsAPI.getThing(thingUID)

        if thing:
            statusInfo = thing.get("statusInfo", {})
            return statusInfo.get("status", "UNKNOWN")
        return "UNKNOWN"

    def isThingStatus(self, thingUID: str, statusToCheck: str) -> bool:
        """
        Checks whether a Thing has the specified status.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.
            statusToCheck (str): The status to check against (e.g., "ONLINE", "OFFLINE").

        Returns:
            bool: True if the Thing has the specified status, False otherwise.
        """
        return self._getThingStatus(thingUID) == statusToCheck

    def isThingOnline(self, thingUID: str) -> bool:
        """
        Checks if a Thing is ONLINE.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is ONLINE, False otherwise.
        """
        return self.isThingStatus(thingUID, "ONLINE")

    def isThingOffline(self, thingUID: str) -> bool:
        """
        Checks if a Thing is OFFLINE.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is OFFLINE, False otherwise.
        """
        return self.isThingStatus(thingUID, "OFFLINE")

    def isThingPending(self, thingUID: str) -> bool:
        """
        Checks if a Thing is in PENDING status.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in PENDING status, False otherwise.
        """
        return self.isThingStatus(thingUID, "PENDING")

    def isThingUnknown(self, thingUID: str) -> bool:
        """
        Checks if a Thing is in UNKNOWN status.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in UNKNOWN status, False otherwise.
        """
        return self.isThingStatus(thingUID, "UNKNOWN")

    def isThingUninitialized(self, thingUID: str) -> bool:
        """
        Checks if a Thing is in UNINITIALIZED status.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in UNINITIALIZED status, False otherwise.
        """
        return self.isThingStatus(thingUID, "UNINITIALIZED")

    def isThingError(self, thingUID: str) -> bool:
        """
        Checks if a Thing is in ERROR state.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in ERROR state, False otherwise.
        """
        return self.isThingStatus(thingUID, "ERROR")

    def enableThing(self, thingUID: str) -> bool:
        """
        Enables a Thing by sending a PUT request to activate it.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing to be enabled.

        Returns:
            bool: True if the Thing was successfully enabled, False otherwise.
        """
        thing = self.thingsAPI.setThingStatus(thingUID, True)

        if "error" in thing:
            print(json.dumps(thing, indent=4))
            return False
        print(f"Thing {thingUID} was successfully enabled.")
        return True

    def disableThing(self, thingUID: str) -> bool:
        """
        Disables a Thing by sending a PUT request to deactivate it.

        Parameters:
            thingUID (str): The unique identifier (UID) of the Thing to be disabled.

        Returns:
            bool: True if the Thing was successfully disabled, False otherwise.
        """
        thing = self.thingsAPI.setThingStatus(thingUID, False)

        if "error" in thing:
            print(json.dumps(thing, indent=4))
            return False
        print(f"Thing {thingUID} was successfully disabled.")
        return True
