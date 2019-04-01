from gsndb.models import District, School, Student, Calendar, Course, Referral, Grade, Behavior, Attendance
from user_app.models import CustomUser
import os
import json
import csv

class ():
    def __init__(self):
        self.model_dic = {
            "gsndb.District": District,
            "gsndb.School": School,
            "gsndb.Student": Student,
            "gsndb.Calendar": Calendar,
            "gsndb.Course": Course,
            "gsndb.Referral": Referral,
            "gsndb.Grade": Grade,
            "gsndb.Behavior": Behavior,
            "gsndb.Attendance": Attendance,
            "user_app.CustomUser": CustomUser,
        }



def get_field_names(model):
    """accepts a model as an argument and returns the fields of that model as a
     list of strings"""
    fields = model._meta.fields
    field_names = []
    for field in fields:
        name = field.__dict__["name"]
        field_names.append(name)
    return set(field_names)


def get_dir_files(path_to_dir):
    """accepts path to directory and returns a dictionary with filenames as keys
     and file objects as values for every file in directory"""
    filenames = os.listdir(path_to_dir)
    file_dic = {}
    for filename in filenames:
        if path_to_dir.endswith("/"):
            file_object = open(path_to_dir + filename)
            file_dic[filename] = file_object
        else:
            file_object = open(path_to_dir + "/" + filename)
            file_dic[filename] = file_object
    return file_dic


def map_csv_to_model(csv_object, model):
    field_names = get_field_names(model)
    return print(field_names)


def csv_to_django_fixture(file_dic, model_dic):
    for filename, file in file_dic.items():
        for django_path, model in model_dic.items():
            if django_path in filename:
                pass
                #print(filename, model)



file_dic = get_dir_files("./dummy_data")

map_csv_to_model(file_dic["gsndb.District.csv"], District)
