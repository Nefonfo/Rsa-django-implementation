from django import forms


class RsaEncryptForm(forms.Form):
    content_to_encrypt = forms.FileField(required=True)


class RsaDecryptForm(forms.Form):
    content_to_decrypt = forms.FileField(required=True)