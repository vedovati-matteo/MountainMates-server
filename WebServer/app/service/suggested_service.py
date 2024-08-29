from .. import db
from app.model.user import User
from app.model.friends import Friends
from app.service.user_service import get_all_users, get_user_friends


def suggest_friends(user_id):
    """
    Suggests potential friends for a user based on their existing friends' connections.
    """
    all_users = get_all_users()

    # Create a dictionary to represent the adjacency matrix (user -> set of friends)
    adjacency_dict = {user.firebase_id: set() for user in all_users}

    # Populate the adjacency dictionary
    for user in all_users:
        friends = get_user_friends(user.firebase_id)
        for friend in friends:
            adjacency_dict[user.firebase_id].add(friend.firebase_id)

    # Find the index of the target user
    target_user_index = next((i for i, u in enumerate(all_users) if u.firebase_id == user_id), None)
    if target_user_index is None:
        return []  # User not found

    suggested_friend_ids = suggest_friends_list(adjacency_dict, user_id)

    suggested_friends_indices = []
    
    for i, v in enumerate([u.firebase_id for u in all_users]):
        if v in suggested_friend_ids:
            suggested_friends_indices.append(i)
    
    # Convert indices back to user objects
    suggested_friends = [all_users[i] for i in suggested_friends_indices]
    
    return suggested_friends


def suggest_friends_list(adjacency_dict, target_user_id):
    """
    Helper function to generate a list of suggested friend IDs based on the adjacency matrix.
    """
    direct_friends = adjacency_dict.get(target_user_id, set())

    # Find friends of friends (potential suggestions)
    friends_of_friends = set()
    for friend_id in direct_friends:
        friends_of_friends.update(adjacency_dict.get(friend_id, set()))
    
    # Remove the target user and their direct friends from the suggestions
    friends_of_friends.discard(target_user_id)
    friends_of_friends.difference_update(direct_friends)

    return list(friends_of_friends)