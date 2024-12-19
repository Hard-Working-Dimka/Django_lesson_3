from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from random import choice


def find_person(name, year_of_study, group_letter):
    try:
        return Schoolkid.objects.get(full_name__contains=name, year_of_study=year_of_study,
                                     group_letter=group_letter)
    except Schoolkid.DoesNotExist:
        raise Schoolkid.DoesNotExist("Ученик не найден! Проверьте правильность введенных данных.") from None
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned("Найдено несколько учеников! Уточните ФИО.") from None


def fix_marks(name, year_of_study, group_letter):
    schoolkid = find_person(name, year_of_study, group_letter)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=choice([4, 5]))


def remove_chastisements(name, year_of_study, group_letter):
    schoolkid = find_person(name, year_of_study, group_letter)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name, year_of_study, group_letter, lesson):
    schoolkid = find_person(name, year_of_study, group_letter)

    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                   subject__title=lesson).order_by("?").first()
    if lesson is None:
        raise Lesson.DoesNotExist("Предмет не найден! Проверьте правильность ввода.")
    with open("laudatory_messages.txt", "r", encoding="utf8") as file:
        messages = file.readlines()
        massage = choice(messages)
        Commendation.objects.create(teacher=lesson.teacher, subject=lesson.subject, schoolkid=schoolkid,
                                    created=lesson.date, text=massage)
