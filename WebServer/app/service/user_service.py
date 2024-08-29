from .. import db
from app.model.user import User
from app.model.friends import Friends
from datetime import datetime
from flask import abort


def get_all_users():
    """
    Retrieves all users from the database.
    """
    return User.query.all()


def save_new_user(data, firebase_id):
    """
    Creates and saves a new user to the database.
    """
    user = User.query.filter_by(firebase_id=firebase_id).first()
    if not user:
        new_user = User(
            firebase_id=firebase_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            nickname=data['nickname'],
            date_of_birth=datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date(),
            bio=data['bio'],
            hiker_level=data['hiker_level'],
            is_organizer=False  # New users are not organizers by default
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'User registered successfully'
        }
        return response_object, 200
    else:
        abort(409, 'User already exists')


def get_user(user_id):
    """
    Retrieves a specific user from the database.
    """
    return User.query.filter_by(firebase_id=user_id).first_or_404()


def update_user(data, user_id):
    """
    Updates an existing user's information in the database
    """
    user = User.query.filter_by(firebase_id=user_id).first()
    if user:
        keys_to_update = ['first_name', 'last_name', 'nickname', 'bio', 'hiker_level', 'profile_picture']

        for key in keys_to_update:
            if key in data:
                setattr(user, key, data[key])
        
        if 'date_of_birth' in data:
            user.date_of_birth = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()
        
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'User updated successfully'
        }
        return response_object, 200
    else:
        abort(404, 'User not found')


def delete_user(user_id):
    """
    Deletes a user from the database
    """
    user = User.query.filter_by(firebase_id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'User deleted successfully'
        }
        return response_object, 200
    else:
        abort(404, 'User not found')


def get_user_friends(user_id):
    """
    Retrieves a list of a user's friends.
    """
    user = User.query.filter_by(firebase_id=user_id).first()
    if user:
        friends = User.query.filter(User.firebase_id.in_(
            db.session.query(Friends.friend_id).filter_by(user_id=user_id)
        )).all()
        return friends
    else:
        abort(404, 'User not found')


def add_friend(data, user_id):
    """
    Adds a friend to a user's friend list
    """
    user = User.query.filter_by(firebase_id=user_id).first()
    if user:
        if user_id == data['firebase_id']:
            abort(409, 'Cannot be friends with yourself')

        existing_friendship = Friends.query.filter_by(user_id=user_id, friend_id=data['firebase_id']).first()
        if existing_friendship:
            response_object = {
                'status': 'success',
                'message': 'Friendship already exists'
            }
            return response_object, 200
        else:
            friendship = Friends(user_id=user_id, friend_id=data['firebase_id'])
            save_changes(friendship)
            response_object = {
                'status': 'success',
                'message': 'Friend added successfully'
            }
            return response_object, 200
    else:
        abort(404, 'User not found')


def remove_friend(data, user_id):
    """
    Removes a friend from a user's friend list
    """
    user = User.query.filter_by(firebase_id=user_id).first()
    if user:
        friendship = Friends.query.filter_by(user_id=user_id, friend_id=data['firebase_id']).first()
        if friendship:
            db.session.delete(friendship)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Friend removed successfully'
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'success',
                'message': 'Friendship does not exist'
            }
            return response_object, 200
    else:
        abort(404, 'User not found')


def get_all_organizers():
    """
    Retrieves all users who are organizers
    """
    return User.query.filter_by(is_organizer=True).all()


def save_changes(data):
    """
    Helper function to save changes to the database
    """
    db.session.add(data)
    db.session.commit()