import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app import db
from app.model.user import User
from app.model.friends import Friends
from base import BaseTestCase
from app.service.suggested_service import suggest_friends

@patch('firebase_admin.auth.verify_id_token')
class TestUserApi(BaseTestCase):
    """Tests for User related API endpoints."""

    def test_user_creation_retrieval_update_delete(self, mock_verify_id_token):
        """Tests creating, retrieving, listing, updating, and deleting a user."""

        # Sample user data as JSON payloads
        payload1 = json.dumps({
            'first_name': 'Test1',
            'last_name': 'User1',
            'date_of_birth': '1990-01-01',
            'nickname': 'testuser1',
            'bio': 'Test bio 1',
            'hiker_level': 1
        })
        payload2 = json.dumps({
            'first_name': 'Test2',
            'last_name': 'User2',
            'date_of_birth': '1995-05-10',
            'nickname': 'testuser2',
            'bio': 'Test bio 2',
            'hiker_level': 2
        })
        payload3 = json.dumps({  # Updated payload for user 1
            'first_name': 'Updated Test1',
            'last_name': 'User1',
            'date_of_birth': '1990-01-01',
            'nickname': 'testuser1',
            'bio': 'Updated bio 1',
            'hiker_level': 1,
            'profile_picture': 'test.png'
        })

        with self.app.test_client() as client:
            # 1. Add user 2
            response = client.post('api/user/', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, 
                                   data=payload2)
            self.assertEqual(200, response.status_code)
            user2 = User.query.filter_by(firebase_id='2').first()
            self.assertIsNotNone(user2)

            # 2. Add user 1
            response = client.post('api/user/', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=payload1)
            self.assertEqual(200, response.status_code)
            user1 = User.query.filter_by(firebase_id='1').first()
            self.assertIsNotNone(user1)

            # 3. Show self (user 1)
            response = client.get('api/user/self', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual('1', data['firebase_id'])

            # 4. Show user 2
            response = client.get('api/user/2', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual('2', data['firebase_id'])

            # 5. Show user list
            response = client.get('api/user/', headers={"Authorization": "Bearer " + '2'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(2, len(data))

            # 6. Show organizers list (expecting none as neither user is an organizer yet)
            response = client.get('api/user/organizer', headers={"Authorization": "Bearer " + '2'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(0, len(data))

            # 7. Update user 1's data
            self.assertIsNone(user1.profile_picture)  # Check if image is initially None
            response = client.put('api/user/self', 
                                  headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                  data=payload3)
            self.assertEqual(200, response.status_code)
            updated_user1 = User.query.filter_by(firebase_id='1').first()
            self.assertEqual('test.png', updated_user1.profile_picture)
            self.assertEqual('Updated Test1', updated_user1.first_name)
            self.assertEqual('Updated bio 1', updated_user1.bio)

            # 8. Delete user 1
            response = client.delete('api/user/self', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            deleted_user1 = User.query.filter_by(firebase_id='1').first()
            self.assertIsNone(deleted_user1)
            
    
    def test_friends_add_list_delete(self, mock_verify_id_token):
        """Tests adding, listing, and deleting friends for a user."""

        # Sample user data 
        payload1 = json.dumps({
            'first_name': 'Test1',
            'last_name': 'User1',
            'date_of_birth': '1990-01-01',
            'nickname': 'testuser1',
            'bio': 'Test bio 1',
            'hiker_level': 1
        })
        payload2 = json.dumps({
            'first_name': 'Test2',
            'last_name': 'User2',
            'date_of_birth': '1995-05-10',
            'nickname': 'testuser2',
            'bio': 'Test bio 2',
            'hiker_level': 2
        })

        with self.app.test_client() as client:
            # 1. Setup: Create two users
            client.post('api/user/', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, data=payload2)
            client.post('api/user/', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, data=payload1)

            # 2. User 1 befriends user 2
            befriend_payload = json.dumps({'firebase_id': '2'})
            response = client.post('api/user/friends/self', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=befriend_payload)
            self.assertEqual(200, response.status_code)
            friendship = Friends.query.filter_by(user_id='1').first()
            self.assertEqual('2', friendship.friend_id)

            # 3. Show self (user 1) friend list
            response = client.get('api/user/friends/self', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            self.assertEqual('2', data[0]['firebase_id'])

            # 4. Show user 1's friend list (same as above, but using user ID)
            response = client.get('api/user/friends/1', headers={"Authorization": "Bearer " + '2'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            self.assertEqual('2', data[0]['firebase_id'])

            # 5. Delete the friendship
            response = client.delete('api/user/friends/self', 
                                    headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                    data=befriend_payload)
            self.assertEqual(200, response.status_code)
            friendship = Friends.query.filter_by(user_id='1').first()
            self.assertIsNone(friendship)  # Ensure friendship is deleted

    def test_friends_delete_user(self, mock_verify_id_token):
        """Tests if friendships are deleted when a user is deleted."""

        # Sample user data 
        payload1 = json.dumps({
            'first_name': 'Test1',
            'last_name': 'User1',
            'date_of_birth': '1990-01-01',
            'nickname': 'testuser1',
            'bio': 'Test bio 1',
            'hiker_level': 1
        })
        payload2 = json.dumps({
            'first_name': 'Test2',
            'last_name': 'User2',
            'date_of_birth': '1995-05-10',
            'nickname': 'testuser2',
            'bio': 'Test bio 2',
            'hiker_level': 2
        })

        with self.app.test_client() as client:
            # 1. Setup: Create two users and establish a friendship
            client.post('api/user/', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, data=payload2)
            client.post('api/user/', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, data=payload1)
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, data=json.dumps({'firebase_id': '2'}))
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, data=json.dumps({'firebase_id': '1'}))

            # 2. Delete user 1
            response = client.delete('api/user/self', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)

            # 3. Check if friendships related to user 1 are deleted
            friendship1 = Friends.query.filter_by(user_id='1').first()
            self.assertIsNone(friendship1)
            friendship2 = Friends.query.filter_by(user_id='1').first()
            self.assertIsNone(friendship2)
    
    def test_suggested_friends_algorithm(self, mock_verify_id_token):
        """Tests the suggested friends algorithm."""

        # Sample user data
        payload = json.dumps({
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'nickname': 'testuser',
            'bio': 'Test bio',
            'hiker_level': 1
        })

        with self.app.test_client() as client:
            # 1. Add 5 users
            for i in range(1, 6):
                client.post('api/user/', headers={"Content-Type": "application/json", "Authorization": "Bearer " + str(i)}, data=payload)

            # 2. Establish friendships to test the algorithm
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, data=json.dumps({'firebase_id': '2'}))
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, data=json.dumps({'firebase_id': '5'}))
            
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, data=json.dumps({'firebase_id': '1'}))
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, data=json.dumps({'firebase_id': '4'}))
            
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '3'}, data=json.dumps({'firebase_id': '4'}))
            
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '4'}, data=json.dumps({'firebase_id': '2'}))
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '4'}, data=json.dumps({'firebase_id': '3'}))
            
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '5'}, data=json.dumps({'firebase_id': '1'}))
            client.post('api/user/friends/self', headers={"Content-Type": "application/json", "Authorization": "Bearer " + '5'}, data=json.dumps({'firebase_id': '3'}))

            # 3. Retrieve suggested friends for user 1 and assert the results
            response = client.get('api/user/suggestedFriends', headers={"Authorization": "Bearer " + '1'})
            data = json.loads(response.get_data(as_text=True))
            
            # Assert that the response contains the expected suggested friends
            expected_suggested_friends = ['3', '4']  # Based on the established friendships
            actual_suggested_friends = [user['firebase_id'] for user in data]
            
            self.assertEqual(len(expected_suggested_friends), len(actual_suggested_friends))
            self.assertEqual(set(expected_suggested_friends), set(actual_suggested_friends))
            

if __name__ == '__main__':
    unittest.main()