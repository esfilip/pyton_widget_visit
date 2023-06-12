import datetime
from typing import Any
from typing import Optional
from sqlalchemy import Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from datetime import datetime, date
from sqlalchemy import ForeignKey, null
from sqlalchemy.orm import  mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "fos_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    def __repr__(self) -> str:
        return f"User(id={self.id!r})"
    
class WidgetVisit(Base):
    __tablename__ = "widget_visit"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("fos_user.id"))
    widget_type: Mapped[str] # can be HashtagAlbum or Widget
    widget_ref:	Mapped[str]
    request_url: Mapped[str] = mapped_column(Text)
    visits: Mapped[int] = mapped_column(default=0)
    visits_date: Mapped[datetime]		
    created_on: Mapped[Optional[datetime]] = mapped_column(default=null)
    updated_on: Mapped[Optional[datetime]] = mapped_column(default=null)	
    status: Mapped[bool] = mapped_column(default=null)

    def __init__(self, owner_id, widget_type, widget_ref, request_url, visits_date):
        self.owner_id = owner_id
        self.widget_type = widget_type
        self.widget_ref = widget_ref
        self.request_url = request_url
        self.visits_date = visits_date

    def __repr__(self) -> str:
        return f"WidgetVisit(id={self.id!r}, owner_id={self.owner_id!r}, widget_type={self.widget_type!r}, widget_ref={self.widget_ref!r}, request_url={self.request_url!r}, visits={self.visits!r}, visits_date={self.visits_date!r}, created_on={self.created_on!r}, updated_on={self.updated_on!r}, status={self.status!r})"