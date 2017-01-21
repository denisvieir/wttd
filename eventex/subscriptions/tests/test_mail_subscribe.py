from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Denis Vieira", cpf="12345678901",
                    email="denisvieira@me.com", phone="11-99241-4041")
        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'denisvieira@me.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        contents = ['Denis Vieira',
                    '12345678901',
                    'denisvieira@me.com',
                    '11-99241-4041'
                    ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

        self.assertIn('Denis Vieira', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('denisvieira@me.com', self.email.body)
        self.assertIn('11-99241-4041', self.email.body)