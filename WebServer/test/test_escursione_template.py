import unittest
import json

from app import db
from app.model.escursione_template import EcursioneTemplate
from base import BaseTestCase

class TestEscursione_template(BaseTestCase):
    def test_add_escursione_template(self):
        payload = json.dumps({
            
        })