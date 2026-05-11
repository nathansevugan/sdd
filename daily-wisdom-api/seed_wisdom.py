import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.models.wisdom import WisdomEntry
from src.core.config import settings

async def seed_wisdom():
    engine = create_async_engine(settings.database_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        wisdom_entries = [
            WisdomEntry(
                title="The only way to do great work is to love what you do.",
                description="Passion is the key to excellence and fulfillment in your work."
            ),
            WisdomEntry(
                title="Innovation distinguishes between a leader and a follower.",
                description="True leadership comes from creating new paths, not following existing ones."
            ),
            WisdomEntry(
                title="Stay hungry, stay foolish.",
                description="Maintain curiosity and embrace the unknown throughout your journey."
            ),
            WisdomEntry(
                title="The future belongs to those who believe in the beauty of their dreams.",
                description="Your dreams have the power to shape your reality when you pursue them with conviction."
            ),
            WisdomEntry(
                title="It does not matter how slowly you go as long as you do not stop.",
                description="Persistence and consistency are more important than speed in achieving long-term goals."
            ),
            WisdomEntry(
                title="The best time to plant a tree was 20 years ago. The second best time is now.",
                description="Don't wait for the perfect moment - take action today and create your future."
            ),
            WisdomEntry(
                title="Success is not final, failure is not fatal: it is the courage to continue that counts.",
                description="True success lies in your resilience and willingness to keep moving forward."
            ),
            WisdomEntry(
                title="The only impossible journey is the one you never begin.",
                description="Every great achievement starts with the decision to try."
            ),
            WisdomEntry(
                title="In the middle of difficulty lies opportunity.",
                description="Challenges are not obstacles but chances for growth and innovation."
            ),
            WisdomEntry(
                title="Be yourself; everyone else is already taken.",
                description="Authenticity is your greatest strength in a world that rewards conformity."
            )
        ]
        
        for wisdom in wisdom_entries:
            session.add(wisdom)
        
        await session.commit()
        print(f"Seeded {len(wisdom_entries)} wisdom entries")

if __name__ == "__main__":
    asyncio.run(seed_wisdom())
