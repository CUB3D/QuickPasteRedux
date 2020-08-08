from authlib.jose import jwt


class Authenticator:
    async def get_auth_claims(self, request):
        pass

    async def can_access_resource(self, request, resource):
        return False


class UKAuthAuthenticator(Authenticator):
    def __init__(self):
        with open("./public.pem") as kf:
            self.public_key = kf.read()

    async def get_auth_claims(self, request):
        auth_cookie = request.cookies.get('UK_APP_AUTH')
        if auth_cookie is not None:
            return jwt.decode(auth_cookie, self.public_key)
        else:
            return None

    async def can_access_resource(self, request, resource):
        claims = await self.get_auth_claims(request)
        return claims and resource.owner == claims["userId"]


class CookieAuthenticator(Authenticator):
    async def can_access_resource(self, request, resource):
        return resource.security_key == request.cookies.get(f"{resource.note_id}_securityKey")


class BulkAuthenticator(Authenticator):
    def __init__(self, authenticators):
        self.authenticators = authenticators

    async def can_access_resource(self, request, resource):
        for authenticator in self.authenticators:
            if await authenticator.can_access_resource(request, resource):
                return True
        return False
