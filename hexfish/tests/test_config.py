
import uuid
import unittest

from hexfish.config import Config


class TestConfig(unittest.TestCase):
    def test_get(self):
        config = Config()
        self.assertEqual(config.get(('nick', config.create_id(), 'cipher')), 'blowcrypt')
        self.assertEqual(config.get(('nick_id', '*default')), str(uuid.UUID(int=0)))
        with self.assertRaises(KeyError):
            config.get(('nick', config.create_id(), 'does_not_exist'))
        with self.assertRaises(KeyError):
            config.get(('nick_id', 'does_not_exist'))

    def test_set(self):
        config = Config()
        config.set(('nick', config.create_id(), 'cipher'), 'blowcrypt')
        self.assertEqual(config.config, {})

        config = Config()
        id_ = config.create_id()
        config.set(('nick', id_, 'cipher'), 'some_other_cipher')
        self.assertEqual(config.config, {'nick': {id_: {'cipher': 'some_other_cipher'}}})