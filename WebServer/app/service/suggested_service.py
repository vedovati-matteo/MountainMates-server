import numpy as np
from .. import db
from app.model.utente import Utente
from app.model.amici import Amici
from app.service.utente_service import get_all_utenti, get_amici_utente

def suggest_friends(id):
    utenti = get_all_utenti()
    matrix = np.zeros((len(utenti), len(utenti)))
    i_id = 0
    for i, u in enumerate(utenti):
        if u.id_firebase == id:
            id_i = i
        amici = get_amici_utente(u.id_firebase)
        for a in amici:
            for j, u2 in enumerate(utenti):
                if u2.id_firebase == a.id_firebase:
                    matrix[i][j] = 1
    l = suggest_friends_list(matrix, id_i)
    user_list = list()
    for i in l:
        user_list.append(utenti[i])
    return user_list
            

def suggest_friends_list(matrix, node):
    friends = []
    # Find the friends of the given node by finding the indices with value 1 in the matrix
    for i in range(len(matrix)):
        if matrix[node][i] == 1:
            friends.append(i)
    # Find the friends of the friends by checking the indices with value 1 in the matrix
    friends_of_friends = []
    for friend in friends:
        for i in range(len(matrix)):
            if matrix[friend][i] == 1 and i != node and i not in friends:
                friends_of_friends.append(i)
    return list(set(friends_of_friends))


