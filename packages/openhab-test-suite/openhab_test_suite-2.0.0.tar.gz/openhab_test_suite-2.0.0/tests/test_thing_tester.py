from openhab_test_suite import ThingTester
from openhab import OpenHABClient

# Here we establish the connection to the OpenHAB API
client = OpenHABClient("http://127.0.0.1:8080", "openhab", "habopen")

# Instantiation of the ThingTester
thingTester = ThingTester(client)

# Example: Testing the various statuses of a Thing
thingUid = "astro:moon:56bdb13645"  # Replace with the actual Thing UID
thingUid2 = "astro:sun:560560e11a"  # Replace with the actual Thing UID

print("Testing ThingTester...")

# Test if the Thing is ONLINE
if thingTester.isThingOnline(thingUid):
    print(f"Thing {thingUid} is ONLINE.")
else:
    print(f"Thing {thingUid} is NOT ONLINE.")

# Test if the Thing is OFFLINE
if thingTester.isThingOffline(thingUid):
    print(f"Thing {thingUid} is OFFLINE.")
else:
    print(f"Thing {thingUid} is NOT OFFLINE.")

# Test if the Thing is in ERROR state
if thingTester.isThingError(thingUid):
    print(f"Thing {thingUid} has an error.")
else:
    print(f"Thing {thingUid} has no error.")

# Test if the Thing is in PENDING state
if thingTester.isThingPending(thingUid):
    print(f"Thing {thingUid} is in PENDING state.")
else:
    print(f"Thing {thingUid} is NOT in PENDING state.")

# Test the second Thing
if thingTester.isThingOnline(thingUid2):
    print(f"Thing {thingUid2} is ONLINE.")
else:
    print(f"Thing {thingUid2} is NOT ONLINE.")

# Test if the second Thing is OFFLINE
if thingTester.is_thing_offline(thingUid2):
    print(f"Thing {thingUid2} is OFFLINE.")
else:
    print(f"Thing {thingUid2} is NOT OFFLINE.")

# Test if the second Thing is in ERROR state
if thingTester.isThingError(thingUid2):
    print(f"Thing {thingUid2} has an error.")
else:
    print(f"Thing {thingUid2} has no error.")

# Test if the second Thing is in PENDING state
if thingTester.isThingPending(thingUid2):
    print(f"Thing {thingUid2} is in PENDING state.")
else:
    print(f"Thing {thingUid2} is NOT in PENDING state.")

# Enable the second Thing
if thingTester.enableThing(thingUid2):
    print(f"{thingUid2} successfully enabled.")
else:
    print(f"Error enabling {thingUid2}.")

# Disable the first Thing
if thingTester.disableThing(thingUid):
    print(f"{thingUid} successfully disabled.")
else:
    print(f"Error disabling {thingUid}.")

# Test if the first Thing is ONLINE
if thingTester.isThingOnline(thingUid):
    print(f"Thing {thingUid} is ONLINE.")
else:
    print(f"Thing {thingUid} is NOT ONLINE.")

# Test if the first Thing is OFFLINE
if thingTester.isThingOffline(thingUid):
    print(f"Thing {thingUid} is OFFLINE.")
else:
    print(f"Thing {thingUid} is NOT OFFLINE.")

# Test if the first Thing is in ERROR state
if thingTester.isThingError(thingUid):
    print(f"Thing {thingUid} has an error.")
else:
    print(f"Thing {thingUid} has no error.")

# Test if the first Thing is in PENDING state
if thingTester.isThingPending(thingUid):
    print(f"Thing {thingUid} is in PENDING state.")
else:
    print(f"Thing {thingUid} is NOT in PENDING state.")

# Test the second Thing again
if thingTester.isThingOnline(thingUid2):
    print(f"Thing {thingUid2} is ONLINE.")
else:
    print(f"Thing {thingUid2} is NOT ONLINE.")

# Test if the second Thing is OFFLINE again
if thingTester.isThingOffline(thingUid2):
    print(f"Thing {thingUid2} is OFFLINE.")
else:
    print(f"Thing {thingUid2} is NOT OFFLINE.")

# Test if the second Thing is in ERROR state again
if thingTester.isThingError(thingUid2):
    print(f"Thing {thingUid2} has an error.")
else:
    print(f"Thing {thingUid2} has no error.")

# Test if the second Thing is in PENDING state again
if thingTester.isThingPending(thingUid2):
    print(f"Thing {thingUid2} is in PENDING state.")
else:
    print(f"Thing {thingUid2} is NOT in PENDING state.")
