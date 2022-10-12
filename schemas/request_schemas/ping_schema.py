from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class PingRequest(BaseModel):
    text: str