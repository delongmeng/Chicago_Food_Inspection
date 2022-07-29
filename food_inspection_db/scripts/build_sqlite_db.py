"""
This program builds the Chicago Food Inspection Sqlite database from the csv files.
"""

import os
import csv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from food_inspection_db.models.models import Base, Facility, Address, Risk, Facility_Risk, Inspection, Facility_Inspection, Violation, Inspection_Violation

def get_data(filepath):
    """
    This function gets the data from the csv file
    """
    data = {}
    files = ['facilities', 'addresses', 'risks', 'facility_risk', 'inspections',
        'facility_inspection', 'violations', 'inspection_violation']
    for file in files:
        with open(filepath + file + '.csv') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            data[file] = [row for row in csv_reader]
    return data


def populate_database(session, data):

    count = 0
    for row in data['facilities']:
        facility = (
            session.query(Facility)
            .filter(Facility.id == row['facility_id'])
            .one_or_none()
        )
        if facility is None:
            facility = Facility(
                id = row['facility_id'],
                name_dba = row['name_dba'],
                name_aka = row['name_aka'],
                license_id = row['license_id'],
                facility_type = row['facility_type'],
                address = row['address'],
                zip = row['zip']
            )
            session.add(facility)
            count += 1
    print(f"   inserted {count} rows into the Facility table")


    count = 0
    for row in data['addresses']:
        address = (
            session.query(Address)
            .filter(Address.street == row['address'], Address.zip == row['zip'])
            .one_or_none()
        )
        if address is None:
            address = Address(
                street = row['address'],
                zip = row['zip'],
                city = row['city'],
                state = row['state'],
                latitude = row['latitude'],
                longitude = row['longitude']
            )
            session.add(address)
            count += 1
    print(f"   inserted {count} rows into the Address table")


    count = 0
    for row in data['risks']:
        risk = (
            session.query(Risk)
            .filter(Risk.code == row['code'])
            .one_or_none()
        )
        if risk is None:
            risk = Risk(
                code = row['code'],
                level = row['level']
            )
            session.add(risk)
            count += 1
    print(f"   inserted {count} rows into the Risk table")


    count = 0
    for row in data['facility_risk']:
        facility_risk = (
            session.query(Facility_Risk)
            .filter(Facility_Risk.facility_id == row['facility_id'])
            .one_or_none()
        )
        if facility_risk is None:
            facility_risk = Facility_Risk(
                facility_id = row['facility_id'],
                risk_code = row['risk_code']
            )
            session.add(facility_risk)
            count += 1
    print(f"   inserted {count} rows into the Facility_Risk table")


    count = 0
    for row in data['inspections']:
        inspection = (
            session.query(Inspection)
            .filter(Inspection.id == row['inspection_id'])
            .one_or_none()
        )
        if inspection is None:
            inspection = Inspection(
                id = row['inspection_id'],
                date = pd.to_datetime(row['inspection_date']),
                type = row['inspection_type'],
                result = row['results']
            )
            session.add(inspection)
            count += 1
    print(f"   inserted {count} rows into the Inspection table")


    count = 0
    for row in data['facility_inspection']:
        facility_inspection = (
            session.query(Facility_Inspection)
            .filter(Facility_Inspection.facility_id == row['facility_id'],
                Facility_Inspection.inspection_id == row['inspection_id'])
            .one_or_none()
        )
        if facility_inspection is None:
            facility_inspection = Facility_Inspection(
                facility_id = row['facility_id'],
                inspection_id = row['inspection_id']
            )
            session.add(facility_inspection)
            count += 1
    print(f"   inserted {count} rows into the Facility_Inspection table")


    count = 0
    for row in data['violations']:
        violation = (
            session.query(Violation)
            .filter(Violation.code == row['code'])
            .one_or_none()
        )
        if violation is None:
            violation = Violation(
                code = row['code'],
                description = row['description']
            )
            session.add(violation)
            count += 1
    print(f"   inserted {count} rows into the Violation table")


    count = 0
    for row in data['inspection_violation']:
        inspection_violation = (
            session.query(Inspection_Violation)
            .filter(Inspection_Violation.inspection_id == row['inspection_id'],
                Inspection_Violation.violation_code == row['violation_code'],
                Inspection_Violation.violation_comment == row['violation_comment'])
            .one_or_none()
        )
        if inspection_violation is None:
            inspection_violation = Inspection_Violation(
                inspection_id = row['inspection_id'],
                violation_code = row['violation_code'],
                violation_comment = row['violation_comment']
            )
            session.add(inspection_violation)
            count += 1
    print(f"   inserted {count} rows into the Inspection_Violation table")


    session.commit()


def main(directory='./data/'):
    print("\nStart generating database...")
    csv_filepath = directory + 'tables/'
    data = get_data(csv_filepath)

    sqlite_filepath = directory + 'db/food_inspections.db'
    # does the database exist?
    if os.path.exists(sqlite_filepath):
        os.remove(sqlite_filepath)

    # create the database and insert data
    engine = create_engine(f"sqlite:///{sqlite_filepath}")
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    populate_database(session, data)
    session.close()
    print("...database created!\n")

if __name__ == "__main__":
    main()
