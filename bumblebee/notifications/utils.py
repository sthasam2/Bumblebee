"""
create_buzz_notification(buzz, new_upvotes=None, new_downvotes=None, remove_votes=None, comments=None, )
update_buzz_notification(buzz, new_upvotes=None, new_downvotes=None, remove_votes=None, comments=None, )
delete_notification(buzz, new_upvotes=None, new_downvotes=None, remove_votes=None, comments=None, )
"""


def generate_notification_string(action, latest, count, contenttype):
    """ """

    if count == 1:
        return f"{latest[0]} {action} your {contenttype}."
    elif count == 2:
        return f"{latest[0]} and {latest[1]} {action} your {contenttype}."
    elif count >= 2:
        return f"{latest[0]}, {latest[1]}, and {count-2} others {action} your {contenttype}."
