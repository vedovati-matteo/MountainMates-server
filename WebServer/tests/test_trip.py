import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app import db
from app.model.trip import Trip
from app.model.trip_template import TripTemplate
from app.model.user import User
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestTrip(BaseTestCase):
    """Tests for Trip related API endpoints."""

    def test_trip_creation_and_retrieval(self, mock_verify_id_token):
        """Tests creating, retrieving, listing, updating, and deleting a trip."""

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
            # Create a user as an organizer (required for creating trips)
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

            # 1. Create a new trip (without a template)
            response = client.post('api/trip/noTemplate', 
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                   data=trip_payload)
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            trip_id = data['trip_id']
            trip = Trip.query.filter_by(trip_id=trip_id).first()
            self.assertIsNotNone(trip)

            # 2. Retrieve the created trip
            response = client.get(f'api/trip/{trip_id}', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(trip_id, data['trip_id'])

            # 3. List all trips 
            response = client.get('api/trip/', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))

            # 4. Update the trip (example: change the max_participants)
            updated_payload = json.dumps({'max_participants': 15})
            response = client.put(f'api/trip/{trip_id}', 
                                  headers={"Content-Type": "application/json", "Authorization": "Bearer " + '1'}, 
                                  data=updated_payload)
            self.assertEqual(200, response.status_code)
            updated_trip = Trip.query.filter_by(trip_id=trip_id).first()
            self.assertEqual(15, updated_trip.max_participants)

            # 5. Delete the trip
            response = client.delete(f'api/trip/{trip_id}', headers={"Authorization": "Bearer " + '1'})
            self.assertEqual(200, response.status_code)
            deleted_trip = Trip.query.filter_by(trip_id=trip_id).first()
            self.assertIsNone(deleted_trip)

if __name__ == '__main__':
    unittest.main()