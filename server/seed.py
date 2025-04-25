from app import app, db
from models import Client, Program, Enrollment, User

with app.app_context():
    # Drop everything and recreate tables (optional for testing)
    db.drop_all()
    db.create_all()

    print("-----------------Seeding Database-------------.")


    # Create a sample doctor
    doctor = User(username="drmark", full_name="Dr Mark Mwangi.")
    doctor.set_password('securepassword123')  # this hashes and sets the password

    db.session.add(doctor)
    db.session.commit()

    print("Doctor seeded successfully.")


    # Sample health programs
    tb = Program(name="Tuberculosis", description="Tuberculosis management and treatment", doctor_id=doctor.id)
    hiv = Program(name="HIV", description="HIV testing and ARV program", doctor_id=doctor.id)
    malaria = Program(name="Malaria", description="Malaria prevention and treatment", doctor_id=doctor.id)

    db.session.add_all([tb, hiv, malaria])
    db.session.commit()
    
    print("Health Programs seeded successfully.")


    # Sample clients
    client1 = Client(full_name="Jane Doe", age=32, gender="Female")
    client2 = Client(full_name="John Smith", age=45, gender="Male")
    client3 = Client(full_name="Alice Wanjiku", age=28, gender="Female")
    client4 = Client(full_name="Johana Otieno", age=34, gender="Male")
    client5 = Client(full_name="Mary Njeri", age=22, gender="Female")



    db.session.add_all([client1, client2, client3, client4, client5])
    db.session.commit()

    print("Clients seeded successfully.")


    # Enroll clients in programs
    enrollment1 = Enrollment(client_id=client1.id, program_id=tb.id)
    enrollment2 = Enrollment(client_id=client1.id, program_id=hiv.id)
    enrollment3 = Enrollment(client_id=client2.id, program_id=malaria.id)

    db.session.add_all([enrollment1, enrollment2, enrollment3])
    db.session.commit()

    print("Enrollments seeded successfully.")

    print("-----------------Database seeded successfully------------------.")

