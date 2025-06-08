import pytest
import sqlite3
import tempfile
import os
from app import create_app


@pytest.fixture
def create_test_db():
    """Create a minimal test database with sample data"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    try:
        # Create tables and insert sample data
        conn = sqlite3.connect(db_path)

        # Create minimal schema
        conn.executescript(
            """
            CREATE TABLE Employee (
                EmployeeId INTEGER PRIMARY KEY,
                FirstName TEXT,
                LastName TEXT
            );
            
            CREATE TABLE Customer (
                CustomerId INTEGER PRIMARY KEY,
                SupportRepId INTEGER,
                FOREIGN KEY (SupportRepId) REFERENCES Employee (EmployeeId)
            );
            
            CREATE TABLE Invoice (
                InvoiceId INTEGER PRIMARY KEY,
                CustomerId INTEGER,
                InvoiceDate TEXT,
                Total REAL,
                FOREIGN KEY (CustomerId) REFERENCES Customer (CustomerId)
            );
            
            -- Insert sample data
            INSERT INTO Employee (EmployeeId, FirstName, LastName) VALUES 
                (1, 'Jane', 'Peacock'),
                (2, 'Steve', 'Johnson');
            
            INSERT INTO Customer (CustomerId, SupportRepId) VALUES 
                (1, 1),
                (2, 2);
            
            INSERT INTO Invoice (InvoiceId, CustomerId, InvoiceDate, Total) VALUES 
                (1, 1, '2009-01-01', 100.50),
                (2, 1, '2009-02-01', 84.34),
                (3, 2, '2010-01-01', 121.91),
                (4, 2, '2010-02-01', 100.00);
        """
        )

        conn.commit()
        conn.close()

        yield db_path

    finally:
        # Clean up
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def app_with_test_db(create_test_db):
    """Create application with test database"""
    # Temporarily replace the database path
    import app.database

    original_db_path = (
        app.database.Database.__init__.__defaults__[0]
        if app.database.Database.__init__.__defaults__
        else "data.db"
    )

    # Monkey patch the Database class to use test database
    def patched_init(self, db_path: str = create_test_db):
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file {db_path} not found")

    app.database.Database.__init__ = patched_init

    app = create_app()
    app.config["TESTING"] = True

    yield app

    # Restore original
    def restore_init(self, db_path: str = original_db_path):
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file {db_path} not found")

    app.database.Database.__init__ = restore_init
