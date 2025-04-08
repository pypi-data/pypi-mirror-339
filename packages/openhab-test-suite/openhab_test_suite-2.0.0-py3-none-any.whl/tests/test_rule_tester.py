from openhab_test_suite import RuleTester
from openhab import OpenHABClient
import time

# Establishing connection to the OpenHAB API
client = OpenHABClient("http://127.0.0.1:8080", "openhab", "habopen")

# Instantiating the RuleTester
ruleTester = RuleTester(client)

# Example: Testing the functions of the RuleTester
ruleUid = "test_color-1"  # Replace this with the actual rule UID
expectedItem = "testColor"  # Replace this with the item to be checked
expectedValue = "140,50,50"  # The expected value after rule execution

print("Testing RuleTester...\n")

# Testing the retrieval of the rule status
print("Testing getRuleStatus...")
status = ruleTester.getRuleStatus(ruleUid)
print(f"getRuleStatus result: {status}\n")

# Testing if the rule is active
print("Testing isRuleActive...")
isActive = ruleTester.isRuleActive(ruleUid)
print(f"isRuleActive result: {isActive}\n")

# Testing if the rule is disabled
print("Testing isRuleDisabled...")
isDisabled = ruleTester.isRuleDisabled(ruleUid)
print(f"isRuleDisabled result: {isDisabled}\n")

# Testing if the rule is running
print("Testing isRuleRunning...")
isRunning = ruleTester.isRuleRunning(ruleUid)
print(f"isRuleRunning result: {isRunning}\n")

# Testing if the rule is in the IDLE state
print("Testing isRuleIdle...")
isIdle = ruleTester.isRuleIdle(ruleUid)
print(f"isRuleIdle result: {isIdle}\n")

# Testing enabling the rule
print("Testing enableRule...")
enableResult = ruleTester.enableRule(ruleUid)
print(f"enableRule result: {enableResult}\n")

# Short wait to ensure the rule was enabled
time.sleep(1)

# Testing disabling the rule
print("Testing disableRule...")
disableResult = ruleTester.disableRule(ruleUid)
print(f"disableRule result: {disableResult}\n")

# Testing rule execution
print("Testing runRule...")
runResult = ruleTester.runRule(ruleUid)
print(f"runRule result: {runResult}\n")

# Testing rule execution and verifying the item state
print("Testing testRuleExecution...")
testExecutionResult = ruleTester.testRuleExecution(ruleUid, expectedItem, expectedValue)
print(f"testRuleExecution result: {testExecutionResult}\n")

# Optional: Wait to ensure everything is processed
time.sleep(2)

print("All tests completed.")
