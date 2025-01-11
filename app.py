from flask import Flask, render_template, request, redirect
from datetime import datetime
from collections import defaultdict
import mysql.connector
import re
import os

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

#Add functions**********************************************************************************************

@app.route("/add/add_policyholder", methods=["GET", "POST"])
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
        
        # Validate contact number (assuming digit number less than 14)
        elif not contact_number.isdigit() or 9 > len(contact_number) > 14:
            error_message = "Contact number must be between 10-13 digit number."
        
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
            return redirect("/view/view_policyholders")
        except Exception as e:
            print(f"Error inserting policyholder: {e}")
            return render_template("add_policyholder.html", error="Failed to add policyholder.")
    
    return render_template("add/add_policyholder.html")

@app.route("/add/add_insurance_policy", methods=["GET", "POST"])
def add_insurance_policy():
    if request.method == "POST":
        # Get form data
        policy_number = request.form.get("policy_number")
        policy_type = request.form.get("policy_type")  # THIRD_PARTY_COVERAGE or COMPREHENSIVE_COVERAGE
        policy_premium = request.form.get("policy_premium")
        
        # Coverage data based on the policy type
        liability_coverage_limit = request.form.get("liability_coverage_limit", None)
        property_damage_liability = request.form.get("property_damage_liability", None)
        injury_liability_coverage = request.form.get("injury_liability_coverage", None)
        
        repair_coverage_limit = request.form.get("repair_coverage_limit", None)
        roadside_assistance_included = True if request.form.get('roadside_assistance_included') else False
        theft_coverage = True if request.form.get('theft_coverage') else False
        # roadside_assistance_included = request.form.get("roadside_assistance_included", None)
        # theft_coverage = request.form.get("theft_coverage", None)

        # Initialize error message
        error_message = None
        
        # Validation
        if not policy_number or not policy_type or not policy_premium:
            error_message = "Policy Number, Type, and Premium are required."
        try:
            policy_premium = float(policy_premium)
            if policy_premium <= 0:
                error_message = "Policy premium must be a positive value."
        except ValueError:
            error_message = "Invalid premium value."
        
        if policy_type == "THIRD_PARTY_COVERAGE":
            if not liability_coverage_limit or not property_damage_liability or not injury_liability_coverage:
                error_message = "Third-party coverage details are missing."
        elif policy_type == "COMPREHENSIVE_COVERAGE":
            if not repair_coverage_limit:
                error_message = "Repair Coverage Limit details are missing."
        
        # If there are validation errors, render the form again with the error message
        if error_message:
            return render_template("add_insurance_policy.html", error=error_message)
        
        # If no errors, proceed with insertion
        try:
            # Step 1: Insert the policy into the insurance_policy table
            query = """
                INSERT INTO insurance_policy (Policy_Number, Policy_Type, Policy_Premium_Amount)
                VALUES (%s, %s, %s)
                """
            cursor.execute(query, (policy_number, policy_type, policy_premium))
            db.commit()
            
            # Get the Policy_ID of the inserted policy
            policy_id = cursor.lastrowid

            # Step 2: Insert the relevant coverage details based on the policy type
            if policy_type == "THIRD_PARTY_COVERAGE":
                query = """
                    INSERT INTO third_party_coverage (Policy_ID, Liability_Coverage_Limit, Property_Damage_Liability, Injury_Liability_Coverage)
                    VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query, (policy_id, liability_coverage_limit, property_damage_liability, injury_liability_coverage))
            
            elif policy_type == "COMPREHENSIVE_COVERAGE":
                query = """
                    INSERT INTO comprehensive_coverage (Policy_ID, Repair_Coverage_Limit, Roadside_Assistance_Included, Theft_Coverage)
                    VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query, (policy_id, repair_coverage_limit, roadside_assistance_included, theft_coverage))
            
            # Commit changes to the database
            db.commit()

            return redirect("/view/view_policies")

        except Exception as e:
            print(f"Error inserting insurance policy: {e}")
            return render_template("add_insurance_policy.html", error="Failed to add insurance policy.")
    
    return render_template("add/add_insurance_policy.html")

# Apply Application Function
@app.route('/add/add_application', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        # Get selected values from the form
        policyholder_id = request.form['policyholder_id']
        policy_id = request.form['policy_id']
        application_date = request.form['application_date']
        application_purpose = request.form['application_purpose']

        # Check if Policyholder_ID exists in the POLICYHOLDER table
        cursor.execute("SELECT * FROM POLICYHOLDER WHERE Policyholder_ID = %s", (policyholder_id,))
        policyholder = cursor.fetchone()

        if not policyholder:
            return "Error: Policyholder ID does not exist. Please provide a valid ID."

        # Check if Policy_ID exists in the INSURANCE_POLICY table
        cursor.execute("SELECT * FROM INSURANCE_POLICY WHERE Policy_ID = %s", (policy_id,))
        policy = cursor.fetchone()

        if not policy:
            return "Error: Policy ID does not exist. Please provide a valid policy ID."

        # Insert into APPLICATION table
        insert_application_query = """
            INSERT INTO APPLICATION (Policyholder_ID, Policy_ID, Application_Date, Application_Status, Application_Purpose)
            VALUES (%s, %s, %s, 'Pending', %s)
        """
        cursor.execute(insert_application_query, (policyholder_id, policy_id, application_date, application_purpose))
        db.commit()

        # Get the last inserted application ID
        application_id = cursor.lastrowid

        # Handle Personal or Commercial details
        if application_purpose == 'PERSONAL':
            mileage_limit = request.form['mileage_limit']
            driver_count = request.form['driver_count']
            insert_personal_query = """
                INSERT INTO PERSONAL (Application_ID, Mileage_Limit, Driver_Count)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_personal_query, (application_id, mileage_limit, driver_count))
            db.commit()

        elif application_purpose == 'COMMERCIAL':
            fleet_size = request.form['fleet_size']
            goods_covered = request.form['goods_covered']
            business_use_type = request.form['business_use_type']
            insert_commercial_query = """
                INSERT INTO COMMERCIAL (Application_ID, Fleet_Size, Goods_Covered, Business_Use_Type)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_commercial_query, (application_id, fleet_size, goods_covered, business_use_type))
            db.commit()

        return redirect('/view/view_applications')  # Redirect to the applications list page
    
    # Fetch all policyholders
    cursor.execute("SELECT * FROM POLICYHOLDER")
    policyholders = cursor.fetchall()

    # Fetch all insurance policies (from INSURANCE_POLICY table)
    cursor.execute("SELECT * FROM INSURANCE_POLICY")
    policies = cursor.fetchall()

    return render_template('add/add_application.html', policyholders=policyholders, policies=policies)

@app.route('/add/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        try:
            # Get form data
            application_id = request.form['application_id']
            vehicle_plate_number = request.form['vehicle_plate_number']
            vehicle_type = request.form['vehicle_type']
            vehicle_manufacture_year = request.form['vehicle_manufacture_year']

            # Insert into VEHICLE table
            insert_vehicle_query = """
                INSERT INTO VEHICLE (Vehicle_Plate_Num, Vehicle_Type, Vehicle_Manufacture_Year, Application_ID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_vehicle_query, (vehicle_plate_number, vehicle_type, vehicle_manufacture_year, application_id))
            db.commit()

            # Get the last inserted Vehicle_ID
            vehicle_id = cursor.lastrowid

            # Handle subtype details
            if vehicle_type == 'SEDAN':
                trunk_size = request.form['trunk_size']
                fuel_efficiency = request.form['fuel_efficiency']
                insert_sedan_query = """
                    INSERT INTO SEDAN (Vehicle_ID, Trunk_Size, Fuel_Efficiency)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_sedan_query, (vehicle_id, trunk_size, fuel_efficiency))
                db.commit()

            elif vehicle_type == 'SUV':
                towing_capacity = request.form['towing_capacity']
                # Ensure 'all_wheel_drive' is True if checked, else False
                all_wheel_drive = True if request.form.get('all_wheel_drive') else False

                insert_suv_query = """
                    INSERT INTO SUV (Vehicle_ID, Towing_Capacity, All_Wheel_Drive)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_suv_query, (vehicle_id, towing_capacity, all_wheel_drive))
                db.commit()

            # Add similar logic for other vehicle types (TRUCK, MOTORCYCLE, VAN)
            elif vehicle_type == 'TRUCK':
                payload_capacity = request.form['payload_capacity']
                number_of_tyres = request.form['number_of_tyres']
                insert_truck_query = """
                    INSERT INTO TRUCK (Vehicle_ID, Payload_Capacity, Number_of_Tyres)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_truck_query, (vehicle_id, payload_capacity, number_of_tyres))
                db.commit()

            elif vehicle_type == 'MOTORCYCLE':
                engine_displacement = request.form['engine_displacement']
                helmet_storage = True if request.form.get('helmet_storage') else False
                insert_motorcycle_query = """
                    INSERT INTO MOTORCYCLE (Vehicle_ID, Engine_displacement, Helmet_storage)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_motorcycle_query, (vehicle_id, engine_displacement, helmet_storage))
                db.commit()

            elif vehicle_type == 'VAN':
                seating_capacity = request.form['seating_capacity']
                cargo_space = request.form['cargo_space']
                insert_van_query = """
                    INSERT INTO VAN (Vehicle_ID, Seating_Capacity, Cargo_Space)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_van_query, (vehicle_id, seating_capacity, cargo_space))
                db.commit()

            return redirect('/view/view_vehicles')  # Redirect to a vehicle list page after insertion

        except Exception as e:
            db.rollback()  # Rollback in case of an error
            return f"An error occurred: {str(e)}"

    # Fetch applications for dropdown
    cursor.execute("SELECT * FROM APPLICATION")
    applications = cursor.fetchall()

    return render_template('add/add_vehicle.html', applications=applications)

@app.route('/approve_application', methods=['GET', 'POST'])
def approve_application():
    applications = []

    if request.method == 'GET':
        try:
            # Fetch all applications where the status is 'Pending'
            cursor.execute("""
                SELECT Application_ID, Application_Date, Application_Purpose
                FROM APPLICATION
                WHERE Application_Status = 'Pending'
            """)
            applications = cursor.fetchall()  # Get all pending applications

            return render_template('approve_application.html', applications=applications)

        except mysql.connector.Error as err:
            errors = [f"Database error: {err}"]
            return render_template('error.html', errors=errors)

    elif request.method == 'POST':
        application_id = request.form.get('application_id')
        action = request.form.get('action')  # Approve or Reject
        policy_start_date = request.form.get('policy_start_date')
        policy_end_date = request.form.get('policy_end_date')

        errors = []

        if not application_id or not action:
            errors.append("Please select an application and an action.")
            return render_template('approve_application.html', errors=errors, applications=applications)

        if action == 'Approve':
            # Validate the manual dates
            if not policy_start_date or not policy_end_date:
                errors.append("Please provide both Policy Start Date and Policy End Date.")
                return render_template('approve_application.html', errors=errors, applications=applications)

            try:
                policy_start_date = datetime.strptime(policy_start_date, "%Y-%m-%d").date()
                policy_end_date = datetime.strptime(policy_end_date, "%Y-%m-%d").date()

                if policy_start_date >= policy_end_date:
                    errors.append("Policy End Date must be after Policy Start Date.")
                    return render_template('approve_application.html', errors=errors, applications=applications)

                # Update the application status to 'Approved'
                cursor.execute("""
                    UPDATE APPLICATION
                    SET Application_Status = 'Approved'
                    WHERE Application_ID = %s
                """, (application_id,))
                db.commit()

                # Insert a new active policy record
                cursor.execute("""
                    INSERT INTO ACTIVE_POLICY (Policy_Start_Date, Policy_End_Date, Application_ID)
                    VALUES (%s, %s, %s)
                """, (policy_start_date, policy_end_date, application_id))
                db.commit()

                return redirect('/view_active_policies')  # Redirect to main menu or list page

            except mysql.connector.Error as err:
                errors.append(f"Database error: {err}")
                return render_template('approve_application.html', errors=errors, applications=applications)

        elif action == 'Reject':
            try:
                # Update the application status to 'Rejected'
                cursor.execute("""
                    UPDATE APPLICATION
                    SET Application_Status = 'Rejected'
                    WHERE Application_ID = %s
                """, (application_id,))
                db.commit()

                return redirect('/view_active_policies')  # Redirect to main menu or list page

            except mysql.connector.Error as err:
                errors.append(f"Database error: {err}")
                return render_template('approve_application.html', errors=errors, applications=applications)

        else:
            errors.append("Invalid action selected.")
            return render_template('approve_application.html', errors=errors, applications=applications)

#View functions**********************************************************************************************

@app.route("/view/view_policyholders")
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
    return render_template("view/view_policyholders.html", policyholders=policyholders_list)


@app.route('/view/view_active_policies', methods=['GET'])
def view_active_policies():
    try:
        # Fetch all records from the ACTIVE_POLICY table
        cursor.execute("""
            SELECT * FROM ACTIVE_POLICY 
        """)
        active_policies = cursor.fetchall()  # Fetch all rows

        # Render the template with the data
        return render_template('view_active_policies.html', active_policies=active_policies)

    except mysql.connector.Error as err:
        errors = [f"Database error: {err}"]
        return render_template('error.html', errors=errors)

@app.route("/view/view_vehicles")
def view_vehicles():
    query = """
        SELECT 
            vehicle.Vehicle_ID,
            vehicle.Vehicle_Plate_Num,
            vehicle.Vehicle_Type,
            vehicle.Vehicle_Manufacture_Year,
            policyholder.Policyholder_Name,
            active_policy.Policy_Start_Date,
            active_policy.Policy_End_Date,
            application.Application_ID,
            application.Application_Purpose
        FROM 
            vehicle
        LEFT JOIN application ON vehicle.Application_ID = application.Application_ID
        LEFT JOIN active_policy ON application.Application_ID = active_policy.Application_ID
        LEFT JOIN policyholder ON application.Policyholder_ID = policyholder.Policyholder_ID
    """
    cursor.execute(query)
    vehicles = cursor.fetchall()

    # Add additional info based on Vehicle_Type and Application_Purpose
    for vehicle in vehicles:
        # Fetch personal or commercial details based on Application_Purpose
        if vehicle["Application_Purpose"] == "PERSONAL":
            cursor.execute("SELECT Mileage_Limit, Driver_Count FROM personal WHERE Application_ID = %s", (vehicle["Application_ID"],))
            vehicle["Purpose_Details"] = cursor.fetchone() or {}
        elif vehicle["Application_Purpose"] == "COMMERCIAL":
            cursor.execute("SELECT Fleet_Size, Goods_Covered, Business_Use_Type FROM commercial WHERE Application_ID = %s", (vehicle["Application_ID"],))
            vehicle["Purpose_Details"] = cursor.fetchone() or {}
        else:
            vehicle["Purpose_Details"] = {}

        # Fetch additional vehicle-specific info
        if vehicle["Vehicle_Type"] == "SEDAN":
            cursor.execute("SELECT Trunk_Size, Fuel_Efficiency FROM sedan WHERE Vehicle_ID = %s", (vehicle["Vehicle_ID"],))
            vehicle["Additional_Info"] = cursor.fetchone() or {}
        elif vehicle["Vehicle_Type"] == "SUV":
            cursor.execute("SELECT Towing_Capacity, All_Wheel_Drive FROM suv WHERE Vehicle_ID = %s", (vehicle["Vehicle_ID"],))
            vehicle["Additional_Info"] = cursor.fetchone() or {}
        elif vehicle["Vehicle_Type"] == "MOTORCYCLE":
            cursor.execute("SELECT Engine_Displacement, Helmet_Storage FROM motorcycle WHERE Vehicle_ID = %s", (vehicle["Vehicle_ID"],))
            vehicle["Additional_Info"] = cursor.fetchone() or {}
        elif vehicle["Vehicle_Type"] == "TRUCK":
            cursor.execute("SELECT Payload_Capacity, Number_Of_Tyres FROM truck WHERE Vehicle_ID = %s", (vehicle["Vehicle_ID"],))
            vehicle["Additional_Info"] = cursor.fetchone() or {}
        elif vehicle["Vehicle_Type"] == "VAN":
            cursor.execute("SELECT Seating_Capacity, Cargo_Space FROM van WHERE Vehicle_ID = %s", (vehicle["Vehicle_ID"],))
            vehicle["Additional_Info"] = cursor.fetchone() or {}
        else:
            vehicle["Additional_Info"] = {}

    return render_template("view/view_vehicles.html", vehicles=vehicles)

@app.route('/view/view_applications')
def view_applications():
    # Fetch all applications and their basic details
    cursor.execute("""
        SELECT 
            a.Application_ID,
            a.Application_Date,
            a.Application_Status,
            a.Application_Purpose,
            ph.Policyholder_Name,
            ip.Policy_Number
        FROM APPLICATION a
        LEFT JOIN POLICYHOLDER ph ON a.Policyholder_ID = ph.Policyholder_ID
        LEFT JOIN INSURANCE_POLICY ip ON a.Policy_ID = ip.Policy_ID;
    """)
    application_data = cursor.fetchall()

    # Debugging print to verify structure
    print(application_data)

    # Prepare data for rendering
    applications = []
    for row in application_data:
        application = {
            'application_id': row['Application_ID'],
            'application_date': row['Application_Date'],
            'application_status': row['Application_Status'],
            'application_purpose': row['Application_Purpose'],
            'policyholder_name': row['Policyholder_Name'],
            'policy_number': row['Policy_Number']
        }
        applications.append(application)

    return render_template('view/view_applications.html', applications=applications)


# Additional routes for CRUD operations and queries go here
@app.route("/view/view_policies")
def view_policies():
    query = """
        SELECT 
            insurance_policy.Policy_ID AS Policy_ID, 
            insurance_policy.Policy_Number AS Policy_Number, 
            insurance_policy.Policy_Type AS Policy_Type, 
            insurance_policy.Policy_Premium_Amount AS Policy_Premium_Amount,
            comprehensive_coverage.Repair_Coverage_Limit AS Repair_Coverage_Limit,
            comprehensive_coverage.Roadside_Assistance_Included AS Roadside_Assistance_Included,
            comprehensive_coverage.Theft_Coverage AS Theft_Coverage,
            third_party_coverage.Liability_Coverage_Limit AS Liability_Coverage_Limit,
            third_party_coverage.Property_Damage_Liability AS Property_Damage_Liability,
            third_party_coverage.Injury_Liability_Coverage AS Injury_Liability_Coverage
        FROM insurance_policy
        LEFT JOIN comprehensive_coverage ON insurance_policy.Policy_ID = comprehensive_coverage.Policy_ID
        LEFT JOIN third_party_coverage ON insurance_policy.Policy_ID = third_party_coverage.Policy_ID
    """
    cursor.execute(query)
    policies = cursor.fetchall()

    formatted_policies = [
        {
            "Policy_ID": policy["Policy_ID"],
            "Policy_Number": policy["Policy_Number"],
            "Policy_Type": policy["Policy_Type"],
            "Policy_Premium_Amount": policy["Policy_Premium_Amount"],
            "Repair_Coverage_Limit": policy.get("Repair_Coverage_Limit"),
            "Roadside_Assistance_Included": policy.get("Roadside_Assistance_Included"),
            "Theft_Coverage": policy.get("Theft_Coverage"),
            "Liability_Coverage_Limit": policy.get("Liability_Coverage_Limit"),
            "Property_Damage_Liability": policy.get("Property_Damage_Liability"),
            "Injury_Liability_Coverage": policy.get("Injury_Liability_Coverage"),
        }
        for policy in policies
    ]

    return render_template("view/view_policies.html", policies=formatted_policies)

@app.route('/view/view_policyholders_premiums')
def view_policyholders_premiums():
    # SQL query to calculate total premiums for each policyholder
    cursor.execute("""
        SELECT 
            ph.Policyholder_ID,
            ph.Policyholder_Name,
            ph.Policyholder_Contact_Number,
            ph.Policyholder_Email,
            SUM(ip.Policy_Premium_Amount) AS Total_Premium
        FROM POLICYHOLDER ph
        INNER JOIN APPLICATION a ON ph.Policyholder_ID = a.Policyholder_ID
        INNER JOIN INSURANCE_POLICY ip ON a.Policy_ID = ip.Policy_ID
        WHERE a.Application_Status = 'Approved'
        GROUP BY ph.Policyholder_ID, ph.Policyholder_Name, ph.Policyholder_Contact_Number, ph.Policyholder_Email;
    """)
    policyholders_data = cursor.fetchall()

    # Debugging print to verify the result
    print(policyholders_data)

    # Prepare data for rendering
    policyholders = []
    for row in policyholders_data:
        policyholder = {
            'policyholder_id': row['Policyholder_ID'],
            'name': row['Policyholder_Name'],
            'contact_number': row['Policyholder_Contact_Number'],
            'email': row['Policyholder_Email'],
            'total_premium': row['Total_Premium']
        }
        policyholders.append(policyholder)

    return render_template('view/view_policyholders_premiums.html', policyholders=policyholders)

@app.route('/view/view_vehicles_insured')
def view_vehicles_insured():
    # SQL query to get vehicle insurance details, policy coverage, and expiration dates
    cursor.execute("""
        SELECT 
            v.Vehicle_ID, 
            v.Vehicle_Plate_Num,
            v.Vehicle_Type,
            ip.Policy_Number,
            ip.Policy_Type,
            tpc.Liability_Coverage_Limit AS Liability_Limit,
            tpc.Property_Damage_Liability AS Property_Damage_Limit,
            tpc.Injury_Liability_Coverage AS Injury_Limit,
            cpc.Repair_Coverage_Limit AS Repair_Limit,
            CASE 
                WHEN cpc.Roadside_Assistance_Included = 1 THEN 'Included'
                ELSE 'Not Included' 
            END AS Roadside_Assistance,
            CASE 
                WHEN cpc.Theft_Coverage = 1 THEN 'Included'
                ELSE 'Not Included' 
            END AS Theft_Coverage,
            ap.Policy_Start_Date,
            ap.Policy_End_Date
        FROM VEHICLE v
        JOIN APPLICATION a ON v.Application_ID = a.Application_ID
        JOIN INSURANCE_POLICY ip ON a.Policy_ID = ip.Policy_ID
        LEFT JOIN THIRD_PARTY_COVERAGE tpc ON ip.Policy_ID = tpc.Policy_ID
        LEFT JOIN COMPREHENSIVE_COVERAGE cpc ON ip.Policy_ID = cpc.Policy_ID
        JOIN ACTIVE_POLICY ap ON a.Application_ID = ap.Application_ID
        WHERE a.Application_Status = 'Approved'
        ORDER BY v.Vehicle_ID ASC;
    """)
    vehicles_data = cursor.fetchall()

    # Prepare data for rendering
    vehicles = []
    for row in vehicles_data:
        coverage_details = {}

        if row['Liability_Limit']:  # If Third Party Coverage exists
            coverage_details = {
                'coverage_type': 'Third Party Coverage',
                'liability_limit': row['Liability_Limit'],
                'property_damage_limit': row['Property_Damage_Limit'],
                'injury_limit': row['Injury_Limit'],
            }
        elif row['Repair_Limit']:  # If Comprehensive Coverage exists
            coverage_details = {
                'coverage_type': 'Comprehensive Coverage',
                'repair_limit': row['Repair_Limit'],
                'roadside_assistance': row['Roadside_Assistance'],
                'theft_coverage': row['Theft_Coverage'],
            }
        else:
            coverage_details = {'coverage_type': 'No Coverage'}

        vehicle = {
            'vehicle_id': row['Vehicle_ID'],
            'plate_number': row['Vehicle_Plate_Num'],
            'vehicle_type': row['Vehicle_Type'],
            'policy_number': row['Policy_Number'],
            'policy_type': row['Policy_Type'],
            'coverage_details': coverage_details,
            'policy_start_date': row['Policy_Start_Date'],
            'policy_end_date': row['Policy_End_Date']
        }
        vehicles.append(vehicle)

    return render_template('view/view_vehicles_insured.html', vehicles=vehicles)

@app.route("/view/policy_bills")
def policy_bills():
    # Query to fetch policy bills
    query = """
        SELECT 
            ip.Policy_ID,
            ip.Policy_Number,
            ip.Policy_Premium_Amount,
            COUNT(a.Application_ID) AS Bill_Count
        FROM INSURANCE_POLICY ip
        LEFT JOIN APPLICATION a ON ip.Policy_ID = a.Policy_ID
        WHERE a.Application_Status = 'Approved'
        GROUP BY ip.Policy_ID, ip.Policy_Number, ip.Policy_Premium_Amount
        ORDER BY ip.Policy_ID ASC;
    """
    cursor.execute(query)
    policies = cursor.fetchall()

    return render_template("view/policy_bills.html", policies=policies)

@app.route("/view/monthly_sales")
def monthly_sales():
    # Fetch raw data from the database
    query = """
        SELECT 
            ap.Policy_Start_Date,
            ap.Active_Policy_ID,
            ip.Policy_Premium_Amount
        FROM active_policy ap
        JOIN INSURANCE_POLICY ip ON ap.Active_Policy_ID = ip.Policy_ID
        WHERE ap.Policy_Start_Date IS NOT NULL;
    """
    cursor.execute(query)
    raw_data = cursor.fetchall()

    # Prepare data using Python logic
    monthly_data = defaultdict(lambda: {"Policy_Count": 0, "Total_Premium": 0.0})

    for record in raw_data:
        # Extract the month-year from Policy_Start_Date
        month_year = record['Policy_Start_Date'].strftime('%Y-%m')
        monthly_data[month_year]["Policy_Count"] += 1
        monthly_data[month_year]["Total_Premium"] += float(record['Policy_Premium_Amount'])

    # Convert the defaultdict to a sorted list for rendering
    sales_data = [
        {"Month": month, "Policy_Count": data["Policy_Count"], "Total_Premium": data["Total_Premium"]}
        for month, data in sorted(monthly_data.items(), reverse=True)
    ]

    return render_template("view/monthly_sales.html", sales_data=sales_data)


@app.route("/view/top_vehicles")
def top_vehicles():
    query = """
        SELECT 
            vehicle.Vehicle_Type, 
            COUNT(active_policy.Active_Policy_ID) AS NumberOfPolicies
        FROM 
            vehicle
        JOIN 
            application ON vehicle.Application_ID = application.Application_ID
        JOIN 
            active_policy ON application.Application_ID = active_policy.Application_ID
        GROUP BY 
            vehicle.Vehicle_Type
        ORDER BY 
            NumberOfPolicies DESC
        LIMIT 5
    """
    cursor.execute(query)
    top_vehicle_types = cursor.fetchall()
    return render_template("view/top_vehicles.html", top_vehicle_types=top_vehicle_types)

# Create a route to display the vehicles that policyholders applied for insurance
@app.route("/view/policyholder_vehicles")
def policyholder_vehicles():
    # SQL query to get the vehicles associated with all policyholders
    query = """
    SELECT
        ph.Policyholder_ID,
        ph.Policyholder_Name,
        v.Vehicle_ID,
        v.Vehicle_Plate_Num,
        v.Vehicle_Type,
        v.Vehicle_Manufacture_Year
    FROM POLICYHOLDER ph
    JOIN APPLICATION a ON ph.Policyholder_ID = a.Policyholder_ID
    JOIN VEHICLE v ON a.Application_ID = v.Application_ID
    ORDER BY ph.Policyholder_ID;
    """

    cursor.execute(query)
    vehicles_data = cursor.fetchall()

    return render_template("view/policyholder_vehicles.html", vehicles_data=vehicles_data)

#Delete functions**********************************************************************************************

@app.route("/delete_policy/<int:policy_id>", methods=["POST"])
def delete_policy(policy_id):
    try:
        # Fetch all application IDs related to the policy
        cursor.execute("""
            SELECT Application_ID 
            FROM application 
            WHERE Policy_ID = %s
        """, (policy_id,))
        applications = cursor.fetchall()

        # Extract Application_IDs
        application_ids = [app['Application_ID'] for app in applications]

        if application_ids:
            # Delete corresponding active policies
            cursor.execute("""
                DELETE FROM active_policy 
                WHERE Application_ID IN (%s)
            """ % ','.join(['%s'] * len(application_ids)), tuple(application_ids))

        # Delete from `application` table (linked to the policy)
        # cursor.execute("DELETE FROM application WHERE Policy_ID = %s", (policy_id,))

        # Finally, delete the insurance policy itself
        cursor.execute("DELETE FROM insurance_policy WHERE Policy_ID = %s", (policy_id,))

        db.commit()
        return redirect("/view_policies")
    except Exception as e:
        print(f"Error deleting policy: {e}")
        db.rollback()
        return redirect("/view_policies")

@app.route("/delete_policyholder/<int:policyholder_id>", methods=["POST"])
def delete_policyholder(policyholder_id):
    try:
        # Delete all associated vehicles
        cursor.execute("""
            DELETE FROM vehicle 
            WHERE Application_ID IN (
                SELECT Application_ID 
                FROM application 
                WHERE Policyholder_ID = %s
            )
        """, (policyholder_id,))

        # Fetch all applications related to the policyholder
        cursor.execute("""
            SELECT Application_ID 
            FROM application 
            WHERE Policyholder_ID = %s
        """, (policyholder_id,))
        applications = cursor.fetchall()

        # Extract application IDs
        application_ids = [app['Application_ID'] for app in applications]

        if application_ids:
            # Delete corresponding active policies
            cursor.execute("""
                DELETE FROM active_policy 
                WHERE Application_ID IN (%s)
            """ % ','.join(['%s'] * len(application_ids)), tuple(application_ids))

            # Delete corresponding insurance policies
            cursor.execute("""
                DELETE FROM insurance_policy 
                WHERE Policy_ID IN (
                    SELECT Policy_ID 
                    FROM application 
                    WHERE Application_ID IN (%s)
                )
            """ % ','.join(['%s'] * len(application_ids)), tuple(application_ids))

        # Delete applications linked to this policyholder
        cursor.execute("""
            DELETE FROM application 
            WHERE Policyholder_ID = %s
        """, (policyholder_id,))

        # Finally, delete the policyholder
        cursor.execute("DELETE FROM policyholder WHERE Policyholder_ID = %s", (policyholder_id,))

        db.commit()
        return redirect("/view_policyholders")
    except Exception as e:
        print(f"Error deleting policyholder: {e}")
        db.rollback()
        return redirect("/view_policyholders")

#Update functions**********************************************************************************************

@app.route("/update_policy/<int:policy_id>", methods=["GET", "POST"])
def update_policy(policy_id):
    if request.method == "POST":
        # Get updated data from the form
        policy_number = request.form['policy_number']
        policy_type = request.form['policy_type']
        policy_premium = request.form['policy_premium']

        # Update the policy in the database
        cursor.execute("""
            UPDATE insurance_policy
            SET Policy_Number = %s,
                Policy_Type = %s,
                Policy_Premium_Amount = %s
            WHERE Policy_ID = %s
        """, (policy_number, policy_type, policy_premium, policy_id))
        db.commit()
        return redirect("/view_policies")
    
    # If GET request, fetch the current details of the policy
    cursor.execute("SELECT * FROM insurance_policy WHERE Policy_ID = %s", (policy_id,))
    policy = cursor.fetchone()
    return render_template("update/update_policy.html", policy=policy)

@app.route("/update_vehicle/<int:vehicle_id>", methods=["GET", "POST"])
def update_vehicle(vehicle_id):
    if request.method == "POST":
        # Get updated data from the form
        vehicle_plate_num = request.form['vehicle_plate_num']
        vehicle_type = request.form['vehicle_type']
        vehicle_manufacture_year = request.form['vehicle_manufacture_year']

        # Update the vehicle in the database
        cursor.execute("""
            UPDATE vehicle
            SET Vehicle_Plate_Num = %s,
                Vehicle_Type = %s,
                Vehicle_Manufacture_Year = %s
            WHERE Vehicle_ID = %s
        """, (vehicle_plate_num, vehicle_type, vehicle_manufacture_year, vehicle_id))
        db.commit()
        return redirect("/view/view_vehicles")
    
    # If GET request, fetch the current details of the vehicle
    cursor.execute("SELECT * FROM vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    return render_template("update/update_vehicle.html", vehicle=vehicle)

@app.route("/update_policyholder/<int:policyholder_id>", methods=["GET", "POST"])
def update_policyholder(policyholder_id):
    if request.method == "POST":
        # Get updated data from the form
        name = request.form['name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        driving_license_number = request.form['driving_license_number']

        # Update the policyholder in the database
        cursor.execute("""
            UPDATE policyholder
            SET Policyholder_Name = %s,
                Policyholder_Contact_Number = %s,
                Policyholder_Email = %s,
                Policyholder_Date_Of_Birth = %s,
                Policyholder_Driving_License_Number = %s
            WHERE Policyholder_ID = %s
        """, (name, contact_number, email, date_of_birth, driving_license_number, policyholder_id))
        db.commit()
        return redirect("/view/view_policyholders")
    
    # If GET request, fetch the current details of the policyholder
    cursor.execute("SELECT * FROM policyholder WHERE Policyholder_ID = %s", (policyholder_id,))
    policyholder = cursor.fetchone()
    return render_template("update/update_policyholder.html", policyholder=policyholder)

@app.route("/update_application/<int:application_id>", methods=["GET", "POST"])
def update_application(application_id):
    if request.method == "POST":
        # Get updated data from the form
        application_status = request.form['application_status']
        application_purpose = request.form['application_purpose']
        application_date = request.form['application_date']

        # Update the application in the database
        cursor.execute("""
            UPDATE application
            SET Application_Status = %s,
                Application_Purpose = %s,
                Application_Date = %s
            WHERE Application_ID = %s
        """, (application_status, application_purpose, application_date, application_id))
        db.commit()
        return redirect("/view/view_applications")
    
    # If GET request, fetch the current details of the application
    cursor.execute("SELECT * FROM application WHERE Application_ID = %s", (application_id,))
    application = cursor.fetchone()
    
    # Fetch related policyholder and policy details for display
    cursor.execute("""
        SELECT 
            policyholder.Policyholder_Name,
            insurance_policy.Policy_Number
        FROM 
            application
        LEFT JOIN 
            policyholder ON application.Policyholder_ID = policyholder.Policyholder_ID
        LEFT JOIN 
            insurance_policy ON application.Policy_ID = insurance_policy.Policy_ID
        WHERE 
            application.Application_ID = %s
    """, (application_id,))
    related_info = cursor.fetchone()

    return render_template("update/update_application.html", application=application, related_info=related_info)

@app.route("/delete_application/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    try:
        # Execute the DELETE statement
        cursor.execute("DELETE FROM application WHERE Application_ID = %s", (application_id,))
        db.commit()  # Commit the changes to the database
        return redirect("/list_applications")  # Redirect to the applications list
    except Exception as e:
        print(f"Error deleting application: {e}")
        return redirect("/list_applications")  # Redirect back in case of error
#*******************************************************************************************************

@app.route("/debug_directory")
def debug_directory():
    # Get the current working directory
    project_root = os.getcwd()

    # Walk through the directory structure
    directory_structure = []
    for root, dirs, files in os.walk(project_root):
        directory_structure.append({
            "root": root,
            "dirs": dirs,
            "files": files
        })

    # Render the structure as plain text for debugging
    response = ""
    for item in directory_structure:
        response += f"Root: {item['root']}\n"
        response += "Directories:\n" + "\n".join(f"  {d}" for d in item['dirs']) + "\n"
        response += "Files:\n" + "\n".join(f"  {f}" for f in item['files']) + "\n\n"

    return f"<pre>{response}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
    

    
    


