import time
from openhab import OpenHABClient, Rules, Items
import json

class RuleTester:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ItemTester with an OpenHAB client.

        :param client: The OpenHABClient instance used to communicate with the OpenHAB system.
        """
        self.client = client
        self.rulesAPI = Rules(client)
        self.__itemsAPI = Items(client)

    def runRule(self, ruleUID: str, contextData: dict = None) -> bool:
        """
        Executes a rule immediately.

        :param ruleUID: The UID of the rule to be executed.
        :return: True if the rule was executed successfully, False otherwise.
        """
        if self.isRuleDisabled(ruleUID):
            print(f"Error: Rule {ruleUID} could not be executed because it is disabled.")
            return False

        rule = self.rulesAPI.runNow(ruleUID, contextData)

        if "error" in rule:
            print(json.dumps(rule, indent=4))
            return False
        print(f"Rule {ruleUID} executed successfully.")
        return True

    def enableRule(self, ruleUID: str) -> bool:
        """
        Enables a rule.

        :param ruleUID: The UID of the rule to be enabled.
        :return: True if the rule was successfully enabled, False otherwise.
        """
        rule = self.rulesAPI.enableRule(ruleUID)

        if "error" in rule:
            print(json.dumps(rule, indent=4))
            return False
        print(f"Rule {ruleUID} executed successfully.")
        return True

    def disableRule(self, ruleUID: str) -> bool:
        """
        Disables a rule.

        :param ruleUID: The UID of the rule to be disabled.
        :return: True if the rule was successfully disabled, False otherwise.
        """
        rule = self.rulesAPI.disableRule(ruleUID)

        if "error" in rule:
            print(json.dumps(rule, indent=4))
            return False
        print(f"Rule {ruleUID} executed successfully.")
        return True

    def testRuleExecution(self, ruleUID: str, expectedItem: str, expectedValue: str) -> bool:
        """
        Tests the execution of a rule and verifies the expected outcome.

        :param ruleUID: The UID of the rule to be tested.
        :param expectedItem: The item to check after rule execution.
        :param expectedValue: The expected value of the item.
        :return: True if the test was successful, otherwise False.
        """
        try:
            # Run the rule
            if not self.runRule(ruleUID):
                print(f"Error: Rule {ruleUID} could not be executed.")
                return False

            # Short pause for rule execution
            time.sleep(2)

            # Retrieve the state of the item
            state = self.__itemsAPI.getItemState(expectedItem)
            
            if state is None or state != expectedValue:
                print(f"Error: State of item {expectedItem} after rule execution does not match. Expected: {expectedValue}, Found: {state}")
                return False

            print(f"{expectedItem} state after rule execution: {state}")
            return state == expectedValue
        except Exception as e:
            print(f"Error during rule test execution: {e}")
            return False

    def isRuleActive(self, ruleUID: str) -> bool:
        """
        Checks if the rule is active.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is active, False otherwise.
        """
        rule = self.rulesAPI.getRule(ruleUID)

        # Check if the response is a valid dictionary
        if isinstance(rule, dict) and "status" in rule:
            # Extract the status
            status = rule.get("status", {}).get("status", "UNINITIALIZED")
            print(f"Rule status: {status}")
            return status != "UNINITIALIZED"

        # Error case
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def isRuleDisabled(self, ruleUID: str) -> bool:
        """
        Checks if the rule is disabled.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is disabled, False otherwise.
        """
        rule = self.rulesAPI.getRule(ruleUID)

        # Check if the response is a valid dictionary
        if isinstance(rule, dict) and "status" in rule:
            # Extract the status and statusDetail
            status = rule.get("status", {}).get("status", "IDLE")
            statusDetail = rule.get("status", {}).get("statusDetail", "NONE")
            print(f"Rule status: {status}, Detail: {statusDetail}")

            # Rule is disabled if status is "UNINITIALIZED" and statusDetail is "DISABLED"
            return status == "UNINITIALIZED" and statusDetail == "DISABLED"

        # Error case
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def isRuleRunning(self, ruleUID: str) -> bool:
        """
        Checks if the rule is currently running.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is running, False otherwise.
        """
        rule = self.rulesAPI.getRule(ruleUID)

        # Check if the response is a valid dictionary
        if isinstance(rule, dict) and "status" in rule:
            # Extract the status
            status = rule.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")

            # Rule is running if the status is "RUNNING"
            return status == "RUNNING"

        # Error case
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def isRuleIdle(self, ruleUID: str) -> bool:
        """
        Checks if the rule is in the IDLE state.

        :param ruleUID: The UID of the rule to check.
        :return: True if the rule is in the IDLE state, False otherwise.
        """
        rule = self.rulesAPI.getRule(ruleUID)

        # Check if the response is a valid dictionary
        if isinstance(rule, dict) and "status" in rule:
            # Extract the status
            status = rule.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")

            # Rule is in the IDLE state if the status is "IDLE"
            return status == "IDLE"

        # Error case
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return False

    def getRuleStatus(self, ruleUID: str) -> dict:
        """
        Retrieves the full status of a rule.

        :param ruleUID: The UID of the rule whose status is to be retrieved.
        :return: A dictionary containing status information or an empty dictionary in case of an error.
        """
        rule = self.rulesAPI.getRule(ruleUID)

        # Check if the response is a valid dictionary
        if isinstance(rule, dict) and "status" in rule:
            # Extract status information
            statusInfo = {
                "status": rule.get("status", {}).get("status", "UNKNOWN"),
                "statusDetail": rule.get("status", {}).get("statusDetail", "UNKNOWN"),
                "editable": rule.get("editable", False),
                "name": rule.get("name", ""),
                "uid": rule.get("uid", ""),
            }
            print(f"Rule status details: {statusInfo}")
            return statusInfo

        # Error case
        print(f"Error retrieving the status of rule {ruleUID}. Response: {rule}")
        return {}
