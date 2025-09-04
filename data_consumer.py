import os
import requests
from sqlalchemy import create_engine, Column, String, Integer, Float, Date, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///nyc_restaurant_inspections.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Inspection(Base):
    __tablename__ = 'inspections'

    camis = Column(String, primary_key=True)
    dba = Column(String)
    boro = Column(String)
    building = Column(String)
    street = Column(String)
    zipcode = Column(String)
    phone = Column(String)
    cuisine_description = Column(String)
    inspection_date = Column(Date)
    action = Column(String)
    violation_code = Column(String)
    violation_description = Column(String)
    critical_flag = Column(String)
    score = Column(String)
    record_date = Column(DateTime)
    inspection_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    community_board = Column(String)
    council_district = Column(String)
    census_tract = Column(String)
    bin = Column(String)
    bbl = Column(String)
    nta = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# API endpoint
API_ENDPOINT = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"

def fetch_data(limit=1000, offset=0):
    """Fetch data from the API with a limit and offset."""
    params = {
        '$limit': limit,
        '$offset': offset
    }
    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def main():
    """Main function to fetch and store data."""
    offset = 0
    limit = 1000  # Adjust the limit as needed

    while True:
        print(f"Fetching data with offset: {offset}")
        data = fetch_data(limit=limit, offset=offset)
        if not data:
            print("No more data to fetch.")
            break

        for item in data:
            inspection_date_str = item.get('inspection_date')
            inspection_date = datetime.strptime(inspection_date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S').date() if inspection_date_str else None

            record_date_str = item.get('record_date')
            record_date = datetime.strptime(record_date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S') if record_date_str else None

            # Create a new Inspection object
            inspection = Inspection(
                camis=item.get('camis'),
                dba=item.get('dba'),
                boro=item.get('boro'),
                building=item.get('building'),
                street=item.get('street'),
                zipcode=item.get('zipcode'),
                phone=item.get('phone'),
                cuisine_description=item.get('cuisine_description'),
                inspection_date=inspection_date,
                action=item.get('action'),
                violation_code=item.get('violation_code'),
                violation_description=item.get('violation_description'),
                critical_flag=item.get('critical_flag'),
                score=item.get('score'),
                record_date=record_date,
                inspection_type=item.get('inspection_type'),
                latitude=float(item.get('latitude')) if item.get('latitude') else None,
                longitude=float(item.get('longitude')) if item.get('longitude') else None,
                community_board=item.get('community_board'),
                council_district=item.get('council_district'),
                census_tract=item.get('census_tract'),
                bin=item.get('bin'),
                bbl=item.get('bbl'),
                nta=item.get('nta')
            )
            session.merge(inspection)

        session.commit()
        offset += limit

    print("Data fetching and storing complete.")

if __name__ == "__main__":
    main()