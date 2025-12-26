DEFAULT_HOSPITALS = {
    "Diabetes": ["Apollo Hospitals", "Fortis Healthcare", "AIIMS"],
    "Heart": ["Apollo Cardiology", "Fortis Heart Care", "AIIMS Cardiology"],
    "Kidney": ["Apollo Nephrology", "Fortis Nephrology", "AIIMS Nephrology"],
    "Liver": ["Apollo Hepatology", "Fortis Liver Care", "AIIMS Hepatology"]
}

LOCATION_HOSPITALS = {

    # -------- NORTH INDIA --------
    "delhi": {
        "Diabetes": ["AIIMS Delhi", "Apollo Delhi"],
        "Heart": ["Fortis Escorts", "AIIMS Cardiology"],
        "Kidney": ["Medanta Delhi"],
        "Liver": ["ILBS Delhi"]
    },
    "punjab": {
        "Diabetes": ["Fortis Mohali"],
        "Heart": ["Hero DMC Ludhiana"],
        "Kidney": ["Apollo Amritsar"],
        "Liver": ["Fortis Mohali"]
    },
    "haryana": {
        "Diabetes": ["Medanta Gurgaon"],
        "Heart": ["Medanta Heart Institute"],
        "Kidney": ["Artemis Hospital"],
        "Liver": ["Medanta Liver Centre"]
    },
    "uttar pradesh": {
        "Diabetes": ["SGPGI Lucknow"],
        "Heart": ["Medanta Lucknow"],
        "Kidney": ["KGMU Lucknow"],
        "Liver": ["SGPGI Liver Institute"]
    },
    "uttarakhand": {
        "Diabetes": ["AIIMS Rishikesh"],
        "Heart": ["AIIMS Rishikesh"],
        "Kidney": ["Himalayan Hospital"],
        "Liver": ["AIIMS Rishikesh"]
    },
    "himachal pradesh": {
        "Diabetes": ["IGMC Shimla"],
        "Heart": ["IGMC Shimla"],
        "Kidney": ["IGMC Shimla"],
        "Liver": ["IGMC Shimla"]
    },
    "jammu and kashmir": {
        "Diabetes": ["SKIMS Srinagar"],
        "Heart": ["SKIMS Cardiology"],
        "Kidney": ["SKIMS Nephrology"],
        "Liver": ["GMC Jammu"]
    },

    # -------- WEST INDIA --------
    "maharashtra": {
        "Diabetes": ["Lilavati Hospital Mumbai"],
        "Heart": ["Asian Heart Institute"],
        "Kidney": ["Hinduja Hospital"],
        "Liver": ["Global Hospital Mumbai"]
    },
    "gujarat": {
        "Diabetes": ["Apollo Ahmedabad"],
        "Heart": ["CIMS Hospital"],
        "Kidney": ["Sterling Hospital"],
        "Liver": ["Institute of Liver Diseases Ahmedabad"]
    },
    "rajasthan": {
        "Diabetes": ["Fortis Jaipur"],
        "Heart": ["EHCC Jaipur"],
        "Kidney": ["SMS Hospital Jaipur"],
        "Liver": ["Fortis Jaipur"]
    },
    "goa": {
        "Diabetes": ["Manipal Hospital Goa"],
        "Heart": ["Manipal Goa"],
        "Kidney": ["Goa Medical College"],
        "Liver": ["Manipal Goa"]
    },

    # -------- SOUTH INDIA --------
    "karnataka": {
        "Diabetes": ["Manipal Hospital Bangalore"],
        "Heart": ["Narayana Health"],
        "Kidney": ["Aster CMI Hospital"],
        "Liver": ["Fortis Bangalore"]
    },
    "tamil nadu": {
        "Diabetes": ["Apollo Chennai"],
        "Heart": ["Fortis Malar"],
        "Kidney": ["MIOT Hospital"],
        "Liver": ["Global Hospital Chennai"]
    },
    "kerala": {
        "Diabetes": ["Aster Medcity Kochi"],
        "Heart": ["Amrita Hospital"],
        "Kidney": ["Lakeshore Hospital"],
        "Liver": ["Aster Medcity"]
    },
    "telangana": {
        "Diabetes": ["Apollo Hyderabad"],
        "Heart": ["Yashoda Hospital"],
        "Kidney": ["Care Hospitals"],
        "Liver": ["AIG Hospitals"]
    },
    "andhra pradesh": {
        "Diabetes": ["Apollo Visakhapatnam"],
        "Heart": ["Care Hospitals Vizag"],
        "Kidney": ["Ramesh Hospitals"],
        "Liver": ["Apollo Vizag"]
    },

    # -------- EAST INDIA --------
    "west bengal": {
        "Diabetes": ["AMRI Hospitals Kolkata"],
        "Heart": ["Rabindranath Tagore Hospital"],
        "Kidney": ["Apollo Gleneagles"],
        "Liver": ["Peerless Hospital"]
    },
    "odisha": {
        "Diabetes": ["SUM Hospital Bhubaneswar"],
        "Heart": ["Apollo Bhubaneswar"],
        "Kidney": ["KIMS Bhubaneswar"],
        "Liver": ["SUM Hospital"]
    },
    "bihar": {
        "Diabetes": ["IGIMS Patna"],
        "Heart": ["Paras HMRI"],
        "Kidney": ["AIIMS Patna"],
        "Liver": ["IGIMS Patna"]
    },
    "jharkhand": {
        "Diabetes": ["RIMS Ranchi"],
        "Heart": ["Medanta Ranchi"],
        "Kidney": ["RIMS Ranchi"],
        "Liver": ["RIMS Ranchi"]
    },

    # -------- CENTRAL INDIA --------
    "madhya pradesh": {
        "Diabetes": ["CHL Hospital Indore"],
        "Heart": ["CARE CHL"],
        "Kidney": ["Apollo Indore"],
        "Liver": ["CHL Hospital"]
    },
    "chhattisgarh": {
        "Diabetes": ["AIIMS Raipur"],
        "Heart": ["Ramkrishna Care"],
        "Kidney": ["AIIMS Raipur"],
        "Liver": ["Ramkrishna Care"]
    },

    # -------- NORTH EAST --------
    "assam": {
        "Diabetes": ["GNRC Guwahati"],
        "Heart": ["GNRC Heart Centre"],
        "Kidney": ["Apollo Guwahati"],
        "Liver": ["GNRC Guwahati"]
    },
    "meghalaya": {
        "Diabetes": ["NEIGRIHMS"],
        "Heart": ["NEIGRIHMS"],
        "Kidney": ["NEIGRIHMS"],
        "Liver": ["NEIGRIHMS"]
    },
    "tripura": {
        "Diabetes": ["AGMC Agartala"],
        "Heart": ["AGMC"],
        "Kidney": ["AGMC"],
        "Liver": ["AGMC"]
    },

    # -------- UNION TERRITORIES --------
    "chandigarh": {
        "Diabetes": ["PGIMER Chandigarh"],
        "Heart": ["PGIMER Cardiology"],
        "Kidney": ["PGIMER Nephrology"],
        "Liver": ["PGIMER"]
    },
    "puducherry": {
        "Diabetes": ["JIPMER"],
        "Heart": ["JIPMER"],
        "Kidney": ["JIPMER"],
        "Liver": ["JIPMER"]
    }
}
def hospital_map_link(hospital, location):
    query = f"{hospital} {location} hospital"
    return f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

def get_best_hospitals(disease, state=None, age=None):
    if not state:
        return DEFAULT_HOSPITALS.get(disease, [])

    state = state.lower().strip()

    return LOCATION_HOSPITALS.get(
        state,
        DEFAULT_HOSPITALS
    ).get(disease, DEFAULT_HOSPITALS.get(disease, []))

