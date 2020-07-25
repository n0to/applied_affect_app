from enum import Enum


class Scenario(str, Enum):
    Lecture = "Lecture",
    Quiz = "Quiz",
    Multimedia = "Multimedia"
    Group_Discussion = "Group Discussion"


class Grade(Enum):
    First = 1,
    Second = 2,
    Third = 3,
    Fourth = 4,
    Fifth = 5,
    Sixth = 6,
    Seventh = 7,
    Eighth = 8,
    Ninth = 9,
    Tenth = 10,
    Eleventh = 11,
    Twelfth = 12


class Subject(str, Enum):
    English = "English",
    Hindi = "Hindi",
    Sanskrit = "Sanskrit",
    Kannada = "Kannada",
    Mathematics = "Mathematics",
    Science = "Science",
    Social_Science = "Social Science",
    Physics = "Physics"
    Chemistry = "Chemistry",
    Biology = "Biology",
    Engineering_Drawing = "Engineering Drawing",
    Computer_Science = "Computer Science",
    History = "History",
    Civics = "Civics",
    Geography = "Geography"


class Curriculum(str, Enum):
    ICSE = "ICSE",
    CBSE = "CBSE",
    IB = "IB"


class Section(str, Enum):
    A = "A",
    B = "B",
    C = "C",
    D = "D",
    E = "E",
    F = "F"
