from typing import Any
from django.core.management.base import BaseCommand
from trade_admin_auth.views import decrypt_with_common_cipher
from django.conf import settings
from API.SeDGFHte import encrypted_format
import pyotp

class Command(BaseCommand):
    help="Genrate auth key for admin login in development."

    def handle(self,*args, **options):
        if(settings.DEBUG):
         key  = pyotp.TOTP(decrypt_with_common_cipher(encrypted_format)).now()
         return self.stdout.write(f'taf key is genrated...{key}')
        else:
          return self.stdout.write(self.style.WARNING("this command is not availabe in production mode."))  