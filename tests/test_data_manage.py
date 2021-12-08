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
    
    # testing check_deadline method inside of manager (By tomorrow, next week, next month)
    def test_check_deadline(self):
        # simple one
        self.assertEqual(self.manager.check_date('By tomorrow'), datetime.date(2021,12,2))
        self.assertEqual(self.manager.check_date('By next week'), datetime.date(2021,12,8))
        # by next month adds +30
        self.assertEqual(self.manager.check_date('By next month'), datetime.date(2021,12,31))
        # diff input
        self.assertEqual(self.manager.check_date(' something By tomorrow'), datetime.date(2021,12,2))
        self.assertEqual(self.manager.check_date(' something By next week'), datetime.date(2021,12,8))
        self.assertEqual(self.manager.check_date(' something By next month'), datetime.date(2021,12,31))
        # should be none here
        self.assertEqual(self.manager.check_date('By tomorrow yep yep'), None)
        self.assertEqual(self.manager.check_date('By next week yep yep'), None)
        self.assertEqual(self.manager.check_date('By next month     yes please'), None)
        # by starts with lowercase letter
        self.assertEqual(self.manager.check_date('by tomorrow '), None)
        self.assertEqual(self.manager.check_date('by tomorrow'), None)
        # strange input

    # testing cur_month_deadline method inside of manage (By <date>)
    def test_current_month_deadlines(self):
        # correct data
        self.assertEqual(self.manager.check_date('By 3'), datetime.date(2021, 12, 3))
        self.assertEqual(self.manager.check_date('By 30'), datetime.date(2021, 12, 30))
        self.assertEqual(self.manager.check_date('By 25'), datetime.date(2021, 12, 25))
        # with spaces in the end should be ok
        self.assertEqual(self.manager.check_date('By 25 '), datetime.date(2021, 12, 25))
        self.assertEqual(self.manager.check_date('By 30 '), datetime.date(2021, 12, 30))
        # a little bit missed
        self.assertEqual(self.manager.check_date('By 35'), None)
        self.assertEqual(self.manager.check_date('Task and task By 35'), None)
        # incorrect format
        self.assertEqual(self.manager.check_date('By 3 and'), None)
        self.assertEqual(self.manager.check_date(' By 3 and and adn l'), None)
        self.assertEqual(self.manager.check_date('By     3      and'), None)
        # by starts with lowercase letter
        self.assertEqual(self.manager.check_date('by 30 '), None)

    def test_by_month(self):
        # normal input
        self.assertEqual(self.manager.check_date('By february'), datetime.date(2022, 2, 1))
        self.assertEqual(self.manager.check_date('By january'), datetime.date(2022, 1, 1))
        self.assertEqual(self.manager.check_date('By june'), datetime.date(2022, 6, 1))
        # uppercase
        self.assertEqual(self.manager.check_date('By February'), datetime.date(2022, 2, 1))
        self.assertEqual(self.manager.check_date('By FebRuarY'), datetime.date(2022, 2, 1))
        self.assertEqual(self.manager.check_date('By JUNE'), datetime.date(2022, 6, 1))
        # incorrect format
        self.assertEqual(self.manager.check_date('By june and 3'), None)
        self.assertEqual(self.manager.check_date('By june 21'), None)
        self.assertEqual(self.manager.check_date('By june and february'), None)
        self.assertEqual(self.manager.check_date('by june'), None)

    def test_by_month_and_day(self):
        # normal input
        self.assertEqual(self.manager.check_date('By 3 march'), datetime.date(2022,3,3))
        self.assertEqual(self.manager.check_date('By 30 march'), datetime.date(2022,3,30))
        self.assertEqual(self.manager.check_date('By 30 june'), datetime.date(2022,6,30))
        self.assertEqual(self.manager.check_date('By 14 september'), datetime.date(2022,9,14))
        # big numbers
        self.assertEqual(self.manager.check_date('By 36 march'), None)
        self.assertEqual(self.manager.check_date('By 70 march'), None)
        self.assertEqual(self.manager.check_date('By 90 march'), None)
        # wrong fromat
        self.assertEqual(self.manager.check_date('By march 3'), None)
        self.assertEqual(self.manager.check_date('by 3 march'), None)
        self.assertEqual(self.manager.check_date('        By 33 march'), None)
        # more than needed
        self.assertEqual(self.manager.check_date('By 3 march and'), datetime.date(2022,3,3))
        self.assertEqual(self.manager.check_date('Task Task Task By 3 march and march'), datetime.date(2022,3,3))
        self.assertEqual(self.manager.check_date('By 10 July and'), datetime.date(2022,7,10))
        # Uppercase input
        self.assertEqual(self.manager.check_date('By 3 March'), datetime.date(2022,3,3)) 
        self.assertEqual(self.manager.check_date('By 3 January'), datetime.date(2022,1,3))
        self.assertEqual(self.manager.check_date('By 10 AugusT'), datetime.date(2022,8,10))

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
        self.assertEqual(self.manager.check_date('By february'), datetime.date(2022, 2, 1))
        self.assertEqual(self.manager.check_date('By september'), datetime.date(2021, 9, 1))
        self.assertEqual(self.manager.check_date('By 3 december'), datetime.date(2021, 12, 3))
        self.assertEqual(self.manager.check_date('By june'), datetime.date(2022, 6, 1))


if __name__ == '__main__':
    unittest.main()