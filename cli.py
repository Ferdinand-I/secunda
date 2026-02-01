import asyncio
import csv
import sys
from pathlib import Path

import click
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from storage.database.models.building import Building
from storage.database.models.activity import Activity
from storage.database.models.organization_activity import organization_activity
from storage.database.models.organization import Organization
from core.settings import settings


DATA_PATH = "data"


async def seed_db() -> None:
    engine = create_async_engine(settings.db.url.render_as_string(hide_password=False), echo=True)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        # --- Buildings ---
        with open(f"{DATA_PATH}/buildings.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                session.add(
                    Building(
                        id=int(row["id"]),
                        address=row["address"],
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                    )
                )

        await session.flush()

        # --- Activities ---
        with open(f"{DATA_PATH}/activities.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                parent_id = int(row["parent_id"]) if row["parent_id"] else None
                session.add(Activity(id=int(row["id"]), name=row["name"], parent_id=parent_id))

        await session.flush()

        # --- Organizations ---
        with open(f"{DATA_PATH}/organizations.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                phones = row["phones"].split(";") if row["phones"] else []
                session.add(
                    Organization(
                        id=int(row["id"]), name=row["name"], building_id=int(row["building_id"]), phones=phones
                    )
                )

        await session.flush()

        # --- M2M organizations_activities ---
        with open(f"{DATA_PATH}/organizations_activities.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                await session.execute(
                    organization_activity.insert().values(
                        organization_id=int(row["organization_id"]), activity_id=int(row["activity_id"])
                    )
                )

        await session.commit()
        print("✅ Test data seeded successfully!")


@click.command()
def main():
    asyncio.run(seed_db())


if __name__ == "__main__":
    main()
