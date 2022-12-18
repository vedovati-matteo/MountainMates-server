import unittest
import json

from app import db
from app.model.escursione import Escursione
from base import BaseTestCase

class TestEscursione_template(BaseTestCase):
    def test_add_escursione_completa(self):
        payload = json.dumps({
        'id_escursione':1,
        'id_escursione_template': 1,
        'orario_ritrovo': "",
        'data': "",
        'max_participant':1,
        'organizzatori': []
    })
        with self.app.test_client() as client:
            response = client.post('/escursione_template/', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(200, response.status_code)
            
        # Then
        escursione = Escursione.query.filter_by(nome='testName').first()
        self.assertIsNotNone(escursione)
        
    def test_add_escursione(self):
        payload = json.dumps({
        'id_escursione': 1,
        'id_escursione_template': 1,
        'orario_ritrovo': "",
        'data': "",
        'max_participant': 1,
        'organizzatori': []
        })
        with self.app.test_client() as client:
            response = client.post('/escursione/', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(200, response.status_code)
            
        # Then
        escursione = Escursione.query.filter_by(nome='testName').first()
        self.assertIsNotNone(escursione) 

    def test_add_escursione_Org(self):
        payload = json.dumps({
        'id_escursione': 1,
        'id_escursione_template':1,
        'orario_ritrovo': "",
        'data': "",
        'max_participant':1,
        'organizzatori': []
        })

        with self.app.test_client() as client:
            response = client.post('/escursione/', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(200, response.status_code)
            
        # Then
        escursione = Escursione.query.filter_by(nome='testName').first()
        self.assertIsNotNone(escursione)


if __name__ == '__main__':
    unittest.main()