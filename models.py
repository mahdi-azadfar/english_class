from shutil import copytree, rmtree
import os
import json

from persiantools import jdatetime

DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
MONTHS = ["Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar", "Mehr", "Aban", "Azar", "Dey", "Bahman",
          "Esfand", ]


# from test import monthlyStatus

class Base:
    semester_name = None
    extra_list = None
    canceling_list = None
    students_list = None
    today = None
    classes_list = None
    COLORS = None
    schedule = None
    colors_dict = None
    last_ids = None

    def __init__(self, key):
        self.key = key
        self.id = self.id_creator(self.key)
        self.finishing_up(data=self)

    @classmethod
    def start(cls):
        cls.back_up()
        # load canceling list
        msg = open('Data/canceling_list.json')
        cls.canceling_list = json.load(msg)
        msg.close()

        # loading extras
        msg = open('Data/extra_list.json')
        cls.extra_list = json.load(msg)
        msg.close()

        # loading schedule
        msg = open('Data/schedule.json')
        cls.schedule = json.load(msg)
        msg.close()

        # loading colors available for new color tag
        msg = open('Data/colors.json')
        cls.colors_dict = json.load(msg)
        msg.close()
        cls.COLORS = cls.colors_dict['list']

        # loading classes data from file and store it in classes_list
        msg = open(f'Data/class_list.json')
        cls.classes_list = json.load(msg)
        msg.close()

        # loading students data from file and store it in students_list
        msg = open(f'Data/student_list.json')
        cls.students_list = json.load(msg)
        msg.close()

        # loading ids from file and store it it _ids_data
        msg = open(f'Data/lasts.json')
        cls.last_ids = json.load(msg)
        msg.close()
        cls.today = jdatetime.JalaliDate.today()
        if cls.last_ids['month'] is None:
            cls.semester_name = ''
        else:
            cls.semester_name = MONTHS[cls.last_ids['month'] - 1]
        ExtraClass.clear_expired_extras_from_schedule()
        EnClass.calculate_students_payments()

    @classmethod
    def back_up(cls):
        now = jdatetime.JalaliDateTime.now()
        path_and_name = f'./backup/{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}/'
        copytree('Data', path_and_name, dirs_exist_ok=True)

    @classmethod
    def load_back_up(cls, backup_name=None):
        if backup_name is None:
            return os.listdir('./backup/')
        else:
            copytree(f'./backup/{backup_name}', 'Data', dirs_exist_ok=True)
            Base.start()

    @classmethod
    def read_back_up(cls):
        today = jdatetime.JalaliDate.today()
        if os.path.exists(f'Data/class records/{today.year}-{today.month - 1}.json'):

            msg = open(f'Data/class records/{Base.today.year}-{Base.today.month - 1}.json')
            data = json.load(msg)
            msg.close()
            return data

        else:
            return False

    @classmethod
    def new_month(cls):
        EnClass.finishing_class(clear_all=True)

        for student in cls.students_list:
            cls.students_list[student]['Status'] = 'Deactive'
        with open(f'Data/student_list.json', 'w') as fo:
            fo.write(json.dumps(cls.students_list))

        # resetting last id
        cls.last_ids['class'] = 0
        with open(f'Data/lasts.json', 'w') as fo:
            fo.write(json.dumps(cls.last_ids))
        rmtree("backup")
        os.makedirs("backup")

    @classmethod
    def id_creator(cls, key):
        cls.last_ids[key] = cls.last_ids[key] + 1
        return cls.last_ids[key]

    @classmethod
    def finishing_up(cls, data=None, path='Data'):

        def save_to_list(obj):
            info = obj.__dict__
            temp_id = info.pop('id')
            temp_id = str(temp_id)
            if obj.key == 'student':
                cls.students_list[temp_id] = obj.data_dict
            else:
                data.pop('key')
                cls.classes_list[temp_id] = data

        if data:
            save_to_list(data)

        # saving extras in file
        with open(f'{path}/extra_list.json', 'w') as fi:
            fi.write(json.dumps(cls.extra_list))

        # saving colors in file
        cls.colors_dict['list'] = cls.COLORS
        with open(f'{path}/colors.json', 'w') as fi:
            fi.write(json.dumps(cls.colors_dict))

        # saving schedule
        with open(f'{path}/schedule.json', 'w') as fi:
            fi.write(json.dumps(cls.schedule))

        # saving class and students data in files

        with open(f'{path}/class_list.json', 'w') as fo:
            fo.write(json.dumps(cls.classes_list))
        with open(f'{path}/student_list.json', 'w') as fo:
            fo.write(json.dumps(cls.students_list))

        # saving last id in file
        with open(f'{path}/lasts.json', 'w') as fo:
            fo.write(json.dumps(cls.last_ids))
        # saving canceling list
        with open('Data/canceling_list.json', 'w') as fi:
            fi.write(json.dumps(cls.canceling_list))

    @classmethod
    def add_canceling_data_to_classes(cls):
        for class_id in cls.classes_list:
            canceled_count = 0
            if Base.canceling_list.get(class_id):
                canceled_count += len(Base.canceling_list[class_id]['canceled_by_teacher'])
                canceled_by_student = len(Base.canceling_list[class_id]['canceled_by_student'])
                if canceled_by_student >= 1:
                    canceled_count += 1
                    cls.classes_list[class_id]['non_refundable_canceling'] = canceled_by_student - 1
                cls.classes_list[class_id]['refundable_canceling'] = canceled_count
        Base.finishing_up()


class Student(Base):
    def __init__(self, data_dict):
        self.status = True
        self.data_dict = data_dict
        self.data_dict['Debt'] = 0
        self.data_dict['Paid'] = 0
        self.data_dict['Status'] = 'Deactive'
        self.id = self.search_student(data=data_dict)
        if self.id:
            self.status = False
        else:
            super().__init__(key='student')

    @classmethod
    def active_students_list(cls):
        final_list = {}
        for student in cls.students_list:
            if cls.students_list[student]['Status'] == 'Active':
                student_full_name = cls.students_list[student]['First Name'] + cls.students_list[student]['Last Name']
                final_list[student] = student_full_name
        return final_list

    @classmethod
    def search_student(cls, student_id=None, data=None, key=None, ids_list=None, full_name=None):
        # search by student id
        if student_id:
            student_id = str(student_id)
            if student_id in cls.students_list:
                if key == 'full_name':
                    return cls.students_list[student_id]["First Name"] +\
                           ' ' + cls.students_list[student_id]["Last Name"]

                else:
                    return cls.students_list[student_id]
            else:
                return []
        # searching for duplicated information
        elif data:
            for student in cls.students_list:
                if cls.students_list[student] == data:
                    return student
            return False
        # search student by name
        elif full_name:
            for student in cls.students_list:
                info = cls.students_list[student]
                if (
                        info["First Name"] == full_name["First Name"] and
                        info["Last Name"] == full_name["Last Name"]
                ):
                    return student
            return False
        # get list of student ids and return dict of information
        elif ids_list:
            temp_dict = {}
            counter = 1
            for s_id in ids_list:
                try:
                    info = cls.students_list[s_id]
                    temp_dict[counter] = info
                    counter += 1
                except KeyError:
                    return False
            return temp_dict

    @classmethod
    def set_students_active(cls, ids_list):
        for student_id in ids_list:
            Base.students_list[str(student_id)]['Status'] = 'Active'
            Base.finishing_up()

    @classmethod
    def edit_student(cls, student_id, data):
        for data_part in data:
            cls.students_list[student_id][data_part] = data[data_part]

        Base.finishing_up()

    @classmethod
    def delete_student(cls, student_id):
        Base.students_list.pop(student_id)
        Base.finishing_up()


class EnClass(Base):
    def __init__(self, students, times, start_date, salary, level, color):
        self.students = students
        Student.set_students_active(students)
        self.times = times
        self.start_date = start_date
        self.salary = salary
        self.level = level
        self.sessions_past = 0
        self.refundable_canceling = 0
        self.non_refundable_canceling = 0
        self.extra = 0
        self.color = color
        self.todo = None
        self.summary = None

        Base.COLORS.pop(Base.COLORS.index(color))
        self.add_to_schedule(times)
        super().__init__(key='class')

    @staticmethod
    def add_to_schedule(times):
        for time in times:
            n1 = time[1].replace(' : ', '')
            n2 = time[2].replace(' : ', '')
            class_time = n1 + '-' + n2
            Base.schedule[time[0]].append(class_time)

    @classmethod
    def is_this_time_free(cls, day, start_time, end_time, compared_session=None):
        today = Base.today
        start_time = int(start_time)
        end_time = int(end_time)

        def last_and_next_class():
            last_class_time = 0
            next_class_time = 2400
            for session in schedule:

                times = session.split('-')
                times[0] = int(times[0])
                times[1] = int(times[1])

                # next class finding
                if next_class_time > times[0] > end_time:
                    next_class_time = times[0]
                if last_class_time < times[1] < start_time:
                    last_class_time = times[1]
            return True, last_class_time, next_class_time

        def checker(start, end):
            start = int(start)
            end = int(end)
            if (start <= end_time <= end) | (start <= start_time <= end):
                return False
            return True

        if compared_session:
            if compared_session[0] == day:
                return checker(compared_session[1], compared_session[2])
            else:
                return True
        else:
            schedule = Base.schedule[day]
            for time in schedule:
                time = time.split('-')
                if checker(start=time[0], end=time[1]) is False:
                    return [False, 'occ', '']
            extra_data = Base.extra_list
            for each_class in extra_data:
                for extra_class in extra_data[each_class]:
                    compare_date = extra_class['date']
                    compare_date = compare_date.split('-')
                    compare_date = jdatetime.JalaliDate(int(compare_date[0]), int(compare_date[1]),
                                                        int(compare_date[2]))
                    if compare_date >= today and extra_class['day'] == day:
                        if checker(start=extra_class['start'], end=extra_class['end']) is False:
                            return [False, each_class, 'extra']
            return last_and_next_class()

    @classmethod
    def edit_class_data(cls, class_id, students, times, level, salary, start_date, color):
        Base.classes_list[class_id]['students'] = students
        Base.classes_list[class_id]['times'] = times
        Base.classes_list[class_id]['start_date'] = start_date
        Base.classes_list[class_id]['salary'] = salary
        Base.classes_list[class_id]['level'] = level
        if Base.classes_list[class_id]['color'] != color:
            Base.COLORS.append(Base.classes_list[class_id]['color'])
            Base.COLORS.pop(Base.COLORS.index(color))
            Base.classes_list[class_id]['color'] = color

        Base.finishing_up()

    @staticmethod
    def str_to_time_format(time_str):
        time_str = time_str.split('-')
        date_fixed = jdatetime.JalaliDate(int(time_str[0]), int(time_str[1]), int(time_str[2]))
        return date_fixed

    @staticmethod
    def all_classes_date_creator():
        today = jdatetime.JalaliDate.today()
        month = today.month
        year = today.year
        days_in_month = today.days_in_month(month=today.month, year=1402)
        first_day_of_month = jdatetime.JalaliDate(year=year, month=month, day=1)
        first_day_of_month_weekday = first_day_of_month.weekday()
        data = Base.classes_list
        result = {}
        for each_class in data:
            first_class_dates = []
            # creat the date of first session in month
            for session in data[each_class]['times']:
                weekday = DAYS.index(session[0])
                if first_day_of_month_weekday <= weekday:
                    first_class_dates.append((weekday - first_day_of_month_weekday + 1))
                else:
                    first_class_dates.append((weekday - first_day_of_month_weekday + 8))
            # calculate rest from first dates
            list_of_dates = []
            # add filter
            for date in first_class_dates:
                added_date = date
                while added_date <= days_in_month:
                    temp = data[each_class]['start_date'].split('-')
                    start_day = int(temp[-1])
                    if added_date > start_day:
                        list_of_dates.append(added_date)
                    added_date += 7
            list_of_dates.sort()
            result[each_class] = list_of_dates
        return result

    @classmethod
    def add_notes(cls, class_id, todo, summary):
        msg = open('Data/classes_history.json')
        classes_history = json.load(msg)
        msg.close()
        classes_history[class_id] = [todo, summary]
        with open('Data/classes_history.json', 'w') as fi:
            fi.write(json.dumps(classes_history))

    @classmethod
    def read_notes(cls, class_id):
        msg = open('Data/classes_history.json')
        classes_history = json.load(msg)
        msg.close()
        if classes_history.get(class_id):
            return classes_history[class_id]
        else:
            return ['', '']

    @staticmethod
    def save_class_history(class_id):
        today = Base.today
        try:
            msg = open(f'Data/class records/{today.year}-{today.month}.json')
            records = json.load(msg)
            msg.close()
        except FileNotFoundError:
            records = {}
        records[class_id] = Base.classes_list[class_id]
        records[class_id]['end_date'] = today.__str__()
        with open(f'Data/class records/{today.year}-{today.month}.json', 'w') as fi:
            fi.write(json.dumps(records))

    @classmethod
    def finishing_class(cls, class_id=None, clear_all=False):

        classes_list = []
        if class_id is not None:
            classes_list.append(class_id)
        elif clear_all:
            classes_list = Base.classes_list

        for each_class in classes_list:
            cls.save_class_history(each_class)
            cls.calculate_students_payments()

            # clear extra classes
            if Base.extra_list.get(each_class):
                for extra_class in Base.extra_list[each_class]:
                    day_sch = Base.schedule[extra_class['day']]
                    n1 = extra_class['start'].replace(' : ', '')
                    n2 = extra_class['end'].replace(' : ', '')
                    index = day_sch.index(f"{n1}-{n2}")
                    day_sch.pop(index)
                Base.extra_list.pop(each_class)

            # clear canceling list
            if Base.canceling_list.get(each_class):
                Base.canceling_list.pop(each_class)

            # clearing schedule
            for time in Base.classes_list[each_class]['times']:
                day_sch = Base.schedule[time[0]]
                n1 = time[1].replace(' : ', '')
                n2 = time[2].replace(' : ', '')
                index = day_sch.index(f"{n1}-{n2}")
                day_sch.pop(index)
                Base.schedule[time[0]] = day_sch

            # give back class color to colors list
            Base.COLORS.append(Base.classes_list[each_class]['color'])

            # deactive students
            for student in Base.classes_list['students']:
                Base.students_list[student]['Status'] = 'Deactive'
        if class_id is not None:
            Base.classes_list.pop(class_id)
        elif clear_all:
            Base.classes_list = {}
        Base.finishing_up()

    @classmethod
    def calculate_students_payments(cls):
        EnClass.calculate_sessions_passed_for_all_classes()
        data = cls.classes_list
        payment_dict = {}
        for each_class in data:
            class_info = data[each_class]
            sessions_past = class_info['sessions_past']
            canceled = class_info['refundable_canceling']
            extra = class_info['extra']
            classes_count = sessions_past - canceled + extra
            payment = int(class_info['salary']) * classes_count
            payment_for_each_student = payment / len(class_info['students'])
            for student in class_info['students']:
                if payment_dict.get(student) is None:
                    payment_dict[student] = 0
                payment_dict[student] += payment_for_each_student
        for student in payment_dict:
            cls.students_list[student]['debt'] = payment_dict[student]
        Base.finishing_up()

    @classmethod
    def calculate_sessions_passed_for_all_classes(cls):
        data = cls.all_classes_date_creator()
        today = jdatetime.JalaliDate.today().day
        for class_id in data:
            sessions_count = 0
            for date in data[class_id]:
                if today > date:
                    sessions_count += 1
            cls.classes_list[class_id]['sessions_past'] = sessions_count
        Base.finishing_up()

    @classmethod
    def search_class(cls, class_id=None, key='data'):
        if class_id is not None:
            if cls.classes_list.get(class_id):

                if key == 'data':
                    return cls.classes_list[class_id]
                elif key == 'students_names':
                    result = ''
                    students = cls.classes_list[class_id]['students']
                    for student in students:
                        if result != '':
                            result += '\n'
                        result += Student.search_student(student_id=student, key='full_name')
                    return result
            else:
                return False
        return cls.classes_list


class ExtraClass:
    def __init__(self, date, day, start, end, class_id):
        self.data = {
            'date': date,
            'day': day,
            'start': start,
            'end': end
        }
        if Base.extra_list.get(class_id):
            pass
        else:
            Base.extra_list[class_id] = []
        Base.extra_list[class_id].append(self.data)
        Base.classes_list[class_id]['extra'] += 1
        corrected_Start = start.replace(' : ', '')
        corrected_end = end.replace(' : ', '')
        Base.schedule[day].append(f'{corrected_Start}-{corrected_end}')
        Base.finishing_up()

    @classmethod
    def clear_expired_extras_from_schedule(cls):
        for each_class in Base.extra_list:
            for extra in Base.extra_list[each_class]:
                temp = extra['date'].split('-')
                extra_class_day = int(temp[-1])
                if Base.today.day > extra_class_day:
                    corrected_start = extra['start'].replace(' : ', '')
                    corrected_end = extra['end'].replace(' : ', '')
                    try:
                        Base.schedule[extra['day']].remove(f'{corrected_start}-{corrected_end}')

                    except KeyError:
                        pass

                    Base.finishing_up()
