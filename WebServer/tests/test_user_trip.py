import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app import db
from app.model.user_trip import UserTrip  # Adjust if your model name is different
from app.model.user import User
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestUserTrip(BaseTestCase):
    """Tests for the 'UserTrip' relationship (user joining a trip)."""

    def test_user_trip(self, mock_verify_id_token):
        """Tests adding, listing, updating, and deleting a 'UserTrip' relationship."""

        # Mock Firebase authentication to simulate a logged-in user
        mock_verify_id_token.return_value = {'uid': '1'}

        # Sample user and trip data as JSON payloads
        user_payload = json.dumps({
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'nickname': 'testuser',
            'bio': 'Test bio',
            'hiker_level': 2
        })
        trip_payload = json.dumps({
            'name': 'Test Trip',
            'province': 'BG',
            'starting_point': 'Test Start',
            'map_link': 'https://testmap.com',
            'elevation_gain': 500,
            'distance': 10.5,
            'estimated_time': '4 hours',
            'min_altitude': 800,
            'max_altitude': 1200,
            'difficulty': 3,
            'required_tools': 'Hiking boots, backpack',
            'path_description': 'Scenic trail with moderate climbs.',
            'image': 'https://testimage.com/trip.jpg',
            "meeting_time": "09:00 AM",
            "date": "2023-12-25",
            "max_participants": 10
        })

        with self.app.test_client() as client:
            # 1. Create a user and organizer
            response = client.post('api/user/', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=user_payload)
            self.assertEqual(200, response.status_code)
            
            new_user = User(
                firebase_id='2',
                first_name='TestOrg',
                last_name='User',
                nickname='testuserOrg',
                date_of_birth=datetime.strptime('1990-01-01', "%Y-%m-%d").date(),
                bio='Test bio',
                hiker_level=2,
                is_organizer=True
            )
            db.session.add(new_user)
            db.session.commit()

            # 2. Create a trip (without a template) 
            response = client.post('api/trip/noTemplate', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '2'}, 
                                   data=trip_payload)
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            trip_id = data['trip_id']

            # 3. Add the user to the trip (create a UserTrip relationship)
            join_trip_payload = json.dumps({'trip_id': trip_id})
            response = client.post('api/registration/user/self',  # Adjust endpoint if needed
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=join_trip_payload)
            self.assertEqual(200, response.status_code)
            user_trip = UserTrip.query.filter_by(user_id='1', trip_id=trip_id).first()
            self.assertIsNotNone(user_trip)

            # 4. Show list of trips the user is enrolled in
            response = client.get('api/registration/user/self', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

            # 5. Show list of users enrolled in the trip
            response = client.get(f'api/registration/trip/{trip_id}', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

            # 6. Update the user's enrollment status (e.g., mark as completed)
            update_payload = json.dumps({
                'trip_id': trip_id,
                'status': 2,  # Assuming 2 represents 'completed'
                'rating': 4 
            })
            response = client.put('api/registration/user/self', 
                                  headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                  data=update_payload)
            self.assertEqual(200, response.status_code)
            updated_user_trip = UserTrip.query.filter_by(user_id='1', trip_id=trip_id).first()
            self.assertEqual(2, updated_user_trip.status)

            # 7. Delete the user's enrollment from the trip
            response = client.delete('api/registration/user/self', 
                                    headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                    data=join_trip_payload)
            self.assertEqual(200, response.status_code)
            user_trip = UserTrip.query.filter_by(user_id='1', trip_id=trip_id).first()
            self.assertIsNone(user_trip)

if __name__ == '__main__':
    unittest.main()