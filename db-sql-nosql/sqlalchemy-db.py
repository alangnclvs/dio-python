# Import necessary SQLAlchemy modules
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, create_engine, ForeignKey, select, func
from sqlalchemy import Integer, String

# Creating the SQLAlchemy base class
Base = declarative_base()


class User(Base):
    """
    Class that represents the "user_account" table
    """

    __tablename__ = "user_account"

    # Define the table columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    # Establishing the relationship between the User and Address classes
    address = relationship(
        "Address", back_populates="user", cascade="all, delete, delete-orphan"
    )

    # Method that returns a string representation of the User class
    def __repr__(self):
        return "User(id={!r}, name={!r}, " "fullname={!r})".format(
            self.id, self.name, self.fullname
        )


class Address(Base):
    """
    Class that represents the "address" table
    """

    __tablename__ = "address"

    # Defining the table columns
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))

    # Establishing the relationship between the Address and User classes
    user = relationship("User", back_populates="address")

    # Method that returns a string representation of the Address class
    def __repr__(self):
        return (
            f"Address(id={self.id!r}, "
            f"email_address={self.email_address!r})"
        )


# Function that creates the engine and the tables
def create_engine_and_tables():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return engine


# Function that inserts data into the database
def insert_users_data(session):
    # Creating the users
    alan = User(
        name="alan",
        fullname="Alan Gonçalves",
        address=[Address(email_address="alan@outlook.com")],
    )

    cristina = User(
        name="cristina",
        fullname="Cristina Yang",
        address=[Address(email_address="cristina@outlook.com")],
    )

    robin = User(
        name="robin",
        fullname="Robin Scherbatsky",
        address=[Address(email_address="robin@outlook.com")],
    )

    # Adding the users to the session
    session.add_all([alan, cristina, robin])
    session.commit()


# Function that retrieves data from the database by name
def retrieve_users_by_name(session):
    statement = session.query(User).filter(
        User.name.in_(["alan", "cristina", "robin"])
    )
    print("Retrieving users by name")
    for user in statement:
        print(user)


# Function that retrieves data from the database by user id
def retrieve_addresses_by_user_id(session, user_id):
    statement_address = session.query(Address).filter(
        Address.user_id == user_id
    )
    print("Retrieving addresses by user id")
    for address in statement_address:
        print(address)


# Function that retrieves data from the database ordered by fullname
def retrieve_users_ordered_by_fullname(session):
    statement_order = session.query(User).order_by(User.fullname.desc())
    print("Retrieving users ordered by fullname")
    for user in statement_order:
        print(user)


# Function that retrieves data joining the User and Address tables
def retrieve_users_and_addresses(session):
    statement_join = session.query(User.fullname, Address.email_address)\
        .join(User)
    print("Retrieving users and addresses")
    for result in statement_join:
        print(result)


# Function that retrieves data joining the tables using connection
def retrieve_users_and_addresses_with_connection(engine):
    with engine.connect() as connection:
        statement_join = select(User.fullname, Address.email_address)\
            .join(User)
        results = connection.execute(statement_join).fetchall()
        print("Running query with connection")
        for result in results:
            print(result)


# Function that retrieves the user count
def retrieve_user_count(session):
    statement_count = session.query(func.count("*")).select_from(User)
    print("Retrieving user count")
    for result in statement_count:
        print(result[0])


# Function that runs the main program
def main():
    engine = create_engine_and_tables()

    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()

    insert_users_data(session)

    retrieve_users_by_name(session)
    retrieve_addresses_by_user_id(session, user_id=2)
    retrieve_users_ordered_by_fullname(session)
    retrieve_users_and_addresses(session)
    retrieve_users_and_addresses_with_connection(engine)
    retrieve_user_count(session)

    session.close()


# Run the main loop
if __name__ == "__main__":
    main()
