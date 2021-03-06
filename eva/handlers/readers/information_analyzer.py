from datetime import datetime, timedelta

from handlers.readers.information_map import USER_INFORMATION_MAP


class FinishedCoursesInformationAnalyzer(object):

    def __init__(self, informations):
        self.information_data = informations
        self.history_analysis = {
            "after_2015": [],
            "between_2013_to_2014": [],
            "before_2013": [],
        }

    @property
    def data_analyzed(self):
        """
        After analyzing the user information, it
        will return a dictionary with information
        data divided by the predetermined time
        intervals.
        """
        return self.history_analysis

    def analyze(self):
        """
        Will iterate over the list containing all
        the information acquired, doing the
        individual analysis of each one of them.
        """
        for user_data in self.information_data:
            extract_data = self._extract_data(user_data)

            # Analyze the data by end date
            self._analysis_end_date(extract_data)

    def _analysis_end_date(self, extracted_information_data):
        """
        From a dictionary with the information of a
        user extracted, it will analyze the
        timeframe in which the course was finalized
        and add properly to the dictionary
        "history_analysis".
        """
        datetime_analyzer = DateTimeAnalyzer(
            extracted_information_data["course_end_date"])

        end_date = datetime_analyzer.get_date()

        date_equals_2015 = datetime(2015, 1, 1)
        date_equals_2013 = datetime(2013, 1, 1)

        if end_date is not None:
            check_if_user_finishes_after_2015 = datetime_analyzer.compare_dates(
                end_date, date_equals_2015)

            check_if_user_finishes_before_2013 = datetime_analyzer.compare_dates(
                date_equals_2013, end_date)

            if check_if_user_finishes_after_2015:
                self.history_analysis["after_2015"].append(
                    extracted_information_data)

            elif check_if_user_finishes_before_2013:
                self.history_analysis["before_2013"].append(
                    extracted_information_data)

            else:
                self.history_analysis["between_2013_to_2014"].append(
                    extracted_information_data)

    def _extract_data(self, user_information_list):
        """
        Extracts a user's information from a list and
        stores it in a dictionary containing the data
        that will be used later.
        """
        course_name_value = user_information_list[USER_INFORMATION_MAP["nome_curso"]]
        workload_value = user_information_list[USER_INFORMATION_MAP["carga_horaria"]]
        teaching_format_value = user_information_list[USER_INFORMATION_MAP["formato"]]
        enrollment_status_value = user_information_list[USER_INFORMATION_MAP["sit_matricula"]]
        class_status_value = user_information_list[USER_INFORMATION_MAP["sit_turma"]]
        course_end_date_value = user_information_list[USER_INFORMATION_MAP["dt_fim"]]

        return {
            "course_name": course_name_value,
            "workload": workload_value,
            "teaching": teaching_format_value,
            "enrollment": enrollment_status_value,
            "class_status": class_status_value,
            "course_end_date": course_end_date_value,
        }


class DateTimeAnalyzer(object):

    def __init__(self, date_string):
        self.date_string = date_string

    @classmethod
    def compare_dates(cls, date, date_to_compare):
        try:
            bool_date = date >= date_to_compare
        except TypeError:
            return False
        return bool_date

    def get_date(self):
        """
        It will return a datetime instance if no errors
        occur during the transformations needed to
        stencil the date from a raw set of information.
        """
        splited_date = self._split_datetime(self.date_string)

        if splited_date is None:
            return None

        date_informations = self._get_year_month_day(splited_date)

        if date_informations is None:
            return None

        datetime_instance = self._create_a_datetime_instance(date_informations)

        if datetime_instance is None:
            return None

        return datetime_instance

    def _split_datetime(self, date_string):
        """
        Gets the first ten values ​​of an entry, and divides
        them by using the '-' as a separator, in order to
        get a list with the day, month and year:

        e.g.: 2016-04-12 12:58:17.107
        """
        try:
            date = date_string[:10].split("-")
        except IndexError:
            return None

        return date

    def _get_year_month_day(self, date):
        """
        Check if a list has at least three values
        which will be used as day, month and year.
        """
        YEAR = 0
        MONTH = 1
        DAY = 2

        try:
            year = date[YEAR]
            month = date[MONTH]
            day = date[DAY]
        except IndexError:
            return None

        return (year, month, day)

    def _create_a_datetime_instance(self, date):
        """
        From a list or tuple with three elements
        representing day, month and year, tries
        to create a datetime instance.
        """
        YEAR = 0
        MONTH = 1
        DAY = 2

        try:
            date = datetime(int(date[YEAR]), int(date[MONTH]), int(date[DAY]))
        except (TypeError, ValueError):
            return None

        return date
