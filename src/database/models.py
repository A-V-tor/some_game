from datetime import datetime

from sqlalchemy import (Boolean, DateTime, Integer, String,
                        func, select, ForeignKey)

from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from src.database.base import Base, async_session_factory


class Player(Base):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[str] = mapped_column(String(100), unique=True)
    last_visit: Mapped[datetime] = mapped_column(DateTime)
    first_visit: Mapped[datetime] = mapped_column(DateTime)
    is_daily_visit: Mapped[bool] = mapped_column(Boolean, default=False)

    player_levels: Mapped[list['PlayerLevel']] = relationship(
        'PlayerLevel', back_populates='player', cascade="all, delete-orphan"
    )
    boosts: Mapped[list['Boost']] = relationship(
        'Boost', back_populates='player', cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'{self.player_id}'

    @classmethod
    async def get_player_by_id(cls, player_id: str):

        async with async_session_factory() as session:
            result = await session.scalar(
                select(cls)
                .where(cls.player_id.contains(player_id))
                .options(
                    selectinload(cls.player_levels)
                    .joinedload(PlayerLevel.level)
                    .selectinload(Level.level_prizes)
                    .joinedload(LevelPrize.prize),
                    selectinload(cls.boosts)
                )
            )
            return result

    @classmethod
    async def get_all_notes(cls):
        async with async_session_factory() as session:
            result = (await session.execute(
                select(cls)
                .options(
                    selectinload(cls.player_levels)
                    .joinedload(PlayerLevel.level)
                    .selectinload(Level.level_prizes)
                    .joinedload(LevelPrize.prize),
                    selectinload(cls.boosts)
                )
            )).scalars().all()

            return result


class Boost(Base):
    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String)

    player_id: Mapped[int] = mapped_column(
        ForeignKey('players.id', ondelete="CASCADE")
    )

    player: Mapped['Player'] = relationship('Player', back_populates='boosts')

    def __str__(self):
        return f'{self.type}'


class Level(Base):
    __tablename__ = 'levels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    order: Mapped[int] = mapped_column(Integer, default=0)

    player_levels: Mapped[list['PlayerLevel']] = relationship(
        'PlayerLevel', back_populates='level', cascade="all, delete-orphan"
    )

    level_prizes: Mapped[list['LevelPrize']] = relationship(
        'LevelPrize', back_populates='level', cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'{self.title}'

    @classmethod
    async def get_level_by_order(cls, order: int):
        async with async_session_factory() as session:
            result = await session.scalar(select(cls).where(cls.order == order))

            return result


class Prize(Base):
    __tablename__ = 'prizes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)

    level_prizes: Mapped[list['LevelPrize']] = relationship(
        'LevelPrize', back_populates='prize', cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'{self.title}'

    @classmethod
    async def get_prize_by_title(cls, title: str):
        async with async_session_factory() as session:
            result = await session.scalar(select(cls).where(cls.title == title))

            return result


class PlayerLevel(Base):
    __tablename__ = 'player_levels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    completed: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(Integer, default=0)

    player_id: Mapped[int] = mapped_column(
        ForeignKey('players.id', ondelete="CASCADE")
    )

    level_id: Mapped[int] = mapped_column(
        ForeignKey('levels.id', ondelete="CASCADE")
    )

    player: Mapped['Player'] = relationship('Player', back_populates='player_levels')
    level: Mapped['Level'] = relationship('Level', back_populates='player_levels')

    def __str__(self):
        return f'{self.player_id} - {self.level_id}'

    @classmethod
    async def create_player_level(cls, player_id: Player, score: int, level_id: int):
        async with async_session_factory() as session:
            new_note = cls(
                completed=datetime.now(),
                player_id=player_id,
                score=score,
                is_completed=True,
                level_id=level_id
            )

            session.add(new_note)

            await session.commit()

            return True


class LevelPrize(Base):
    __tablename__ = 'level_prizes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    received: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    level_id: Mapped[int] = mapped_column(
        ForeignKey('levels.id', ondelete="CASCADE")
    )
    prize_id: Mapped[int] = mapped_column(
        ForeignKey('prizes.id', ondelete="CASCADE")
    )

    level: Mapped['Level'] = relationship('Level', back_populates='level_prizes')

    prize: Mapped['Prize'] = relationship('Prize', back_populates='level_prizes')

    def __str__(self):
        return f'{self.level_id} - {self.prize_id}'






