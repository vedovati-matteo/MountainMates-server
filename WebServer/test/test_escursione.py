import unittest
from unittest.mock import patch
import json

from app import db
from app.model.escursione import Escursione
from app.model.escursione_template import EscursioneTemplate
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestEscursione_template(BaseTestCase):
    def test_escursione(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'uid': '1'}
        payload1 = json.dumps({
            'nome': 'testNome',
            'provincia':'BG',
            'partenza':'testPartenza',
            'mapLink': 'testMap',
            'dislivello': 1, 
            'distanza': 1.1,
            'tempo_stimato': '3 ore e mezza',
            'altezza_min':1 ,
            'altezza_max':1,
            'difficulty': 1,
            'strumenti_richiesti':'test1, test2',
            'descrizione_percorso':'test',
            'img':'testImg',
            "orario_ritrovo": "testOrario",
            "data": "2023-01-26",
            "numero_max": 2
        })
        
        
        
        with self.app.test_client() as client:
            # Add escursione 1 (no template)
            response = client.post('/escursione/noTemplate', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload1)
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            id = data['id_escursione']
            escursione = Escursione.query.filter_by(id_escursione=id).first()
            self.assertIsNotNone(escursione)
            id_template = escursione.id_escursione_template
            escursione_template = EscursioneTemplate.query.filter_by(id_escursione_template=id_template).first()
            self.assertIsNotNone(escursione_template)
            # Add escursione 2 (with template)
            payload2 = json.dumps({
                "id_escursione_template": id_template,
                "orario_ritrovo": "testOrario2",
                "data": "2023-01-27",
                "numero_max": 2
            })
            response = client.post('/escursione/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload2)
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            id = data['id_escursione']
            escursione = Escursione.query.filter_by(id_escursione=id).first()
            self.assertIsNotNone(escursione)
            # Show escursione 2
            response = client.get('/escursione/' + id, headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(id, data['id_escursione'])
            # Show escursione list
            response = client.get('/escursione/', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(2, len(data))
            # Show escursione template list
            response = client.get('/escursione/fromTemplate/' + id_template, headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(2, len(data))
            # Update escursione 2
            payload3 = json.dumps({
                "id_escursione_template": id_template,
                "orario_ritrovo": "testOrario",
                "data": "2023-01-26",
                "numero_max": 1
            })
            response = client.put('/escursione/' + id, headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload3)
            self.assertEqual(200, response.status_code)
            escursione = Escursione.query.filter_by(id_escursione=id).first()
            self.assertEqual(1, escursione.numero_max)
            # Delete escursione 2
            response = client.delete('/escursione/' + id, headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            escursione = Escursione.query.filter_by(id_escursione=id).first()
            self.assertIsNone(escursione)


if __name__ == '__main__':
    unittest.main()