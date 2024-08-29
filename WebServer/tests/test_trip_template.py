import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app import db
from app.model.trip_template import TripTemplate 
from app.model.user import User
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestTripTemplate(BaseTestCase):
    """Tests for Trip Template related API endpoints."""

    def test_trip_template(self, mock_verify_id_token):
        """Tests creating, retrieving, listing, and deleting a trip template."""

        # Mock Firebase authentication to simulate a logged-in user
        mock_verify_id_token.return_value = {'uid': '1'}

        # Sample trip template data as JSON payload
        payload = json.dumps({
            'name': 'Test Trip',
            'province': 'BG',
            'starting_point': 'Test Start',
            'map_link': 'https://testmap.com',
            'elevation_gain': 500,
            'distance': 10.5,
            'estimated_time': '4 hours',
            'min_altitude': 800,
            'max_altitude': 1200,
            'difficulty': 3,  # Moderate difficulty
            'required_tools': 'Hiking boots, backpack',
            'path_description': 'Scenic trail with moderate climbs.',
            'image': 'https://testimage.com/trip.jpg'
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

            # 1. Add a new trip template
            response = client.post('api/trip_template/', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=payload)
            
            self.assertEqual(200, response.status_code)  # Expect successful creation
            data = json.loads(response.get_data(as_text=True))
            template_id = data['trip_template_id']
            trip_template = TripTemplate.query.filter_by(trip_template_id=template_id).first()
            self.assertIsNotNone(trip_template)  # Ensure the template was created in the database

            # 2. Show the created trip template
            response = client.get(f'api/trip_template/{template_id}', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(template_id, data['trip_template_id'])

            # 3. Show list of all trip templates
            response = client.get('api/trip_template/', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))  # Expect one template in the list

            # 4. Delete the trip template
            response = client.delete(f'api/trip_template/{template_id}', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            trip_template = TripTemplate.query.filter_by(trip_template_id=template_id).first()
            self.assertIsNone(trip_template)  # Ensure the template was deleted from the database

if __name__ == '__main__':
    unittest.main()