import abc
from enum import Enum
import aiosqlite
class AuthPermission(Enum):
    USER = 0        
    MODERATOR = 5       # basic edit permission (category permission needed)
    MODERATOR_USER = 6  # basic edit permission and can grant others permissions (category permission needed)
    EDITOR = 8          # can edit everything and can grant others permissions  (category permission not needed)
    ADMIN = 10          # can do everything

class AuthProvider():
    @abc.abstractmethod
    async def authenticate(self,app,*args,**kwargs):
        pass
    @abc.abstractmethod
    async def authorize(self, username: str, permission: AuthPermission) -> bool:
        pass
    @abc.abstractmethod
    async def needs_credentials(self) -> bool:
        pass

class NoAuth(AuthProvider):
    async def authenticate(self, app, *args,**kwargs) -> bool:
        username = "admin"
        user_id=1
    
        
        
        return  {"username":username,"user_id":user_id}
    async def authorize(self, username: str, permission: AuthPermission) -> bool:
        return True
    async def needs_credentials(self) -> bool:return False