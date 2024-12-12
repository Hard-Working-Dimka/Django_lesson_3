from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from random import choice


def find_person(name, school_class):
    return Schoolkid.objects.get(full_name__contains=name, year_of_study=school_class[:1],
                                 group_letter=school_class[1:2])


def fix_marks(name, school_class):
    schoolkid = find_person(name, school_class)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=choice([4, 5]))


def remove_chastisements(name, school_class):
    schoolkid = find_person(name, school_class)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name, school_class, lesson):
    schoolkid = find_person(name, school_class)

    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                       subject__title=lesson).order_by("?").first()

    with open("laudatory_messages.txt", "r", encoding="utf8") as file:
        messages = file.readlines()
        massage = choice(messages)
        Commendation.objects.create(teacher=lesson.teacher, subject=lesson.subject, schoolkid=schoolkid,
                                    created=lesson.date, text=massage)
