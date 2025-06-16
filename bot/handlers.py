from db.db import SessionLocal, User, Group, GroupUser, Record, Loan
from sqlalchemy.orm import joinedload
from telegram import Update
from telegram.ext import ContextTypes

async def my_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print(user_id)
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        await update.message.reply_text('You are not registered in the system.')
        session.close()
        return
    groups = session.query(Group).join(GroupUser).filter(GroupUser.user_id == user_id).all()
    if not groups:
        await update.message.reply_text('You are not a member of any groups.')
        session.close()
        return
    response = ''
    total_owed = 0.0
    total_owes = 0.0
    for group in groups:
        group_owed = 0.0
        group_owes = 0.0
        records = session.query(Record).filter_by(group_id=group.id).all()
        for record in records:
            for loan in record.loans:
                if loan.lender_id == user_id:
                    group_owed += loan.amount
                if loan.borrower_id == user_id:
                    group_owes += loan.amount
        response += f'Group: {group.name}\n  You owe: {group_owes}\n  Owed to you: {group_owed}\n\n'
        total_owed += group_owed
        total_owes += group_owes
    response += f'Total you owe: {total_owes}\nTotal owed to you: {total_owed}'
    await update.message.reply_text(response)
    session.close()
