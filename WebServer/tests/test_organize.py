import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app import db
from app.model.organize import Organize
from app.model.user import User
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestOrganizes(BaseTestCase):
    """Tests for the 'Organizes' relationship between users and trips."""

    def test_organizes(self, mock_verify_id_token):
        """Tests adding, listing, and deleting an 'Organizes' relationship."""

        # Mock Firebase authentication to simulate a logged-in user
        mock_verify_id_token.return_value = {'uid': '1'}

        # Sample trip data as JSON payload
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
            # Create a user as an organizer
            new_user = User(
                firebase_id='1',
                first_name='Test',
                last_name='User',
                nickname='testuser',
                date_of_birth=datetime.strptime('1990-01-01', "%Y-%m-%d").date(),
                bio='Test bio',
                hiker_level=2,
                is_organizer=True
            )
            db.session.add(new_user)
            db.session.commit()

            # Create a trip (without a template) to establish an 'Organizes' relationship with
            response = client.post('api/trip/noTemplate', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=trip_payload)
            data = json.loads(response.get_data(as_text=True))
            trip_id = data['trip_id']

            # 1. Add an organizer to the trip
            organizer_payload = json.dumps({'trip_id': trip_id})
            response = client.post(f'api/organize/user/1', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=organizer_payload)
            self.assertEqual(200, response.status_code)
            organizes_relationship = Organize.query.filter_by(organizer_id='1', trip_id=trip_id).first()
            self.assertIsNotNone(organizes_relationship)

            # 2. Show list of trips organized by the user
            response = client.get('api/organize/user/1', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

            # 3. Show list of organizers for the trip
            response = client.get(f'api/organize/trip/{trip_id}', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

            # 4. Delete the 'Organizes' relationship
            response = client.delete(f'api/organize/user/1', 
                                    headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                    data=organizer_payload)
            self.assertEqual(200, response.status_code)
            organizes_relationship = Organize.query.filter_by(organizer_id='1', trip_id=trip_id).first()
            self.assertIsNone(organizes_relationship)

if __name__ == '__main__':
    unittest.main()