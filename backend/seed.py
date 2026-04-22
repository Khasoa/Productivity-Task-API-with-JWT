"""
Seed script — populates the database with sample users and tasks.
Run with: python seed.py
"""
from faker import Faker
from app import create_app, db
from app.models import User, Task

fake = Faker()

app = create_app()

with app.app_context():
    # Clear existing data (order matters for FK constraints)
    print("Clearing old data...")
    Task.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding users and tasks...")

    priorities = ["Low", "Medium", "High"]

    for i in range(3):
        user = User(username=fake.user_name() + str(i))
        user.set_password("password123")  # Same password for easy Postman testing
        db.session.add(user)
        db.session.flush()  # Get user.id before committing

        # Give each user 5 tasks
        for _ in range(5):
            task = Task(
                title=fake.sentence(nb_words=4),
                description=fake.sentence(nb_words=10),
                completed=fake.boolean(),
                priority=fake.random_element(priorities),
                user_id=user.id
            )
            db.session.add(task)

    db.session.commit()
    print("✅ Seeded 3 users with 5 tasks each.")
    print("Password for all users: password123")