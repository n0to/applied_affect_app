from enum import Enum


class Scenario(Enum):
    Lecture = 1,
    Quiz = 2,
    Multimedia = 3,
    Group_Discussion = 4


class Grade(Enum):
    First = 1,
    Second = 2,
    Third = 3,
    Fourth = 4,
    Fifth = 5,
    Sixth = 6,
    Seventh = 7,
    Eighth = 8,
    Nineth = 9,
    Tenth = 10,
    Eleventh = 11,
    Twelfth = 12


class Subject(Enum):
    English = 1,
    Hindi = 2,
    Sanskrit = 3,
    Kannada = 4,
    Mathematics = 5,
    Science = 6,
    Social_Science = 7,
    Physics = 8,
    Chemistry = 9,
    Biology = 10,
    Engineering_Drawing = 11,
    Computer_Science = 12,
    History = 13,
    Civics = 14,
    Geography = 15


class Curriculum(Enum):
    ICSE = 1,
    CBSE = 2,
    IB = 3


class Section(Enum):
    A = 1,
    B = 2,
    C = 3,
    D = 4,
    E = 5,
    F = 6