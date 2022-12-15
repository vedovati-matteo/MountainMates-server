import unittest
import json

from app import db
from app.model.utente import Utente
from base import BaseTestCase

class TestUtenteApi(BaseTestCase):
    def test_add_user(self):
        # Given
        payload = json.dumps({
            'nome': 'testName',
            'cognome': 'testSurname',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick',
            'bio': 'testBio',
            'livello_camminatore': 1
        })
        # When
        with self.app.test_client() as client:
            response = client.post('/utente/', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(200, response.status_code)
            
        # Then
        utente = Utente.query.filter_by(nome='testName').first()
        self.assertIsNotNone(utente)
        

if __name__ == '__main__':
    unittest.main()