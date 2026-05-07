# Tiger-Tutor-Project-301
Use a Pyomo integer program to create teams of tutors that provides as much support as possible to the classrooms RIT supports.

Project Description:
In fall of 2024 Dr. Katie started the Tiger Tutor Team (T3
) with the help of over 40 RIT student
volunteers. The program has grown each semester, and we currently have 74 volunteer tutors
this spring. T3 takes RIT students and pairsthem with an 8th grade algebra class or a 5th/6th grade
class in the Rochester City School District. Our goal isto keep accelerated 5th and 6th grade math
students excited about math, and to help our 8th gradersto passthe NY State Algebra 1 Regents
exam, an exam required of all NY State students and a gateway to upperlevel math classes. In
our first year we saw failure rates drop by 50% in the classes we supported, and the number of
5s (the highest score possible) triple in the entire district.
RIT tutors are placed into teams, and each team is assigned one classroom time per week to
support. For example, one team supports Mrs. Driscoll’s Tuesday Algebra 1 class from 10:54 to 11:36
am at School ofthe Arts, while anotherteam supportsthe same class but on Thursdays.
The process of creating the teams is extremely time consuming. In order to for Dr. Katie to be
able to sustain and grow the program, an automated team making system needs to be developed.
This year we are supporting 3 schools and 8 different “classes”. They are as follows:
• School #12
• 7:50 – 8:30 am (5th Grade)
• 1:10 – 1:50 pm (6th Grade)
• Loretta Johnson Middle School – 8th Grade Algebra
• 10:00-11:33 AM AC Days
• 7:53 – 8:37 AM AC Days
• 12:57 – 2:30 PM BD Days
• 11:36 – 12:21 PM BD Days
• School of the Arts(SOTA) - 8th Grade Algebra
• 10:54-11:36 AM
• 12:27 – 1:10 PM
Volunteertutors provide us the following information:
• Willingnessto work with 5th/6th graders, 8th graders or both
• If they need transportation (X), if they can drive themselves (S), orif they are willing to be a
carpool driver (C)
• Which days and times they are available
• Which school and class time they worked with the previous semester
• Ifthey have any preferences of people they would like to be on a team with
• If they are willing to be a team lead
The Challenge:
Use an integer program to create teams of tutors that provides as much support as possible to the
classrooms we support.
The considerations accounted for when forming teams are described below:
Considerations for all teams:
• Each team MUST have transportation. IE. at least one carpool driver or all students on
the team must be able to drive themselves.
• Tutors are assigned to only 1 team. For example, Team 1 may consist of John, Pat, and
Xueting. John, Pat and Xueting will not be assigned to any other teams.
• Only 1 Team can be assigned to a specific class and day of the week. For example, Team 1
may be assigned to go to SOTA on Tuesdays from 10:54 am to 11:36 am. No other team can
be assigned this timeslot.
• Teams are only assigned a single time slot each week. For example, Team 1 from above
CANNOT also be assigned to go to SOTA on Thursdaysfrom 12:27 – 1:10 pm.
• There is a preference to keep tutors with the same classrooms as the previous semester, if
that’s not possible, keeping the same school is the next best option.
• There is a preference to put tutors who want to team together on the same team.
• Teams MUST consist of 2 to 5 tutors
• Each classroom meeting time MUST have a designated team lead that is chosen from those
tutors who indicate they were willing to be a team lead.
• We MUST send a team at least twice a week to each class.
• There is a preference to distribute our teams across the classes as evenly as possible. For
example, the schedule in Table 1 would be preferred over the schedule in Table 2.
