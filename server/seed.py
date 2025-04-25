from app import app, db
from models import Client, Program, Enrollment, User

with app.app_context():
    # Drop everything and recreate tables (optional for testing)
    db.drop_all()
    db.create_all()

    # Create a sample doctor
    doctor = User(username="drmark", full_name="Dr. Mark M.")

    db.session.add(doctor)
    db.session.commit()

    # Create some health programs
    tb = Program(name="Tuberculosis", description="TB program description")
    hiv = Program(name="HIV", description="HIV program description")
    malaria = Program(name="Malaria", description="Malaria program description")

    db.session.add_all([tb, hiv, malaria])
    db.session.commit()

    # Create some clients
    client1 = Client(full_name="Jane Doe", age=32, gender="Female")
    client2 = Client(full_name="John Smith", age=45, gender="Male")

    db.session.add_all([client1, client2])
    db.session.commit()

    # Enroll clients in programs
    enrollment1 = Enrollment(client_id=client1.id, program_id=tb.id)
    enrollment2 = Enrollment(client_id=client1.id, program_id=hiv.id)
    enrollment3 = Enrollment(client_id=client2.id, program_id=malaria.id)

    db.session.add_all([enrollment1, enrollment2, enrollment3])
    db.session.commit()

    print("Database seeded successfully.")
