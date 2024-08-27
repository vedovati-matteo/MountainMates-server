from .. import db
from app.model.utente import Utente
from app.model.amici import Amici
from app.service.utente_service import get_all_utenti, get_amici_utente

def suggest_friends(id):
    all_users = get_all_utenti()

    # Create a dictionary to represent the adjacency matrix
    adjacency_dict = {user.id_firebase: set() for user in all_users}

    # Populate the adjacency dictionary
    for user in all_users:
        friends = get_amici_utente(user.id_firebase)
        for friend in friends:
            adjacency_dict[user.id_firebase].add(friend.id_firebase)

    # Find the index of the target user
    target_user_index = next((i for i, u in enumerate(all_users) if u.id_firebase == id), None)
    if target_user_index is None:
        return []  # User not found

    suggested_friend_indices = suggest_friends_list(adjacency_dict, id)

    # Convert indices back to user objects
    suggested_friends = [all_users[i] for i in suggested_friend_indices]
    return suggested_friends

def suggest_friends_list(adjacency_dict, target_user_id):
    direct_friends = adjacency_dict.get(target_user_id, set())

    # Find friends of friends
    friends_of_friends = set()
    for friend_id in direct_friends:
        friends_of_friends.update(adjacency_dict.get(friend_id, set()))

    # Remove the target user and their direct friends from the suggestions
    friends_of_friends.discard(target_user_id)
    friends_of_friends.difference_update(direct_friends)

    return list(friends_of_friends)

