from db.db import SessionLocal, User, Group, GroupUser, Record, Loan
import datetime

def seed_data():
    session = SessionLocal()
    # Clear existing data
    session.query(Loan).delete()
    session.query(Record).delete()
    session.query(GroupUser).delete()
    session.query(Group).delete()
    session.query(User).delete()
    session.commit()

    # Create users
    user1 = User(id=123456789, first_name='Alice', second_name='Smith', username='alice')
    user2 = User(id=43481238, first_name='Egor', second_name='Zuev', username='EgorZuev')
    user3 = User(id=555555555, first_name='Charlie', second_name='Brown', username='charlie')
    session.add_all([user1, user2, user3])
    session.commit()

    # Create group
    group1 = Group(name='Trip to Paris', description='Expenses for Paris trip')
    session.add(group1)
    session.commit()

    # Add users to group
    session.add_all([
        GroupUser(group_id=group1.id, user_id=user1.id),
        GroupUser(group_id=group1.id, user_id=user2.id),
        GroupUser(group_id=group1.id, user_id=user3.id)
    ])
    session.commit()

    # Create a record (bill)
    record1 = Record(group_id=group1.id, datetime=datetime.datetime.utcnow(), comment='Hotel')
    session.add(record1)
    session.commit()

    # Add loans (Alice paid for hotel, Bob and Charlie owe her)
    loan1 = Loan(record_id=record1.id, lender_id=user1.id, borrower_id=user2.id, amount=100.0, currency='EUR', category='accommodation')
    loan2 = Loan(record_id=record1.id, lender_id=user1.id, borrower_id=user3.id, amount=100.0, currency='EUR', category='accommodation')
    session.add_all([loan1, loan2])
    session.commit()

    print('Seed data added!')
    session.close()

if __name__ == '__main__':
    seed_data()
