from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:
    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.set_year(year)
        self.set_summary(summary)
        self.set_employee_id(employee_id)

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    def set_year(self, year):
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        if year < 2000:
            raise ValueError("Year must be 2000 or later")
        self._year = year

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        self.set_year(year)

    def set_summary(self, summary):
        if not isinstance(summary, str) or len(summary) == 0:
            raise ValueError("Summary must be a non-empty string")
        self._summary = summary

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        self.set_summary(summary)

    def set_employee_id(self, employee_id):
        if not isinstance(employee_id, int):
            raise ValueError("Employee ID must be an integer")
        if not Employee.find_by_id(employee_id):
            raise ValueError("Employee with given ID does not exist")
        self._employee_id = employee_id

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        self.set_employee_id(employee_id)

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Review instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Review instances"""
        sql = "DROP TABLE IF EXISTS reviews;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO reviews (year, summary, employee_id) 
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        self.id = CURSOR.lastrowid  # Update the id with the primary key value
        Review.all[self.id] = self  # Save the object in the dictionary

    @classmethod
    def create(cls, year, summary, employee_id):
        """Initialize a new Review instance and save the object to the database. Return the new instance."""
        review = cls(year, summary, employee_id)
        review.save()  # Call the save method to insert into the database
        return review  # Return the new instance

    @classmethod
    def instance_from_db(cls, row):
        """Return a Review instance having the attribute values from the table row."""
        id, year, summary, employee_id = row  # Unpack the row data
        review = cls(year, summary, employee_id, id)  # Create a new Review instance
        cls.all[review.id] = review  # Cache it in the dictionary
        return review  # Return the instance

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        sql = "SELECT * FROM reviews WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()  # Get a single row
        if row:
            return cls.instance_from_db(row)  # Return the instance from the row
        return None  # Return None if not found

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql = """
            UPDATE reviews 
            SET year = ?, summary = ?, employee_id = ? 
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = "DELETE FROM reviews WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        del Review.all[self.id]  # Remove from local cache
        self.id = None  # Set id to None

    @classmethod
    def get_all(cls, employee_id=None):
        """Return a list containing one Review instance per table row.
        If employee_id is provided, filter by that employee."""
        sql = "SELECT * FROM reviews"
        if employee_id:
            sql += " WHERE employee_id = ?"
            CURSOR.execute(sql, (employee_id,))
        else:
            CURSOR.execute(sql)

        rows = CURSOR.fetchall()  # Fetch all rows
        return [
            cls.instance_from_db(row) for row in rows
        ]  # Return instances for each row