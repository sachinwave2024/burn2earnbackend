from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from trade_admin_auth.views import decrypt_with_common_cipher
from django.conf import settings
from API.SeDGFHte import encrypted_format
import pyotp
from trade_admin_auth.models import AdminUser_Profile,User
class Command(BaseCommand):
    help="Genrate two factor key for admin login in development."
  
    def add_arguments(self, parser: CommandParser):
       parser.add_argument("user_id",type=int)

    def handle(self,*args, **options):
        if(settings.DEBUG):
           user = User.objects.get(pk=options["user_id"])
           get_userprofile = AdminUser_Profile.objects.get(user = user.id)
           if user is not None and get_userprofile is not None:
                authtoken = pyotp.TOTP(get_userprofile.google_id).now()
                return self.stdout.write(self.style.SUCCESS(f"key is genrated successfully. {authtoken}"))
           else:
             return self.stdout.write(self.style.ERROR("user not found."))
        else:
          return self.stdout.write(self.style.WARNING("this command is not availabe in production mode."))  