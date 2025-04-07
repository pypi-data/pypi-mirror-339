from typing import Optional
from pydantic import BaseModel

class Profile(BaseModel):
    username: str
    first_name: str
    is_online: Optional[bool] = False
    is_verified: Optional[bool] = False
    credibility_score: Optional[float] = 0.0 
    email: str
    bio: Optional[str] = None