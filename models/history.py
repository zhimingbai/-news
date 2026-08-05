# 历史记录数据模型
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.news import News
from models.users import User


class History(Base):
    """历史记录模型"""

    __tablename__ = "history"

    # 创建索引
    __table_args__ = (
        # 同一用户对同一新闻只保留一条历史记录，重复插入会被数据库拒绝
        UniqueConstraint("user_id", "news_id", name="user_news_unique"),
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
        Index("idx_view_time", "view_time"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="历史ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(News.id), nullable=False, comment="新闻ID"
    )
    view_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False, comment="浏览时间"
    )

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
