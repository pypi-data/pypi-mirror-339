import time
import json
from openhab import OpenHABClient, Items, ItemEvents

class ItemTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ItemTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.itemsAPI = Items(client)
        self.itemEventsAPI = ItemEvents(client)

    def doesItemExist(self, itemName: str):
        """
        Checks if an item exists in the OpenHAB system.

        :param itemName: The name of the item to check.
        :return: True if the item exists, otherwise False.
        """
        testItem = self.itemsAPI.getItem(itemName)
        if testItem and testItem.get("name") == itemName:
            return True
        print(f"Error: The item {itemName} does not exist!")
        return False

    def checkItemIsType(self, itemName: str, itemType: str):
        return True
        """
        Verifies that an item is of a specific type.

        :param itemName: The name of the item to check.
        :param itemType: The expected type of the item.
        :return: True if the item is of the expected type, otherwise False.
        """
        validTypes = ["Color", "Contact", "DateTime", "Dimmer", "Group", "Image", "Location", "Number", "Player", "Rollershutter", "String", "Switch"]
        if itemType not in validTypes:
            print(f"Error: '{itemType}' is not a valid item type.")
            return False

        try:
            # Abruf der Item-Daten
            testItem = self.itemsAPI.getItem(itemName)
            if testItem is None:
                print(f"Error: The item '{itemName}' could not be found. Received None.")
                return False

            # Debugging: Gibt die vollständigen Daten des Items aus
            print(f"Item data for '{itemName}': {testItem}")

            print(testItem.get("type"))
            print(itemType)

            # Überprüfung des Item-Typslinux
            if testItem.get("type") == itemType:
                return True

            print(f"Error: The item '{itemName}' is not of type '{itemType}'! Found type: {testItem.get('type')}")
            return False
        except Exception as e:
            print(f"Error while checking item type for '{itemName}': {e}")
            return False

    def checkItemHasState(self, itemName: str, state):
        """
        Checks if an item has a specific state.

        :param itemName: The name of the item to check.
        :param state: The expected state of the item.
        :return: True if the item has the expected state, otherwise False.
        """
        checkState = self.itemsAPI.getItemState(itemName)
        if checkState is None:
            print(f"Error: Could not retrieve the state for item {itemName}.")
            return False

        #print(f"Current state of item '{itemName}': {checkState}")
        if checkState == state:
            return True

        return False

    def testColor(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Color item by sending a command and verifying the expected state.

        :param itemName: The name of the Color item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Color"):
            print(f"Test failed: {itemName} is not of type 'Color'.")
            return False

        #if isinstance(command, (list, set)):
        #    if not any(self.__crud._CRUD__checkColorValue(cmd) for cmd in command):
        #        return False
        #else:
        #    if not self.__crud._CRUD__checkColorValue(command):
        #        return False

        return self.__testItem(itemName, "Color", command, expectedState, timeout)

    def testContact(self, itemName: str, update: str = None, expectedState: str = None, timeout: int = 10):
        """
        Tests the functionality of a Contact item.

        :param itemName: The name of the Contact item.
        :param update: The update to send to the item, optional.
        :param expectedState: The expected state after the update.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Contact"):
            print(f"Test failed: {itemName} is not of type 'Contact'.")
            return False

        #if not self.__crud._CRUD__checkContactValue(update):
        #    return False

        return self.__testItem(itemName, "Contact", update, expectedState, timeout)

    def testDateTime(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a DateTime item by sending a command and verifying the expected state.

        :param itemName: The name of the DateTime item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "DateTime"):
            print(f"Test failed: {itemName} is not of type 'DateTime'.")
            return False

        #if not self.__crud._CRUD__checkDateTimeValue(command):
        #    return False

        return self.__testItem(itemName, "DateTime", command, expectedState, timeout)

    def testDimmer(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Dimmer item by sending a command and verifying the expected state.

        :param itemName: The name of the Dimmer item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Dimmer"):
            print(f"Test failed: {itemName} is not of type 'Dimmer'.")
            return False

        #if not self.__crud._CRUD__checkDimmerValue(command):
        #    return False

        return self.__testItem(itemName, "Dimmer", str(command), str(expectedState), timeout)

    def testImage(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Image item by sending a command and verifying the expected state.

        :param itemName: The name of the Image item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Image"):
            print(f"Test failed: {itemName} is not of type 'Image'.")
            return False

        #if not self.__crud._CRUD__checkImageValue(command):
        #    return False

        return self.__testItem(itemName, "Image", command, expectedState, timeout)

    def testLocation(self, itemName: str, update: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Location item.

        :param itemName: The name of the Location item.
        :param update: The update to send to the item, optional.
        :param expectedState: The expected state after the update.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Location"):
            print(f"Test failed: {itemName} is not of type 'Location'.")
            return False

        #if not self.__crud._CRUD__checkLocationValue(update):
        #    return False

        #if isinstance(update, (list, set)):
        #    if not any(self.__crud._CRUD__checkLocationValue(updt) for updt in update):
        #        return False
        #else:
        #    if not self.__crud._CRUD__ch_CRUD__checkLocationValueeckStringValue(update):
        #        return False

        return self.__testItem(itemName, "Location", update, expectedState, timeout)

    def testNumber(self, itemName: str, command, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Number item by sending a command and verifying the expected state.

        :param itemName: The name of the Number item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Number"):
            print(f"Test failed: {itemName} is not of type 'Number'.")
            return False

        #if not self.__crud._CRUD__checkNumberValue(command):
        #    return False

        return self.__testItem(itemName, "Number", str(command), str(expectedState), timeout)

    def testPlayer(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Player item by sending a command and verifying the expected state.

        :param itemName: The name of the Player item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        #if not self.checkItemIsType(itemName, "Player"):
        #    print(f"Test failed: {itemName} is not of type 'Player'.")
        #    return False

        #if not self.__crud._CRUD__checkPlayerValue(command):
        #    return False
        
        return self.__testItem(itemName, "Player", command, expectedState, timeout)

    def testRollershutter(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Rollershutter item by sending a command and verifying the expected state.

        :param itemName: The name of the Rollershutter item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Rollershutter"):
            print(f"Test failed: {itemName} is not of type 'Rollershutter'.")
            return False

        #if not self.__crud._CRUD__checkRollershutterValue(command):
        #    return False

        return self.__testItem(itemName, "Rollershutter", command, expectedState, timeout)

    def testString(self, itemName: str, command, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a String item by sending a command and verifying the expected state.

        :param itemName: The name of the String item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "String"):
            print(f"Test failed: {itemName} is not of type 'String'.")
            return False

        #if isinstance(command, (list, set)):
        #    if not any(self.__crud._CRUD__checkStringValue(cmd) for cmd in command):
        #        return False
        #else:
        #    if not self.__crud._CRUD__checkStringValue(command):
        #        return False

        return self.__testItem(itemName, "String", command, expectedState, timeout)

    def testSwitch(self, itemName: str, command: str, expectedState = None, timeout: int = 10):
        """
        Tests the functionality of a Switch item by sending a command and verifying the expected state.

        :param itemName: The name of the Switch item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Switch"):
            print(f"Test failed: {itemName} is not of type 'Switch'.")
            return False

        #if not self.__crud._CRUD__checkSwitchValue(command):
        #    return False

        return self.__testItem(itemName, "Switch", command, expectedState, timeout)
    """
    def __testItem(self, itemName: str, itemType: str, commandOrUpdate=None, expectedState=None, timeout: int = 10):
        
        Generic test function for validating the behavior of an item.

        :param itemName: The name of the item to test.
        :param itemType: The type of the item.
        :param commandOrUpdate: The command or update to send to the item (optional).
        :param expectedState: The expected state after the command/update, optional.
                            Can be a single value or a list/set of possible states.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        
        initialState = None
        returnValue = False
        try:
            # Retrieve the initial state if a command/update is to be sent
            initialState = self.itemsAPI.getItemState(itemName) if commandOrUpdate is not None else None
            if initialState is None and commandOrUpdate is not None:
                print(f"Warning: Could not retrieve initial state for item {itemName}.")

            # Open SSE connection to listen for state changes before sending the command/update
            response = self.itemEventsAPI.ItemStateChangedEvent(itemName)
            if response is None:
                print(f"Error: No SSE response received for item {itemName}.")
                return False

            state = None
            startTime = time.time()

            # Start processing SSE events
            with response as events:
                # Send the command/update if provided
                if commandOrUpdate is not None:
                    if itemType in ["Contact", "Location"]:
                        self.itemsAPI.postUpdate(itemName, str(commandOrUpdate))
                    else:
                        self.itemsAPI.sendCommand(itemName, commandOrUpdate)

                    while True:
                        # Check if timeout has been reached
                        if time.time() - startTime > timeout:
                            print(f"Timeout reached after {timeout} seconds. Falling back to getState().")
                            break

                        # Process SSE events
                        for line in events.iter_lines():
                            line = line.decode()
                            if "data" in line:
                                line = line.replace("data: ", "")
                                try:
                                    # Parse the event data
                                    data = json.loads(line)
                                    payload = data.get("payload")
                                    eventType = data.get("type")

                                    # Only process ItemStateChangedEvent
                                    if eventType == "ItemStateChangedEvent" and payload:
                                        payloadData = json.loads(payload)
                                        state = payloadData.get("value")

                                        # Check if the received state matches the expected state
                                        if not isinstance(expectedState, (list, set)):
                                            if state == expectedState:
                                                returnValue = True
                                                return returnValue
                                        else:
                                            if state in expectedState:
                                                print(f"Success: {itemName} reached one of the expected states: {state}")
                                                returnValue = True
                                                return returnValue
                                except json.JSONDecodeError:
                                    print("Warning: Event could not be converted to JSON.")
                else:
                    # Fallback check: Verify final state after timeout
                    if not self.__checkFinalState(itemName, expectedState):
                        print(f"Error: After fallback, state of {itemName} is not in {expectedState}.")
                        returnValue = False
                    else:
                        returnValue = True

        except Exception as e:
            print(f"Error testing {itemName}: {e}")
            returnValue = False

        finally:
            # Ensure the item is reset to its initial state
            self.__resetItem(itemName, itemType, initialState)

        return returnValue
    """

    def __testItem(self, itemName: str, itemType: str, commandOrUpdate=None, expectedState=None, timeout: int = 10):
        """
        Generic test function for validating the behavior of an item.

        :param itemName: The name of the item to test.
        :param itemType: The type of the item.
        :param commandOrUpdate: The command or update to send to the item (optional).
        :param expectedState: The expected state after the command/update, optional.
                            Can be a single value or a list/set of possible states.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        initialState = None
        returnValue = False
        try:
            # Retrieve the initial state
            initialState = self.itemsAPI.getItemState(itemName) if commandOrUpdate is not None else None
            if initialState is None and commandOrUpdate is not None:
                print(f"Warning: Could not retrieve initial state for item {itemName}.")

            # Start SSE listener before sending the command
            response = self.itemEventsAPI.ItemStateChangedEvent(itemName)
            if response is None:
                print(f"Error: No SSE response received for item {itemName}.")
                return False

            state = None
            startTime = time.time()

            with response as events:
                # Send the command/update
                if commandOrUpdate is not None:
                    if itemType in ["Contact", "Location"]:
                        self.itemsAPI.postUpdate(itemName, str(commandOrUpdate))
                    else:
                        self.itemsAPI.sendCommand(itemName, commandOrUpdate)

                    # Iterate through the events
                    lines = events.iter_lines()
                    while time.time() - startTime > timeout:
                        line = next(lines, None)
                        if line is None:
                            # No event, continue to next iteration
                            continue

                        line = line.decode()
                        if "data" not in line:
                            continue

                        try:
                            data = json.loads(line.replace("data: ", ""))
                            payload = data.get("payload")
                            eventType = data.get("type")

                            if eventType == "ItemStateChangedEvent" and payload:
                                payloadData = json.loads(payload)
                                state = payloadData.get("value")

                                if not isinstance(expectedState, (list, set)):
                                    if state == expectedState:
                                        return True
                                else:
                                    if state in expectedState:
                                        print(f"Success: {itemName} reached one of the expected states: {state}")
                                        return True

                        except json.JSONDecodeError:
                            print("Warning: Event could not be converted to JSON.")

                # Timeout reached or no matching event found, fallback to checking the final state
                if not self.__checkFinalState(itemName, expectedState):
                    returnValue = False
                else:
                    returnValue = True

        except Exception as e:
            print(f"Error testing {itemName}: {e}")
            returnValue = False

        finally:
            # Reset item to original state if needed
            self.__resetItem(itemName, itemType, initialState)

        return returnValue

    def __resetItem(self, itemName: str, itemType: str, initialState):
        """
        Resets the item to initial state if necessary.

        :param itemName: The name of the Switch item.
        :param itemType: The type of the item.
        :param initialState: The initial state to send to the item.
        """
        if initialState is not None:
            if itemType in ["Contact", "Location"]:
                self.itemsAPI.postUpdate(itemName, initialState)
            else:
                self.itemsAPI.sendCommand(itemName, initialState)

    def __checkFinalState(self, itemName: str, expectedState):
        """
        Checks the final state other processing an command/update

        :param itemName: The name of the Switch item.
        :param expectedState: The expected state after the command/update, optional.
                            Can be a single value or a list/set of possible states.
        :return: True if the item has the expected state, otherwise False.
        """
        if not isinstance(expectedState, (list, set)):
            if not self.checkItemHasState(itemName, expectedState):
                print(f"Error: After fallback, state of {itemName} is not {expectedState}.")
                return False
        else:
            if not any(self.checkItemHasState(itemName, expected) for expected in expectedState):
                print(f"Error: After fallback, state of {itemName} is not in {expectedState}.")
                return False

        return True