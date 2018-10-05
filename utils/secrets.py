import secrets
import string

print( "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(100)) )
