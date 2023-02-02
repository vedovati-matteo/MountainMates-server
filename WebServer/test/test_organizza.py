import unittest
from unittest.mock import patch
import json
from datetime import datetime

from app import db
from app.model.organizza import Organizza
from app.model.utente import Utente
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestOrganizza(BaseTestCase):
    def test_organizza(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {'uid': '1'}
        payload2 = json.dumps({
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
            # SetUp
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
            
            response = client.post('/escursione/noTemplate', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload2)
            data = json.loads(response.get_data(as_text=True))
            id = data['id_escursione']
            # Add organizzatore
            payload3 = json.dumps({
                'id_escursione': id
            })
            response = client.post('/organizza/utente/1', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload3)
            self.assertEqual(200, response.status_code)
            iscrizione = Organizza.query.filter_by(id_organizzatore='1', id_escursione=id).first()
            self.assertIsNotNone(iscrizione)
            # Show lista organizzazioni
            response = client.get('/organizza/utente/1', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            # Show list organizzatori escursione
            response = client.get('/organizza/escursione/'+id, headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            # Delete iscrizione
            response = client.delete('/organizza/utente/1', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload3)
            self.assertEqual(200, response.status_code)
            iscrizione = Organizza.query.filter_by(id_organizzatore='1', id_escursione=id).first()
            self.assertIsNone(iscrizione)
        

if __name__ == '__main__':
    unittest.main()