import mysql.connector

# Establish a connection to the database


def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_new_password',
        database='flight_management_system'
    )
    cursor = connection.cursor()
    return connection, cursor

# Close the cursor and connection


def close_connection(cursor, connection):
    cursor.close()
    connection.close()

# Function to execute SQL queries


def execute_query(query):
    connection, cursor = create_connection()
    if connection and cursor:
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
        finally:
            close_connection(cursor, connection)
    else:
        print("Failed to connect to the database.")

# Function for Retrieve Operations


def retrieve_operations():
    print("\nRetrieve Operations:")
    print("1. Retrieve a list of all passengers who made reservations on a specific flight.")
    print("2. Retrieve a list of all flights departing from a specific location on a given date.")
    print("3. Retrieve a list of all aircraft that require maintenance within the next week.")
    print("4. Retrieve the reservation ID and passenger name for baggage tracking.")
    print("5. Retrieve the name and phone number of employees for a particular flight to check for incidents during their shifts.")
    print("6. Retrieve the name and airport code of locations to display in a flight schedule.")
    print("7. Retrieve the aircraft’s unique ID and assigned flight and airplane model name for tracking purposes.")
    print("8. Passenger Loyalty Program")
    print("9. Search Operations")
    print("0. Back to Main Menu")

    choice = input("Enter your choice (0-9): ")

    if choice == '1':
        specific_flight_id = input("Enter the specific flight ID: ")
        query = f"""
            SELECT Passenger.*
            FROM Passenger
            JOIN Reservation ON Passenger.passenger_id = Reservation.passenger_id
            WHERE Reservation.flight_id = '{specific_flight_id}';
        """
        execute_query(query)

    elif choice == '2':
        specific_location = input("Enter the specific location: ")
        given_date = input("Enter the given date (YYYY-MM-DD): ")
        query = f"""
            SELECT Flight.*
            FROM Flight
            WHERE Flight.from_location = '{specific_location}'
            AND DATE(Flight.arrival_departure_time) = '{given_date}';
        """
        execute_query(query)

    elif choice == '3':
        query = """
            SELECT Airplane.*
            FROM Airplane
            JOIN Maintenance_History ON Airplane.airplane_number = Maintenance_History.airplane_number
            WHERE Maintenance_History.date BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY;
        """
        execute_query(query)
    elif choice == '4':
        query = """
            SELECT Reservation.id, Passenger.name, Baggage.tag_index
            FROM Reservation
            JOIN Passenger ON Reservation.passenger_id = Passenger.passenger_id
            JOIN Baggage ON Passenger.passenger_id = Baggage.passenger_id;
        """
        execute_query(query)
    elif choice == '5':
        specific_flight_id = input("Enter the specific flight ID: ")
        query = f"""
            SELECT Employee.e_name, Employee.phone_number
            FROM Employee
            JOIN Flight ON Employee.employee_id = Flight.id
            WHERE Flight.id = '{specific_flight_id}';
        """
        execute_query(query)
    elif choice == '6':
        specific_flight_id = input("Enter the specific flight ID: ")
        # Retrieve the arrivial and departure along with the time and location for that flight
        query = f"""
            SELECT Flight.arrival_departure_time, Flight.from_location, Flight.to_location
            FROM Flight
            WHERE Flight.id = '{specific_flight_id}';
        """
        execute_query(query)
    elif choice == '7':
        query = """
            SELECT Airplane.airplane_number, Flight.id, Airplane.airplane_model
            FROM Airplane
            JOIN Flight ON Airplane.airplane_number = Flight.airplane_number;
        """
        execute_query(query)

    elif choice == '8':
        query = """
            SELECT Passenger.passenger_id, COUNT(Reservation.id) AS reservation_count
            FROM Passenger
            JOIN Reservation ON Passenger.passenger_id = Reservation.passenger_id
            GROUP BY Passenger.passenger_id
            HAVING COUNT(Reservation.id) > 5;  # Assuming loyalty starts after 5 reservations
        """
        execute_query(query)

    elif choice == '9':
        search_operations()

    elif choice == '0':
        # Back to Main Menu
        return

    else:
        print("Invalid choice. Please enter a number between 0 and 9.")

    # Recursive call for continuous retrieval operations
    retrieve_operations()

# Function for Search Operations


def search_operations():
    print("\nSearch Operations:")
    print("1. Retrieve the passengers whose name ends with 'Sharma', reservation ID starts with 'EMT', or flight number starts with '4'.")
    print("2. Retrieve the employees whose name starts with 'Hema', job title is 'Pilot', or department containing 'Field'.")
    print("3. Retrieve aircraft by number starting with '134' or type containing 'AB'.")
    print("4. Retrieve a list of passengers in age group 25-40 who made reservations on flights going to Delhi on 18th November 2023.")
    print("0. Back to Main Menu")

    choice = input("Enter your choice (0-4): ")

    if choice == '1':
        query = """
            SELECT *
            FROM Passenger
            WHERE Passenger.name LIKE '%Sharma'
            OR Passenger.passenger_id IN (
                SELECT passenger_id
                FROM Reservation
                WHERE id LIKE 'EMT%' OR flight_number LIKE '6E%'
            );
        """
        execute_query(query)

    elif choice == '2':
        query = """
            SELECT *
            FROM Employee
            WHERE e_name LIKE 'Hema%' OR roles = 'Pilot' OR designation LIKE '%Field%';
        """
        execute_query(query)


    elif choice == '3':
        query = """
            SELECT *
            FROM Airplane
            WHERE airplane_number LIKE '134%' OR airplane_model LIKE '%AB%';
        """
        execute_query(query)


    elif choice == '4':
        pass


    elif choice == '0':
        # Back to Main Menu
        return

    else:
        print("Invalid choice. Please enter a number between 0 and 4.")

    # Recursive call for continuous search operations
    search_operations()


# Main Menu
while True:
    print("\nMain Menu:")
    print("1. Retrieve Operations")
    print("2. Exit")

    main_choice = input("Enter your choice (1-2): ")

    if main_choice == '1':
        # Retrieve Operations
        retrieve_operations()

    elif main_choice == '2':
        # Exit
        break

    else:
        print("Invalid choice. Please enter 1 or 2.")
