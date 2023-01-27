import unittest
from unittest.mock import patch
import json

from app.model.utente import Utente
from app.model.amici import Amici
from base import BaseTestCase

@patch('firebase_admin.auth.verify_id_token')
class TestUtenteApi(BaseTestCase):
    def test_utente(self, mock_verify_id_token):
        # Define payloads
        payload1 = json.dumps({
            'nome': 'testName1',
            'cognome': 'testSurname1',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick1',
            'bio': 'testBio1',
            'livello_camminatore': 1
        })
        payload2 = json.dumps({
            'nome': 'testName2',
            'cognome': 'testSurname2',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick2',
            'bio': 'testBio2',
            'livello_camminatore': 2
        })
        payload3 = json.dumps({
            'nome': 'testName1',
            'cognome': 'testSurname1',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick1',
            'bio': 'testBio1',
            'livello_camminatore': 1,
            'img': 'test.png'
        })
        
        with self.app.test_client() as client:
            # Add user 2
            mock_verify_id_token.return_value = {'uid': '2'}
            response = client.post('/utente/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload2)
            self.assertEqual(200, response.status_code)
            utente = Utente.query.filter_by(id_firebase='2').first()
            self.assertIsNotNone(utente)
            # Add user 1
            mock_verify_id_token.return_value = {'uid': '1'}
            response = client.post('/utente/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload1)
            self.assertEqual(200, response.status_code)
            utente = Utente.query.filter_by(id_firebase='1').first()
            self.assertIsNotNone(utente)
            # Show self (1)
            response = client.get('/utente/self', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual('1', data['id_firebase'])
            # Show user 2
            response = client.get('/utente/2', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual('2', data['id_firebase'])
            # Show user list
            response = client.get('/utente/', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(2, len(data))
            # Show organizzetori list
            response = client.get('/utente/organizzatore', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(0, len(data))
            # Update data
            utente = Utente.query.filter_by(id_firebase='1').first()
            self.assertEqual(None, utente.img)
            response = client.put('/utente/self', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload3)
            self.assertEqual(200, response.status_code)
            utente = Utente.query.filter_by(id_firebase='1').first()
            self.assertEqual('test.png', utente.img)
            # Delete user 1
            response = client.delete('/utente/self', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            utente = Utente.query.filter_by(id_firebase='1').first()
            self.assertIsNone(utente)
            
            
    
    def test_amici(self, mock_verify_id_token):
        # Define payloads
        payload1 = json.dumps({
            'nome': 'testName1',
            'cognome': 'testSurname1',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick1',
            'bio': 'testBio1',
            'livello_camminatore': 1
        })
        payload2 = json.dumps({
            'nome': 'testName2',
            'cognome': 'testSurname2',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick2',
            'bio': 'testBio2',
            'livello_camminatore': 2
        })
        payload4 = json.dumps({'id_firebase': '2'})
        
        with self.app.test_client() as client:
            # Setup
            mock_verify_id_token.return_value = {'uid': '2'}
            response = client.post('/utente/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload2)
            mock_verify_id_token.return_value = {'uid': '1'}
            response = client.post('/utente/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload1)
            # Befiend user 2 (1)
            response = client.post('/utente/friendsSelf', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload4)
            self.assertEqual(200, response.status_code)
            amici = Amici.query.filter_by(id_firebase='1').first()
            self.assertEqual('2', amici.id_friend)
            # Show self friend list
            response = client.get('/utente/friendsSelf', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            self.assertEqual('2', data[0]['id_firebase'])
            # Show user 1 friend list
            response = client.get('/utente/friends/1', headers={"Authorization": "Bearer tokenGiusto"})
            self.assertEqual(200, response.status_code)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(1, len(data))
            self.assertEqual('2', data[0]['id_firebase'])
            # Delete fiendship
            response = client.delete('/utente/friendsSelf', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload4)
            self.assertEqual(200, response.status_code)
            amici = Amici.query.filter_by(id_firebase='1').first()
            self.assertIsNone(amici)
    
    def test_amici_delete_utente(self, mock_verify_id_token):
        # Define payloads
        payload1 = json.dumps({
            'nome': 'testName1',
            'cognome': 'testSurname1',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick1',
            'bio': 'testBio1',
            'livello_camminatore': 1
        })
        payload2 = json.dumps({
            'nome': 'testName2',
            'cognome': 'testSurname2',
            'data_di_nascita': '2022-12-15',
            'nickname': 'testNick2',
            'bio': 'testBio2',
            'livello_camminatore': 2
        })
        payload4 = json.dumps({'id_firebase': '2'})
        payload5 = json.dumps({'id_firebase': '1'})
        
        with self.app.test_client() as client:
            # Setup
            mock_verify_id_token.return_value = {'uid': '2'}
            response = client.post('/utente/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload2)
            mock_verify_id_token.return_value = {'uid': '1'}
            response = client.post('/utente/', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload1)
            response = client.post('/utente/friendsSelf', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload4)
            mock_verify_id_token.return_value = {'uid': '2'}
            response = client.post('/utente/friendsSelf', headers={"Content-Type": "application/json", "Authorization": "Bearer tokenGiusto"}, data=payload5)
            mock_verify_id_token.return_value = {'uid': '1'}
            response = client.delete('/utente/self', headers={"Authorization": "Bearer tokenGiusto"})
            # Check fiendship deleted
            amici = Amici.query.filter_by(id_firebase='1').first()
            self.assertIsNone(amici)
            amici = Amici.query.filter_by(id_friend='1').first()
            self.assertIsNone(amici)
        

if __name__ == '__main__':
    unittest.main()