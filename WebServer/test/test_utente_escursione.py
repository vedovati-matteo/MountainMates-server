import unittest
import json

from app import db
from app.model.utente_escursione import Utente_Escursione
from base import BaseTestCase


class TestUtente_Escursione(BaseTestCase):
    def test_add_utente_Escursione(self):
        payload = json.dumps({
         'id_escursione': ''
    })
        with self.app.test_client() as client:
            response = client.post('/escursione_template/', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(200, response.status_code)
            
        # Then
        utente_escursione = Utente_Escursione.query.filter_by(nome='testName').first()
        self.assertIsNotNone(utente_escursione)
     