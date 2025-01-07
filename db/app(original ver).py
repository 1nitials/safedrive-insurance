from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",          # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="SafeDrive"  # Replace with your database name if needed
)
cursor = db.cursor(dictionary=True)

def execute_sql_file(filepath):
    with open(filepath, 'r') as file:
        sql_script = file.read()
    for statement in sql_script.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.errors.IntegrityError as e:
                print(f"Error: {e}")
    db.commit()

# Initialize the database
execute_sql_file('db/safedrive.sql')


@app.route("/")
def home():
    return render_template("index.html")

# Additional routes for CRUD operations and queries go here
@app.route("/view_policies")
def view_policies():
    
    cleanup_duplicates()
    
    # Query the database for policies
    cursor.execute("SELECT * FROM insurancepolicy")
    policies = cursor.fetchall()  # Fetch all rows as a list of dictionaries
    print(policies)
    
    # Ensure the keys are capitalized to match the template
    formatted_policies = [
        {
            "Policy_ID": policy["Policy_ID"],
            "Policy_Number": policy["Policy_Number"],
            "Policy_Type": policy["Policy_Type"],
            "Policy_Premium_Amount": policy["Policy_Premium_Amount"]
        }
        for policy in policies
    ]
    
    return render_template("view_policies.html", policies=formatted_policies)

@app.route("/view_policyholders")
def view_policyholders():
    # Query the database for policyholders and their policies
    query = """
        SELECT 
            policyholder.Policyholder_ID,
            policyholder.Policyholder_Name,
            policyholder.Policyholder_Contact_Number,
            policyholder.Policyholder_Email,
            policyholder.Policyholder_Date_Of_Birth,
            policyholder.Policyholder_Driving_License_Number,
            insurancepolicy.Policy_Number,
            insurancepolicy.Policy_Type,
            insurancepolicy.Policy_Premium_Amount
        FROM 
            policyholder
        LEFT JOIN 
            activepolicy ON policyholder.Policyholder_ID = activepolicy.Policyholder_ID
        LEFT JOIN 
            insurancepolicy ON activepolicy.Policy_ID = insurancepolicy.Policy_ID
        ORDER BY 
            policyholder.Policyholder_ID
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Group policies under each policyholder
    policyholders = {}
    for row in results:
        policyholder_id = row["Policyholder_ID"]
        if policyholder_id not in policyholders:
            policyholders[policyholder_id] = {
                "Policyholder_ID": row["Policyholder_ID"],
                "Policyholder_Name": row["Policyholder_Name"],
                "Policyholder_Contact_Number": row["Policyholder_Contact_Number"],
                "Policyholder_Email": row["Policyholder_Email"],
                "Policyholder_Date_Of_Birth": row["Policyholder_Date_Of_Birth"],
                "Policyholder_Driving_License_Number": row["Policyholder_Driving_License_Number"],
                "Policies": []
            }
        # Add policy details if available
        if row["Policy_Number"]:
            policyholders[policyholder_id]["Policies"].append({
                "Policy_Number": row["Policy_Number"],
                "Policy_Type": row["Policy_Type"],
                "Policy_Premium_Amount": row["Policy_Premium_Amount"]
            })

    # Convert to a list for rendering
    policyholders_list = list(policyholders.values())
    return render_template("view_policyholders.html", policyholders=policyholders_list)

@app.route("/view_vehicles")
def view_vehicles():
    # Query to fetch all vehicles and their associated policies
    cursor.execute("""
        SELECT
            vehicle.Vehicle_ID,
            vehicle.Vehicle_Plate_Num,
            vehicle.Vehicle_Type,
            vehicle.Vehicle_Manufacture_Year,
            policyholder.Policyholder_Name,
            activepolicy.Policy_Start_Date,
            activepolicy.Policy_End_Date,
            insurancepolicy.Policy_Number,
            insurancepolicy.Policy_Type,
            insurancepolicy.Policy_Premium_Amount
        FROM vehicle
        LEFT JOIN activepolicy ON vehicle.Active_Policy_ID = activepolicy.Active_Policy_ID
        LEFT JOIN insurancepolicy ON activepolicy.Policy_ID = insurancepolicy.Policy_ID
        LEFT JOIN policyholder ON vehicle.Policyholder_ID = policyholder.Policyholder_ID
    """)
    vehicles = cursor.fetchall()

    # Format the data for the template
    formatted_vehicles = [
        {
            "Vehicle_ID": vehicle["Vehicle_ID"],
            "Vehicle_Plate_Num": vehicle["Vehicle_Plate_Num"],
            "Vehicle_Type": vehicle["Vehicle_Type"],
            "Vehicle_Manufacture_Year": vehicle["Vehicle_Manufacture_Year"],
            "Policyholder_Name": vehicle["Policyholder_Name"],
            "Policy_Start_Date": vehicle["Policy_Start_Date"],
            "Policy_End_Date": vehicle["Policy_End_Date"],
            "Policy_Number": vehicle["Policy_Number"],
            "Policy_Type": vehicle["Policy_Type"],
            "Policy_Premium_Amount": vehicle["Policy_Premium_Amount"]
        }
        for vehicle in vehicles
    ]

    return render_template("view_vehicles.html", vehicles=formatted_vehicles)


def cleanup_duplicates():
    # Step 1: Identify duplicates by Policy_Number
    cursor.execute("""
        SELECT MIN(Policy_ID) as MinID
        FROM insurancepolicy
        GROUP BY Policy_Number, Policy_Type, Policy_Premium_Amount
    """)
    unique_ids = [row['MinID'] for row in cursor.fetchall()]  # Keep unique IDs
    
    # Step 2: Delete all rows not in the unique IDs
    query = """
        DELETE FROM insurancepolicy
        WHERE Policy_ID NOT IN (%s)
    """ % (", ".join(map(str, unique_ids)))
    
    cursor.execute(query)
    db.commit()
    print("Duplicates cleaned up successfully!")

if __name__ == "__main__":
    app.run(debug=True)
    
    


