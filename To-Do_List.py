from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="task")
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_to_list(date, to_do):
    to_complete = Table(task=to_do, deadline=datetime.strptime(date, '%Y-%m-%d'))
    session.add(to_complete)
    session.commit()


def print_today(date_today):
    rows = session.query(Table).filter(Table.deadline == date_today.date()).all()
    print("Today {} {}:".format(date_today.strftime('%b'), date_today.strftime('%d')))
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for i in rows:
            print(i.task)


def print_week():
    off_set = 0
    while off_set < 7:
        check_day = datetime.today() + timedelta(days=off_set)
        rows = session.query(Table).filter(Table.deadline == check_day.date()).all()
        print("")
        print("{} {} {}:".format(check_day.strftime('%A'), check_day.strftime('%b'), check_day.strftime('%d')))
        if len(rows) == 0:
            print("Nothing to do!")
            print("")
        else:
            for i in rows:
                print(i.task)
            print("")
        off_set += 1


def print_all():
    rows = session.query(Table).order_by(Table.deadline).all()
    counter = 1
    for i in rows:
        print("{}. {} {} {}".format(str(counter), i.task, i.deadline.day, i.deadline.strftime('%b')))
        counter += 1
    print("")


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    counter = 1
    print("Missed tasks:")
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for i in rows:
            print("{}. {} {} {}".format(str(counter), i.task, i.deadline.day, i.deadline.strftime('%b')))
            counter += 1
    print("")


def delete_task():
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    counter = 1
    if len(rows) == 0:
        print("Nothing to delete")
    else:
        print("Choose the number of the task you want to delete:")
        for i in rows:
            print("{}. {} {} {}".format(str(counter), i.task, i.deadline.day, i.deadline.strftime('%b')))
            counter += 1
        decision = int(input()) - 1
        specific_row = rows[decision]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")
    print("")



print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
choice = input()
while choice != "0":
    if choice == "1":
        print_today(datetime.today())
    elif choice == "2":
        print_week()
    elif choice == "3":
        print_all()
    elif choice == "4":
        missed_tasks()
    elif choice == "5":
        print("Enter task")
        task_to_do = input()
        print("Enter deadline")
        when_due = input()
        add_to_list(when_due, task_to_do)
        print("The task has been added!")
    elif choice == "6":
        delete_task()
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    choice = input()
print("Bye!")
