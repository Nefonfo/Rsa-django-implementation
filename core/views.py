import os
import shutil

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.conf import settings

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

from .forms import RsaEncryptForm, RsaDecryptForm
from .models import RsaKey


# Create your views here.

class RsaEncryptView(LoginRequiredMixin, FormView):
    form_class = RsaEncryptForm
    template_name = 'core/rsa_encrypt.html'

    def form_valid(self, form):
        directory = f'{settings.BASE_DIR}/media/tmp/enc/'
        shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory)

        file_content = self.request.FILES['content_to_encrypt'].read()
        file_out = open(f'{directory}file.rsa', "wb+")

        db_public_key = RsaKey.objects.filter(key_type='PB').first()

        recipient_key = RSA.import_key(db_public_key.content)
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(file_content)
        [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

        return super().form_valid(form)

    def get_success_url(self):
        return '/media/tmp/enc/file.rsa'


class RsaDecryptView(LoginRequiredMixin, FormView):
    form_class = RsaDecryptForm
    template_name = 'core/rsa_decrypt.html'

    def form_valid(self, form):
        file_in = self.request.FILES['content_to_decrypt']

        db_private_key = RsaKey.objects.filter(key_type='PR').first()
        private_key = RSA.import_key(db_private_key.content)

        enc_session_key, nonce, tag, ciphertext = \
            [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        decoded_text = data

        directory = f'{settings.BASE_DIR}/media/tmp/dec/'
        shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory)

        with open(f'{directory}file.txt', "wb+") as text_file:
            text_file.write(decoded_text)

        return super().form_valid(form)

    def get_success_url(self):
        return '/media/tmp/dec/file.txt'
