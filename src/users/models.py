from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from consts import get_created_at_column, get_updated_at_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    created_at: Mapped[datetime] = get_created_at_column()
    updated_at: Mapped[datetime] = get_updated_at_column()
