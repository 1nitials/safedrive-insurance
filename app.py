from flask import Flask, render_template, request, redirect
from datetime import datetime
from collections import defaultdict
import mysql.connector
import re

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

@app.route("/delete_policy/<int:policy_id>", methods=["POST"])
def delete_policy(policy_id):
    try:
        cursor.execute("DELETE FROM insurance_policy WHERE Policy_ID = %s", (policy_id,))
        db.commit()
        return redirect("/view_policies")
    except Exception as e:
        print(f"Error deleting policy: {e}")
        return redirect("/view_policies")

@app.route("/delete_policyholder/<int:policyholder_id>", methods=["POST"])
def delete_policyholder(policyholder_id):
    try:
        cursor.execute("DELETE FROM policyholder WHERE Policyholder_ID = %s", (policyholder_id,))
        db.commit()
        return redirect("/view_policyholders")
    except Exception as e:
        print(f"Error deleting policyholder: {e}")
        return redirect("/view_policyholders")
    
@app.route("/add_policyholder", methods=["GET", "POST"])
def add_policyholder():
    if request.method == "POST":
        # Retrieve form data
        name = request.form.get("name")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        date_of_birth = request.form.get("date_of_birth")
        driving_license_number = request.form.get("driving_license_number")
        
        # Initialize an error message variable
        error_message = None
        
        # Input validation
        if not name or not contact_number or not email or not date_of_birth or not driving_license_number:
            error_message = "All fields are required."
        
        # Validate email format
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_message = "Invalid email format."
        
        # Validate contact number (assuming a 10-digit number)
        elif not contact_number.isdigit() or len(contact_number) > 13:
            error_message = "Contact number must be less than 13-digit number."
        
        # Validate date of birth (ensure it's not a future date)
        try:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
            if dob > datetime.now():
                error_message = "Date of birth cannot be a future date."
        except ValueError:
            error_message = "Invalid date of birth format."
        
        if error_message:
            return render_template("add_policyholder.html", error=error_message)
        
        # If no errors, insert the data into the database
        try:
            query = """
                INSERT INTO policyholder (
                    Policyholder_Name, 
                    Policyholder_Contact_Number, 
                    Policyholder_Email, 
                    Policyholder_Date_Of_Birth, 
                    Policyholder_Driving_License_Number
                ) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, contact_number, email, date_of_birth, driving_license_number))
            db.commit()
            return redirect("/view_policyholders")
        except Exception as e:
            print(f"Error inserting policyholder: {e}")
            return render_template("add_policyholder.html", error="Failed to add policyholder.")
    
    return render_template("add_policyholder.html")

# Additional routes for CRUD operations and queries go here
@app.route("/view_policies")
def view_policies():
    
    cleanup_duplicates()
    
    # Query the database for policies
    cursor.execute("SELECT * FROM insurance_policy")
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
            active_policy.Policy_Start_Date,
            active_policy.Policy_End_Date,
            insurance_policy.Policy_Number,
            insurance_policy.Policy_Type,
            insurance_policy.Policy_Premium_Amount
        FROM 
            policyholder
        LEFT JOIN 
            active_policy ON policyholder.Policyholder_ID = active_policy.Application_ID
        LEFT JOIN 
            insurance_policy ON active_policy.Application_ID = insurance_policy.Policy_ID
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
                "Policy_Start_Date": row["Policy_Start_Date"],
                "Policy_End_Date": row["Policy_End_Date"],
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
            active_policy.Policy_Start_Date,
            active_policy.Policy_End_Date,
            insurance_policy.Policy_Number,
            insurance_policy.Policy_Type,
            insurance_policy.Policy_Premium_Amount
        FROM vehicle
        LEFT JOIN active_policy ON vehicle.Active_Policy_ID = active_policy.Active_Policy_ID
        LEFT JOIN insurance_policy ON active_policy.Application_ID = insurance_policy.Policy_ID
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


@app.route("/monthly_sales")
def monthly_sales():
    cursor.execute("""
        SELECT Policy_Start_Date
        FROM active_policy
        WHERE Policy_Start_Date IS NOT NULL
    """)
    raw_dates = cursor.fetchall()

    # Use a defaultdict to count occurrences per month-year
    monthly_counts = defaultdict(int)
    for record in raw_dates:
        # Extract the month and year from the date
        month_year = record['Policy_Start_Date'].strftime('%Y-%m')
        monthly_counts[month_year] += 1

    # Convert the defaultdict to a list of dictionaries for the template
    sales_data = [{'Month': month, 'Policy_Count': count} for month, count in monthly_counts.items()]
    sales_data.sort(reverse=True, key=lambda x: x['Month'])  # Sort by month descending

    return render_template("monthly_sales.html", sales_data=sales_data)

@app.route("/top_vehicles")
def top_vehicles():
    query = """
        SELECT 
            vehicle.Vehicle_Type, 
            COUNT(*) AS NumberOfPolicies
        FROM 
            vehicle
        JOIN 
            active_policy ON vehicle.Active_Policy_ID = active_policy.Active_Policy_ID
        GROUP BY 
            vehicle.Vehicle_Type
        ORDER BY 
            NumberOfPolicies DESC
        LIMIT 5
    """
    cursor.execute(query)
    top_vehicle_types = cursor.fetchall()
    return render_template("top_vehicles.html", top_vehicle_types=top_vehicle_types)


def cleanup_duplicates():
    # Step 1: Identify duplicates by Policy_Number
    cursor.execute("""
        SELECT MIN(Policy_ID) as MinID
        FROM insurance_policy
        GROUP BY Policy_Number, Policy_Type, Policy_Premium_Amount
    """)
    unique_ids = [row['MinID'] for row in cursor.fetchall()]  # Keep unique IDs
    
    # Step 2: Delete all rows not in the unique IDs
    query = """
        DELETE FROM insurance_policy
        WHERE Policy_ID NOT IN (%s)
    """ % (", ".join(map(str, unique_ids)))
    
    cursor.execute(query)
    db.commit()
    print("Duplicates cleaned up successfully!")

if __name__ == "__main__":
    app.run(debug=True)
    

    
    


