import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app.model.escursione_template import EscursioneTemplate
from app.model.utente import Utente
from base import BaseTestCase
from app import db

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
            # Creazione utente come organizzatore
            new_utente = Utente(
                id_firebase='1',
                nome = 'test1',
                cognome = 'test1',
                nickname = 't1',
                data_di_nascita = datetime.strptime('2022-12-15', "%Y-%m-%d").date(),
                bio = 'bio1',
                livello_camminatore = 2,
                flag_organizzatore = True
            )
            db.session.add(new_utente)
            db.session.commit()
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