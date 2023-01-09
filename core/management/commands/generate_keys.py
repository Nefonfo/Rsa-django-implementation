from django.core.management.base import BaseCommand

from Crypto.PublicKey import RSA

from core.models import RsaKey

class Command(BaseCommand):
    help = 'Generates RSA keys and save it on the database'

    def handle(self, *args, **options):
        key = RSA.generate(2048)
        private_key = key.export_key().decode('utf-8')
        public_key = key.publickey().export_key().decode('utf-8')
        RsaKey.objects.all().delete()
        RsaKey(
            key_type='PB',
            content=public_key
        ).save()

        RsaKey(
            key_type='PR',
            content=private_key
        ).save()

        self.stdout('--- KEYS CREATED SUCCESSFULLY ---')
