import time
import firebase_admin
from firebase_admin import credentials, firestore
from queue import Queue
import threading
import datetime

# A queue storing the keyboards to clean
keyboards_to_clean = Queue()

# Create a threading lock
lock = threading.Lock()


def init_app():
    global db, keyboards
    cred = credentials.Certificate("service json here")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    keyboards = db.collection("keyboards")


def clean_keyboard(keyboard_data):

    print("Cleaning keyboard:", keyboard_data)

    time.sleep(5)

    # Get the keyboard id
    keyId = keyboard_data.get("keyId", None)

    # Update progress to indicate cleaning has started (0.3)
    with lock:
        keyboards.document(keyId).update({
            "progress": 0.3
        })

    # Simulate cleaning process (e.g., the turtle bot cleaning)
    time.sleep(5)

    # Update progress to finished (1.0) and log cleaning time
    with lock:
        keyboards.document(keyId).update({
            "progress": 1.0,
            "lastCleaned": datetime.datetime.now()
        })


def keyboard_listener(col_snapshot, changes, read_time):
    print("Snapshot received.")

    for change in changes:
        # Ignore removals
        if change.type.name == 'REMOVED':
            continue

        # Get the document data
        data = change.document.to_dict()
        key_id = change.document.id

        print("Keyboard ID:", key_id)
        print("Keyboard Data:", data)

        # Check if cleaning has been requested
        lastRequested = data.get("lastRequested", None)
        if lastRequested is None:
            print("No request to clean.")
            continue

        lastCleaned = data.get("lastCleaned", None)
        # Skip if already cleaned after the last request
        if lastCleaned is not None and lastCleaned > lastRequested:
            print("Already cleaned.")
            continue

        print("Requested clean")
        # Add the keyboard data to the queue for cleaning
        keyboards_to_clean.put(data)


def firebase_main():
    # Initialize the firebase app
    init_app()

    # Listen to the keyboard collection snapshots
    keyboards.order_by("lastRequested").on_snapshot(keyboard_listener)

    print("Listening for changes. Press Ctrl+C to exit.")
    try:
        while True:
            if not keyboards_to_clean.empty():
                keyboard_data = keyboards_to_clean.get()
                clean_keyboard(keyboard_data)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
