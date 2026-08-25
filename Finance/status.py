from . import USER_ID

def user(event):

    return event.sender_id == USER_ID
