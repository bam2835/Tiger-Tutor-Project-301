# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:16:35 2026

@author: bam2835, elv3453


Please contact me regarding issues, improvements, tweaks such as adding new schools
Brenden McBride - RIT Student '26'
914 - 483 - 6156


"""

from pyomo.environ import*
model = AbstractModel()
from pyomo.opt import SolverStatus, TerminationCondition 

""" In a separate edition that we made, we included a "loading" screen that tracks if the model is actively solving and also the
time it took to solve. We did not include this in this submission because it was AI generated, and we did not understand it. We have
this model and can provide it to you if you would like it, granted you will use this code at some point."""


# SETS
model.TUTORS = Set()  # Set of tutors
model.TSLOTS = Set()  # Set of class-time slots (each = specific class + day + time)
model.CLASSES = Set()  # Set of 8 class times (each class time has multiple day slots)
model.PAIRS = Set(within=model.TUTORS * model.TUTORS)  # Each element is (t, t') where t != t'

# Parameters
model.slot_class = Param(model.TSLOTS, within=model.CLASSES)  # Mapping: which class time each slot belongs to
model.avlbl = Param(model.TUTORS, model.TSLOTS, within=Binary)  # 1 if tutor t is available for slot c
model.lead = Param(model.TUTORS, within=Binary)  # 1 if tutor t is willing to be a team lead
model.drive = Param(model.TUTORS, within=Binary)  # 1 if tutor t can drive themselves
model.carpool = Param(model.TUTORS, within=Binary)  # 1 if tutor t can drive others (carpool driver)
model.prevClass = Param(model.TUTORS, model.TSLOTS, within=Binary)  # 1 if tutor t worked this exact class-time last semester
model.prevSchool = Param(model.TUTORS, model.TSLOTS, within=Binary)  # 1 if tutor t worked at this school last semester
model.gradeOK = Param(model.TUTORS, model.TSLOTS, within=Binary)  # 1 if tutor t is comfortable with grade level at slot c

# DVs
model.x = Var(model.TUTORS, model.TSLOTS, within=Binary)  # 1 if tutor t is assigned to slot c
model.y = Var(model.TSLOTS, within=Binary)  # 1 if a team is assigned to slot c
model.L = Var(model.TUTORS, model.TSLOTS, within=Binary)  # 1 if tutor t is the team lead for slot c
model.z = Var(model.PAIRS, model.TSLOTS, within=Binary)  # 1 if both tutors in PAIRS are assigned to same slot c
model.d = Var(model.TSLOTS, within=Binary)  # 1 if slot c has at least one carpool driver
model.maxVisits = Var(within=NonNegativeIntegers)  # Tracks the most visits any single class time receives
model.minVisits = Var(within=NonNegativeIntegers)  # Tracks the fewest visits any single class time receives

# Objective Function
#OBJECTIVE WEIGHTS 
""" SEE BELOW """

W_prevClass = 1
W_prevSchool = 1
W_pair = 1
W_slot = 1
W_assign = 0.5
W_balance = 1 

"""
Explaination: The higher weight, the greater the priority of that accomplishment. 
We can do this since we are maximizing our objective.

To Prioritize...
   * Keeping tutors in the same class as last semester: Increase W_prevClass
   * Keeping tutors the same school: Increase W_prevSchool 
   * Honor tutor-made pairing preferences: Increase W_pair
   * Promote even distribution of teams across classes: Increase W_balance
   * Favor assigning more tutors overall: Increase W_assign (slightly - not the main objective)
   * Evening out visits across class times: Increase W_balance

"""

#Objective Function
def objective_rule(model):
    return (
        W_prevClass * sum(model.prevClass[t, c] * model.x[t, c]
                          for t in model.TUTORS for c in model.TSLOTS)

        + W_prevSchool * sum(model.prevSchool[t, c] * model.x[t, c]
                            for t in model.TUTORS for c in model.TSLOTS)

        + W_pair * sum(model.z[t, t2, c]
                       for (t, t2) in model.PAIRS for c in model.TSLOTS)

        + W_slot * sum(model.y[c] for c in model.TSLOTS)

        + W_assign * sum(model.x[t, c]
                         for t in model.TUTORS for c in model.TSLOTS)

        - W_balance * (model.maxVisits - model.minVisits)
    )

model.obj = Objective(rule=objective_rule, sense=maximize)

# ST

# Each tutor assigned to at most 1 slot
def one_team_rule(model, t):
    return sum(model.x[t,c] for c in model.TSLOTS) <= 1
model.one_team = Constraint(model.TUTORS, rule=one_team_rule)

# Availability
def availability_rule(model, t, c):
    return model.x[t,c] <= model.avlbl[t,c]
model.availability = Constraint(model.TUTORS, model.TSLOTS, rule=availability_rule)

# Team size of 2-5 tutors
# Lower Bound
def team_size_lower(model, c):
    return sum(model.x[t,c] for t in model.TUTORS) >= 2 * model.y[c]#CHANGE THE NUMBER 5 to get a different min visits
model.team_size_l = Constraint(model.TSLOTS, rule=team_size_lower)

# Upper bound
def team_size_upper(model, c):
    return sum(model.x[t,c] for t in model.TUTORS) <= 5 * model.y[c] #CHANGE THE NUMBER 5 to get a different max visits
model.team_size_u = Constraint(model.TSLOTS, rule=team_size_upper)

# Team lead requirements
def lead_count_rule(model, c):
    return sum(model.L[t,c] for t in model.TUTORS) == model.y[c]
model.lead_count = Constraint(model.TSLOTS, rule=lead_count_rule)

def lead_assign_rule(model, t, c):
    return model.L[t,c] <= model.x[t,c]
model.lead_assign = Constraint(model.TUTORS, model.TSLOTS, rule=lead_assign_rule)

def lead_eligibility_rule(model, t, c):
    return model.L[t,c] <= model.lead[t]
model.lead_eligibility = Constraint(model.TUTORS, model.TSLOTS, rule=lead_eligibility_rule)

# Each class time gets a minimum of 2 visits per week
def class_coverage_rule(model, k):
    return sum(model.y[c] for c in model.TSLOTS if model.slot_class[c] == k) >= 2
model.class_coverage = Constraint(model.CLASSES, rule=class_coverage_rule)

# Transportation constraint
def carpool_def_rule(model, c):
    return model.d[c] <= sum(model.carpool[t] * model.x[t, c] for t in model.TUTORS)

def transport_rule(model, c):
    return sum(model.drive[t] * model.x[t, c] for t in model.TUTORS) + model.d[c] >= \
           sum(model.x[t, c] for t in model.TUTORS)

model.carpool_def = Constraint(model.TSLOTS, rule=carpool_def_rule)
model.transport = Constraint(model.TSLOTS, rule=transport_rule)


# Preference linking (z variables)
def z_upper1_rule(model, t, t2, c):
    return model.z[(t, t2), c] <= model.x[t, c]
model.z_upper1 = Constraint(model.PAIRS, model.TSLOTS, rule=lambda m, t, t2, c: z_upper1_rule(m, t, t2, c))

def z_upper2_rule(model, t, t2, c):
    return model.z[(t, t2), c] <= model.x[t2, c]
model.z_upper2 = Constraint(model.PAIRS, model.TSLOTS, rule=lambda m, t, t2, c: z_upper2_rule(m, t, t2, c))

def z_lower_rule(model, t, t2, c):
    return model.z[(t, t2), c] >= model.x[t, c] + model.x[t2, c] - 1
model.z_lower = Constraint(model.PAIRS, model.TSLOTS, rule=lambda m, t, t2, c: z_lower_rule(m, t, t2, c))

# Tutors willing to work with 5/6th vs 8th graders
def grade_rule(model, t, c):
    return model.x[t,c] <= model.gradeOK[t,c]
model.grade_constraint = Constraint(model.TUTORS, model.TSLOTS, rule=grade_rule)

# Balance constraints - track max and min visits across class times
def max_visits_rule(model, k):
    return model.maxVisits >= sum(model.y[c] for c in model.TSLOTS if model.slot_class[c] == k)
model.max_visits = Constraint(model.CLASSES, rule=max_visits_rule)

def min_visits_rule(model, k):
    return model.minVisits <= sum(model.y[c] for c in model.TSLOTS if model.slot_class[c] == k)
model.min_visits = Constraint(model.CLASSES, rule=min_visits_rule)

# Create an Instance and Solve the Model
data = DataPortal()
data.load(filename="tutordata.dat", model=model)

optimizer = SolverFactory('glpk')
instance = model.create_instance(data)

results = optimizer.solve(instance, tee=False)

if (results.solver.status == SolverStatus.ok and
    results.solver.termination_condition == TerminationCondition.optimal):

    class_names = {
        'SCH12_5TH':    'School 12 – 5th Grade (7:50–8:30am)',
        'SCH12_6TH':    'School 12 – 6th Grade (1:10–1:50pm)',
        'LJMS_AC_1000': 'Loretta Johnson – AC Days (10:00–11:33am)',
        'LJMS_AC_753':  'Loretta Johnson – AC Lab (7:53–8:37am)',
        'LJMS_BD_1257': 'Loretta Johnson – BD Days (12:57–2:30pm)',
        'LJMS_BD_1136': 'Loretta Johnson – BD Lab (11:36–12:21pm)',
        'SOTA_1054':    'School of the Arts (10:54–11:36am)',
        'SOTA_1227':    'School of the Arts (12:27–1:10pm)',
        # Additional class names can be added here if data file is ever expanded
    }

    email_body = []

    email_body.append("\n==================================================")
    email_body.append("        GENERATED EMAIL NOTIFICATION")
    email_body.append("==================================================\n")
    email_body.append("")
    email_body.append("Hello all, below I have listed the weekly tutoring assignments.")
    email_body.append("Please let me know if there are any issues.")
    email_body.append("")

    for c in instance.TSLOTS:
        if instance.y[c].value > 0.5:

            team = [t for t in instance.TUTORS if instance.x[t, c].value > 0.5]
            lead = [t for t in instance.TUTORS if instance.L[t, c].value > 0.5]
            needs_ride = [t for t in team if instance.drive[t] == 0 and instance.carpool[t] == 0]
            drivers = [t for t in team if instance.drive[t] == 1 or instance.carpool[t] == 1]

            school_code = "_".join(str(c).split("_")[:-1])  # strips day, e.g. SCH12_5TH_Mon -> SCH12_5TH
            school = class_names.get(school_code, school_code)

            email_body.append("-" * 50)
            email_body.append(f"Class: {school}")
            email_body.append(f"Day:   {str(c).split('_')[-1]}")
            email_body.append("")
            email_body.append(f"Team Members: {', '.join(map(str, team))}")
            email_body.append(f"Team Lead:    {', '.join(map(str, lead))}")

            if needs_ride:
                email_body.append(
                    f"Transportation: NEED RIDE -> {', '.join(map(str, needs_ride))} | "
                    f"Drivers -> {', '.join(map(str, drivers))}"
                )
            else:
                email_body.append("Transportation: All members have transportation")

            email_body.append("")

    email_body.append("=" * 50)
    email_body.append("Please coordinate with your team ahead of time.")
    email_body.append("Thank you for supporting T3!")
    email_body.append("- Dr. Katie")
    email_body.append("=" * 50)

    print("\n".join(email_body))

    print("\n===== COVERAGE CHECK =====")
    for k in instance.CLASSES:
        count = sum(1 for c in instance.TSLOTS if instance.slot_class[c] == k and instance.y[c].value > 0.5)
        print(f"{class_names.get(k, k)}: {count} visits covered")

else:
    print("\n Solver did NOT find optimal solution")
    print("Status:", results.solver.status)
    print("Termination:", results.solver.termination_condition)

"""

    The following code is designed to create individualized emails to each team.
    While this idea works for keeping things concise, sending out 40 emails is inefficient and impractical.
    However, it is left here as an option if you had a preference. This belongs right after the if statement 
    (if (results.solver.status == SolverStatus.ok and)...
    
    
    print("\n" + "="*50)
    print("        GENERATED EMAIL NOTIFICATIONS")
    print("="*50 + "\n")

    for c in instance.TSLOTS:
        if instance.y[c].value > 0.5:
            team = [t for t in instance.TUTORS if instance.x[t, c].value > 0.5]
            lead = [t for t in instance.TUTORS if instance.L[t, c].value > 0.5]
            needs_ride = [t for t in team if instance.drive[t] == 0 and instance.carpool[t] == 0]
            drivers = [t for t in team if instance.drive[t] == 1 or instance.carpool[t] == 1]

            school_code = str(c).split("_")[0]
            school = school_names.get(school_code, school_code)

            print("-"*50)
            print(f"Subject: T3 Assignment – {c}")
            print()
            print("Hello Team,")
            print()
            print(f"You have been assigned to support {school}.")
            print(f"Time Slot: {c}")
            print()
            print(f"Team Members: {', '.join(str(t) for t in team)}")
            print(f"Team Lead: {', '.join(str(t) for t in lead)}")
            if needs_ride:
                print(f"Transportation Note: Tutors {', '.join(str(t) for t in needs_ride)} need a ride.")
                print(f"                     Tutors {', '.join(str(t) for t in drivers)} can drive.")
            else:
                print("Transportation Note: All members have transportation.")
            print()
            print("Please coordinate with your team ahead of time.")
            print("Thank you for supporting T3!")
            print()
            print("- Dr. Katie")
            print("-"*50 + "\n")
    """
    
