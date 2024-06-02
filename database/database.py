from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from orm.model import Model

engine = create_async_engine(
    'sqlite+aiosqlite:///recipes.db'
)
session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Model.metadata.drop_all)
