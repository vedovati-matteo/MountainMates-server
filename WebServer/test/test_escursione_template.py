import unittest
import json

from app import db
from app.model.escursione_template import EcursioneTemplate
from base import BaseTestCase

class TestEscursione_template(BaseTestCase):
    def test_add_escursione_template(self):
        payload = json.dumps({
        'nome': '',
        'provincia':'',
        'partenza':'',
        'mapLink': '',
        'dislivello': 1, 
        'distanza': 1,
        'tempo_stimato': '',
        'altezza_min':1 ,
        'altezza_max':1,
        'difficulty': 1,
        'strumenti_richiesti':'',
        'descrizione_percorso':'',
        'img':''
    })
        with self.app.test_client() as client:
            response = client.post('/escursione_template/', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(200, response.status_code)
            
        # Then
        escursione_template = EcursioneTemplate.query.filter_by(nome='testName').first()
        self.assertIsNotNone(escursione_template)
        

if __name__ == '__main__':
    unittest.main()