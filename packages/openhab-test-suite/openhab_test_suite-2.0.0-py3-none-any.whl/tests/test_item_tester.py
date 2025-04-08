from openhab_test_suite import ItemTester
from openhab import OpenHABClient
import time

# Establishing connection to the OpenHAB API
client = OpenHABClient("http://127.0.0.1:8080", "openhab", "habopen")

# Instantiating the ItemTester
tester = ItemTester(client)

timeout = 10

def run_test():
    
    # Test for doesItemExist
    try:
        print(f"doesItemExists: ", tester.doesItemExist(itemName="testColor"))
    except Exception as e:
        print(f"Error in doesItemExist: {e}")
    
    time.sleep(1)

    # Test for checkItemIsType
    try:
        print(f"checkItemIsType: ", tester.checkItemIsType(itemName="testColor", itemType="Color"))
    except Exception as e:
        print(f"Error in checkItemIsType: {e}")
    
    time.sleep(1)

    # Test for checkItemHasState
    try:
        print(f"checkItemHasState: ", tester.checkItemHasState(itemName="testColor", state="ON"))
    except Exception as e:
        print(f"Error in checkItemHasState: {e}")
    
    time.sleep(1)

    # Test for testColor (assuming this sets the state)
    try:
        print(f"testColor: ", tester.testColor(itemName="testColor", command="255,0,0", expectedState="255,0,0", timeout=timeout))
        # Wait for a moment to ensure the state is updated
        time.sleep(2)
    except Exception as e:
        print(f"Error in testColor: {e}")
    
    time.sleep(1)

    # Test for testContact
    try:
        print(f"testContact: ", tester.testContact(itemName="testContact", update="CLOSED", expectedState="CLOSED", timeout=timeout))
    except Exception as e:
        print(f"Error in testContact: {e}")
    
    time.sleep(1)

    # Test for testDateTime
    try:
        print(f"testDateTime: ", tester.testDateTime(itemName="testDateTime", command="2025-01-20T06:38:12.813337920-0800", expectedState="2025-01-20T06:38:12.813337920-0800", timeout=timeout))
    except Exception as e:
        print(f"Error in testDateTime: {e}")
    
    time.sleep(1)

    # Test for testDimmer
    try:
        print(f"testDimmer: ", tester.testDimmer(itemName="testDimmer", command=50, expectedState=50, timeout=timeout))
    except Exception as e:
        print(f"Error in testDimmer: {e}")
    
    time.sleep(1)

    # Test for testImage
    try:
        # Uncomment if testImage is defined
        # print(f"testImage: ", tester.testImage(itemName="testImage", command="", expectedState="", timeout=timeout))
        pass
    except Exception as e:
        print(f"Error in testImage: {e}")
    
    time.sleep(1)

    # Test for testLocation
    try:
        print(f"testLocation: ", tester.testLocation(itemName="testLocation", update="48.054398,8.205645,0.1", expectedState="48.054398,8.205645,0.1", timeout=timeout))
    except Exception as e:
        print(f"Error in testLocation: {e}")
    
    time.sleep(1)

    # Test for testNumber
    try:
        print(f"testNumber: ", tester.testNumber(itemName="testNumber", command=42, expectedState=42, timeout=timeout))
    except Exception as e:
        print(f"Error in testNumber: {e}")
    
    time.sleep(1)

    # Test for testPlayer
    try:
        print(f"testPlayer: ", tester.testPlayer(itemName="testPlayer", command="PLAY", expectedState="PLAY", timeout=timeout))
    except Exception as e:
        print(f"Error in testPlayer: {e}")
    
    time.sleep(1)

    # Test for testRollershutter
    try:
        print(f"testRollershutter: ", tester.testRollershutter(itemName="testRollershutter", command="DOWN", expectedState="100", timeout=timeout))
    except Exception as e:
        print(f"Error in testRollershutter: {e}")
    
    time.sleep(1)

    # Test for testString
    try:
        print(f"testString: ", tester.testString(itemName="testString", command="Hello", expectedState="Hello", timeout=timeout))
    except Exception as e:
        print(f"Error in testString: {e}")
    
    time.sleep(1)

    # Test for testSwitch
    try:
        print(f"testSwitch: ", tester.testSwitch(itemName="testSwitch", command="ON", expectedState="ON", timeout=timeout))
    except Exception as e:
        print(f"Error in testSwitch: {e}")
    
run_test()
