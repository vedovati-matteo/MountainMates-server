import unittest
from unittest.mock import patch
import json

from app.model.escursione_template import EscursioneTemplate
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestEscursione_template(BaseTestCase):
    def test__escursione_template(self, mock_verify_id_token):
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
            'img':'testImg'
        })
        
        with self.app.test_client() as client:
            # Add escursione template 1
            response = client.post('/escursione_template/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload1)
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            id = data['id_escursione_template']
            escursione_template = EscursioneTemplate.query.filter_by(id_escursione_template=id).first()
            self.assertIsNotNone(escursione_template)
            # Show escursione template 1
            response = client.get('/escursione_template/' + id, headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(id, data['id_escursione_template'])
            # Show escursione template list
            response = client.get('/escursione_template/', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            # Delete escursione template 1
            response = client.delete('/escursione_template/' + id, headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            escursione_template = EscursioneTemplate.query.filter_by(id_escursione_template=id).first()
            self.assertIsNone(escursione_template)

if __name__ == '__main__':
    unittest.main()