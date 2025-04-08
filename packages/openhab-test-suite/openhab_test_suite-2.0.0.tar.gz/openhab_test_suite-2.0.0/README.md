# **openhab-test-suite**  
A comprehensive testing library for validating and interacting with openHAB installations.

**openhab-test-suite** simplifies the process of testing items, rules, and things in openHAB systems. The library provides an easy-to-use Python API that interacts with the openHAB REST API, enabling automated testing of various components in your smart home environment.  

---

## **Features**  
- **Item Testing**: Validate item states and ensure proper functionality for various types (e.g., Switch, String, Color).  
- **Thing Testing**: Verify thing statuses (e.g., ONLINE, OFFLINE, PENDING) and troubleshoot connectivity issues.  
- **Rule Testing**: Manage and execute rules programmatically to ensure their expected behavior.  
- Supports local and cloud-based openHAB instances.  
- Designed for developers and testers working on openHAB integrations.  

---

## **Why use openhab-test-suite?**  
This library helps identify issues quickly, automate validation processes, and maintain a reliable smart home setup. Whether you are building new automations or troubleshooting an existing configuration, **openhab-test-suite** provides the tools you need.  

---

## **Requirements**  
- Python 3.7 or newer  
- `python-openhab-crud` library (install using `pip install python-openhab-crud`)
- `python-openhab-itemevents` library (install using `pip install python-openhab-itemevents`)  
- A running openHAB server with REST API enabled (you have to enable Basic Authentication)

---

## **Installation**

### **Install via pip**

To install the package using pip, simply run:

```bash
pip install openhab-test-suite
```

### **Manual Installation**

1. Clone the repository:  
   ```bash
   git clone https://github.com/Michdo93/openhab-test-suite.git
   cd openhab-test-suite
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your openHAB server settings in your Python code.  

---

## **Usage**  

Here is an example of how to use the library for basic operations:  

### Initialize the Client  
```python
from openhab import OpenHABClient

client = OpenHABClient(
    url="http://openhab-server:8080",
    username="your-username",
    password="your-password"
)
```

### Test Things  
```python
from openhab_test_suite import ThingTester

thingTester = ThingTester(client)

# Check if a thing is ONLINE
isOnline = thingTester.isThingOnline("LightSwitch1")
print(f"LightSwitch1 online status: {isOnline}")
```

### Test Rules  
```python
from openhab_test_suite import RuleTester

ruleTester = RuleTester(client)

# Run a rule and verify the result
ruleTester.runRule("myRuleUID")
```

### Test Items
```python
from openhab_test_suite import ItemTester

itemTester = ItemTester(client)
itemName = "testSwithc"

# Check if an item could reach expected state
print(f"{itemName}: ", tester.testSwitch(itemName=itemName, command="ON", expectedState="ON"))
```

---

## **Full List of Methods**

### **ItemTester**  
Provides methods to test and validate openHAB items.

| **Method**             | **Parameters**                                                                                                                   | **Return Value**         | **Description**                                                                                                                                         |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `__init__`             | `client: OpenHABClient`                                                                                                    | None                     | Initializes the `ItemTester` class with an OpenHAB client.                                                                                           |
| `doesItemExist`        | `itemName: str`                                                                                                                  | `True`/`False`           | Checks whether an item exists in the OpenHAB system.                                                                                                    |
| `checkItemIsType`      | `itemName: str`, `itemType: str`                                                                                                 | `True`/`False`           | Checks if an item has the expected type.                                                                                                                |
| `checkItemHasState`    | `itemName: str`, `state`                                                                                                         | `True`/`False`           | Verifies whether an item has a specific state.                                                                                                          |
| `testColor`            | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `Color`.                                                                                                     |
| `testContact`          | `itemName: str`, `update: str = None`, `expectedState: str = None`, `timeout: int = 60`                                          | `True`/`False`           | Tests the functionality of an item of type `Contact`.                                                                                                   |
| `testDateTime`         | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `DateTime`.                                                                                                  |
| `testDimmer`           | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `Dimmer`.                                                                                                    |
| `testImage`            | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `Image`.                                                                                                     |
| `testLocation`         | `itemName: str`, `update: str`, `expectedState=None`, `timeout: int = 60`                                                        | `True`/`False`           | Tests the functionality of an item of type `Location`.                                                                                                  |
| `testNumber`           | `itemName: str`, `command`, `expectedState=None`, `timeout: int = 60`                                                            | `True`/`False`           | Tests the functionality of an item of type `Number`.                                                                                                    |
| `testPlayer`           | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `Player`.                                                                                                    |
| `testRollershutter`    | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `Rollershutter`.                                                                                            |
| `testString`           | `itemName: str`, `command`, `expectedState=None`, `timeout: int = 60`                                                            | `True`/`False`           | Tests the functionality of an item of type `String`.                                                                                                    |
| `testSwitch`           | `itemName: str`, `command: str`, `expectedState=None`, `timeout: int = 60`                                                       | `True`/`False`           | Tests the functionality of an item of type `Switch`.                                                                                                    |
| `__testItem`           | `itemName: str`, `itemType: str`, `commandOrUpdate=None`, `expectedState=None`, `timeout: int = 60`                              | `True`/`False`           | General test function for verifying the functionality of an item.                                                                                       |
| `__reset_item`         | `itemName: str`, `itemType: str`, `initialState`                                                                                 | None                     | Resets the state of an item to its original state.                                                                                                      |
| `__check_final_state`  | `itemName: str`, `expectedState`                                                                                                 | `True`/`False`           | Checks the final state of an item after processing a command or update.                                                                                 |

---

### **ThingTester**  
Provides methods to test and validate openHAB things.

| **Method**                         | **Description**                                                                                                    | **Parameters**                                                                                                          | **Return Value**                               |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `__init__(self, client: OpenHABClient)` | Initializes the `ThingTester` with the provided OpenHAB client.                                                   | `client` (OpenHABClient): The OpenHAB client used to interact with the OpenHAB server.                           | None                                           |
| `_getThingStatus(self, thingUid: str)` | Retrieves the status of a Thing based on its unique identifier (UID).                                                | `thingUid` (str): The unique identifier (UID) of the Thing.                                                              | `str`: The status of the Thing (e.g., "ONLINE", "OFFLINE", "UNKNOWN"). |
| `isThingStatus(self, thingUid: str, statusToCheck: str)` | Checks if a Thing has the specified status.                                                                        | `thingUid` (str): The unique identifier (UID) of the Thing.<br> `statusToCheck` (str): The status to check (e.g., "ONLINE", "OFFLINE"). | `bool`: `True` if the Thing matches the status, `False` otherwise. |
| `isThingOnline(self, thingUid: str)` | Checks if a Thing is in the ONLINE status.                                                                          | `thingUid` (str): The unique identifier (UID) of the Thing.                                                               | `bool`: `True` if the Thing is ONLINE, `False` otherwise. |
| `isThingOffline(self, thingUid: str)` | Checks if a Thing is in the OFFLINE status.                                                                         | `thingUid` (str): The unique identifier (UID) of the Thing.                                                               | `bool`: `True` if the Thing is OFFLINE, `False` otherwise. |
| `isThingPending(self, thingUid: str)` | Checks if a Thing is in the PENDING status.                                                                         | `thingUid` (str): The unique identifier (UID) of the Thing.                                                               | `bool`: `True` if the Thing is PENDING, `False` otherwise. |
| `isThingUnknown(self, thingUid: str)` | Checks if a Thing is in the UNKNOWN status.                                                                         | `thingUid` (str): The unique identifier (UID) of the Thing.                                                               | `bool`: `True` if the Thing is UNKNOWN, `False` otherwise. |
| `isThingUninitialized(self, thingUid: str)` | Checks if a Thing is in the UNINITIALIZED status.                                                                   | `thingUid` (str): The unique identifier (UID) of the Thing.                                                               | `bool`: `True` if the Thing is UNINITIALIZED, `False` otherwise. |
| `isThingError(self, thingUid: str)` | Checks if a Thing is in the ERROR state.                                                                             | `thingUid` (str): The unique identifier (UID) of the Thing.                                                               | `bool`: `True` if the Thing is in ERROR state, `False` otherwise. |
| `enableThing(self, thingUid: str)`  | Enables a Thing by sending a PUT request to activate it.                                                             | `thingUid` (str): The unique identifier (UID) of the Thing to be enabled.                                                  | `bool`: `True` if the Thing was successfully enabled, `False` otherwise. |
| `disableThing(self, thingUid: str)` | Disables a Thing by sending a PUT request to deactivate it.                                                           | `thingUid` (str): The unique identifier (UID) of the Thing to be disabled.                                                | `bool`: `True` if the Thing was successfully disabled, `False` otherwise. |

---

### **RuleTester**  
Provides methods to manage and test openHAB rules.

| **Method**                         | **Description**                                                                                                    | **Parameters**                                                                                                          | **Return Value**                               |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `__init__(self, client: OpenHABClient)` | Initializes the `RuleTester` with the provided OpenHAB client.                                                   | `client` (OpenHABClient): The OpenHAB client used to interact with the OpenHAB server.                           | None                                           |
| `runRule(self, ruleUid: str)`       | Executes a rule immediately.                                                                                        | `ruleUid` (str): The UID of the rule to be executed.                                                                     | `bool`: `True` if the rule was executed successfully, `False` otherwise. |
| `enableRule(self, ruleUid: str)`    | Enables a rule by sending a POST request to the server.                                                             | `ruleUid` (str): The UID of the rule to be enabled.                                                                      | `bool`: `True` if the rule was successfully enabled, `False` otherwise. |
| `disableRule(self, ruleUid: str)`   | Disables a rule by sending a POST request to the server.                                                            | `ruleUid` (str): The UID of the rule to be disabled.                                                                     | `bool`: `True` if the rule was successfully disabled, `False` otherwise. |
| `testRuleExecution(self, ruleUid: str, expectedItem: str, expectedValue: str)` | Tests the execution of a rule and verifies the expected outcome on a specific item.                                  | `ruleUid` (str): The UID of the rule to be tested.<br>`expectedItem` (str): The item to check after rule execution.<br>`expectedValue` (str): The expected value of the item. | `bool`: `True` if the item state matches the expected value, `False` otherwise. |
| `isRuleActive(self, ruleUid: str)`  | Checks if the rule is active by retrieving its status from the server.                                               | `ruleUid` (str): The UID of the rule to check.                                                                            | `bool`: `True` if the rule is active, `False` otherwise. |
| `isRuleDisabled(self, ruleUid: str)` | Checks if the rule is disabled by retrieving its status from the server.                                            | `ruleUid` (str): The UID of the rule to check.                                                                            | `bool`: `True` if the rule is disabled, `False` otherwise. |
| `isRuleRunning(self, ruleUid: str)` | Checks if the rule is currently running by checking its status.                                                     | `ruleUid` (str): The UID of the rule to check.                                                                            | `bool`: `True` if the rule is running, `False` otherwise. |
| `isRuleIdle(self, ruleUid: str)`    | Checks if the rule is in the IDLE state by checking its status.                                                     | `ruleUid` (str): The UID of the rule to check.                                                                            | `bool`: `True` if the rule is idle, `False` otherwise. |
| `getRuleStatus(self, ruleUid: str)` | Retrieves the full status of a rule, including detailed information.                                                | `ruleUid` (str): The UID of the rule to check.                                                                            | `dict`: A dictionary containing the rule's status details. |

---

## **Contributing**

We welcome contributions to improve **openhab-test-suite**!  

### How to contribute:  
1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.  

Please ensure your code adheres to PEP 8 guidelines and includes relevant documentation and tests.  

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
