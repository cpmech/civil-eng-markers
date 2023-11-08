import csv
import random


# Function to read Jeannette's data file
def read_nettes_data():
    filename = "nettes-data.csv"
    students = {}
    with open(filename, newline="", encoding="utf-8-sig") as f:
        for line in csv.DictReader(f):
            students[line["Student ID"]] = line
    return students


# Function to read Tom's data file
def read_toms_data():
    filename = "toms-data.csv"
    staff = {}
    with open(filename, newline="", encoding="utf-8-sig") as f:
        for line in csv.DictReader(f):
            surname = line["Staff"].split(",")[0]
            staff[surname] = {"Load": 0, "Marking": []}
    return staff


# Load student and staff list
students = read_nettes_data()
staff = read_toms_data()

# Update staff list with load/marking tasks. Also insert additional
# supervisors that are in Jeannette's file but not in Tom's
for student_id, student in students.items():
    surname = student["Supervisor"].split(" ")[1].upper()
    if not surname in staff:
        staff[surname] = {"Load": 1, "Marking": [student_id]}
    else:
        staff[surname]["Marking"].append(student_id)
        staff[surname]["Load"] += 1


# Function to print staff loads
def print_loads():
    for surname, data in staff.items():
        print(f"{surname:>12} : {data['Load']}")


# Print supervisory loads
print("SUPERVISORY LOADS")
print("=================")
print_loads()

# Function to find a marker from the pool of staff
exclude = []


def find_marker(supervisor, max_desired_load):
    # shuffle staff to prevent alphabetical surname bias
    surnames = list(staff.keys())
    random.shuffle(surnames)
    # important: need to sort staff by load (ascending)
    staff_list = [(surname, staff[surname]["Load"]) for surname in surnames]
    staff_list.sort(key=lambda x: x[1])  # sort by load
    for surname, load in staff_list:
        if surname == supervisor or surname in exclude:
            continue
        if load < max_desired_load:
            return surname
    return None


# Randomize student's list (not really necessary, but why not)
random_student_ids = list(students.keys())
random.shuffle(random_student_ids)

# Initiate counter for max desired load
max_desired_load = round(1 + len(students) / len(staff))
max_iterations = 20

# Perform iterations
for student_id in random_student_ids:
    student = students[student_id]
    if student["Marker2"] == "None":
        for iteration in range(max_iterations):
            surname = find_marker(student["Supervisor"], max_desired_load)
            if surname == None:
                max_desired_load += 1
            else:
                student["Marker2"] = surname
                staff[surname]["Load"] += 1
                staff[surname]["Marking"].append(student_id)
                break
        else:
            raise Exception(
                f"cannot find marker for {student_id} after {iteration} iterations"
            )

# Print loads
print("\nSUPERVISOR + MARKER#2 LOADS")
print("===========================")
print_loads()

# Print assignments
print("\nASSIGNMENTS")
print("===========")
print(
    f"{'Course Code':>11}, {'First Name':>15}, {'Last Name':>15}, {'Student ID':>10}, {'Supervisor':>12}, {'Marker2':>12}"
)
for student_id, info in students.items():
    surname = info["Supervisor"].split(" ")[1].upper()
    print(
        f"{info['Course Code']:>11}, {info['First Name']:>15}, {info['Last Name']:>15}, {info['Student ID']:>10}, {surname:>12}, {info['Marker2']:>12}"
    )
