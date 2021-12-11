import unittest
import datetime
# need to install for tests.... vs code again....
from freezegun import freeze_time
from todoapp import date_manage


# need to mock data!

class TestDeadlinesMethods(unittest.TestCase):
    
    @freeze_time('2021-12-01')
    def setUp(self):
        self.manager = date_manage.manageDeadlines()
        self.deadline = date_manage.Deadline()
    
    # testing check_deadline method(tomorrow, next week, next month)
    def test_check_deadline(self):
        # simple one
        self.assertEqual(self.deadline.check_deadline('tomorrow'), datetime.date(2021,12,2))
        self.assertEqual(self.deadline.check_deadline('next week'), datetime.date(2021,12,8))
        # by next month adds +30
        self.assertEqual(self.deadline.check_deadline('next month'), datetime.date(2021,12,31))

    # testing cur_month_deadline method inside of manage (By <date>)
    def test_current_month_deadlines(self):
        # correct data
        self.assertEqual(self.deadline.cur_month_deadline('3'), datetime.date(2021, 12, 3))
        self.assertEqual(self.deadline.cur_month_deadline('30'), datetime.date(2021, 12, 30))
        self.assertEqual(self.deadline.cur_month_deadline('25'), datetime.date(2021, 12, 25))
        # a little bit missed
        self.assertEqual(self.manager.check_date('35'), None)

    def test_by_month(self):
        # normal input
        self.assertEqual(self.deadline.by_month('february'), datetime.date(2022, 2, 1))
        self.assertEqual(self.deadline.by_month('january'), datetime.date(2022, 1, 1))
        self.assertEqual(self.deadline.by_month('june'), datetime.date(2022, 6, 1))
        # uppercase
        self.assertEqual(self.deadline.by_month('February'), datetime.date(2022, 2, 1))
        self.assertEqual(self.deadline.by_month('FebRuarY'), datetime.date(2022, 2, 1))
        self.assertEqual(self.deadline.by_month('JUNE'), datetime.date(2022, 6, 1))
        # incorrect format
        self.assertEqual(self.deadline.by_month('june and 3'), None)
        self.assertEqual(self.deadline.by_month('june 21'), None)
        self.assertEqual(self.deadline.by_month('june and february'), None)

    def test_by_month_and_day(self):
        # normal input
        self.assertEqual(self.deadline.by_month_and_day('3', 'march'), datetime.date(2022,3,3))
        self.assertEqual(self.deadline.by_month_and_day('30', 'march'), datetime.date(2022,3,30))
        self.assertEqual(self.deadline.by_month_and_day('30', 'june'), datetime.date(2022,6,30))
        self.assertEqual(self.deadline.by_month_and_day('14', 'september'), datetime.date(2022,9,14))
        self.assertEqual(self.deadline.by_month_and_day('70', 'march'), None)
        self.assertEqual(self.deadline.by_month_and_day('90', 'march'), None)        
        self.assertEqual(self.deadline.by_month_and_day('3', 'March'), datetime.date(2022,3,3)) 
        self.assertEqual(self.deadline.by_month_and_day('3', 'January'), datetime.date(2022,1,3))
        self.assertEqual(self.deadline.by_month_and_day('10', 'AugusT'), datetime.date(2022,8,10))

    def test_in_command(self):
        self.assertEqual(self.manager.deadline.in_command('5'), datetime.date(2021,12,6))
        self.assertEqual(self.manager.deadline.in_command('32'), datetime.date(2022,1,2))
        self.assertEqual(self.manager.deadline.in_command('90'), datetime.date(2022,3,1))
        self.assertEqual(self.manager.deadline.in_command(90), datetime.date(2022,3,1))
        # wrong data
        self.assertEqual(self.manager.deadline.in_command(95), None)
        self.assertEqual(self.manager.deadline.in_command('100'), None)
        self.assertEqual(self.manager.deadline.in_command('In 100'), None)

class TestDeadlinesMethods_version_2(unittest.TestCase):
    # a few test with this date
    @freeze_time('2021-7-01')
    def setUp(self):
        self.manager = date_manage.manageDeadlines()

    def test_different_methods(self):
        self.assertEqual(self.manager.check_date('february'), datetime.date(2022, 2, 1))
        self.assertEqual(self.manager.check_date('september'), datetime.date(2021, 9, 1))
        self.assertEqual(self.manager.check_date('3 december'), datetime.date(2021, 12, 3))
        self.assertEqual(self.manager.check_date('june'), datetime.date(2022, 6, 1))


if __name__ == '__main__':
    unittest.main()