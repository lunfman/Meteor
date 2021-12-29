import unittest
import datetime
from freezegun import freeze_time
from todoapp.date_manage import Deadline, ManageDeadlines


class TestDeadlinesMethods(unittest.TestCase):
    
    @freeze_time('2021-12-01')
    # testing check_deadline method(tomorrow, next week, next month)
    def test_check_deadline(self):
        # simple one
        deadline = Deadline('tomorrow')
        self.assertEqual(deadline.check_deadline(), datetime.date(2021,12,2))
        deadline = Deadline('next week')
        self.assertEqual(deadline.check_deadline(), datetime.date(2021,12,8))
        # by next month adds +30
        deadline = Deadline('next month')
        self.assertEqual(deadline.check_deadline(), datetime.date(2021,12,31))

    # testing cur_month_deadline method inside of manage (By <date>)
    @freeze_time('2021-12-01')
    def test_current_month_deadlines(self):
        # correct data
        deadline = Deadline('3')
        self.assertEqual(deadline.cur_month_deadline(), datetime.date(2021, 12, 3))
        deadline = Deadline('30')
        self.assertEqual(deadline.cur_month_deadline(), datetime.date(2021, 12, 30))
        deadline = Deadline('25')
        self.assertEqual(deadline.cur_month_deadline(), datetime.date(2021, 12, 25))
        # a little bit missed
        # deadline = Deadline('35')
        # self.assertEqual(manager.check_date(), None)
    
    @freeze_time('2021-12-01')
    def test_by_month(self):
        # normal input
        deadline = Deadline('february')
        self.assertEqual(deadline.by_month(), datetime.date(2022, 2, 1))
        deadline = Deadline('january')
        self.assertEqual(deadline.by_month(), datetime.date(2022, 1, 1))
        deadline = Deadline('june')
        self.assertEqual(deadline.by_month(), datetime.date(2022, 6, 1))
        # uppercase
        deadline = Deadline('February')
        self.assertEqual(deadline.by_month(), datetime.date(2022, 2, 1))
        deadline = Deadline('FebRuarY')
        self.assertEqual(deadline.by_month(), datetime.date(2022, 2, 1))
        deadline = Deadline('JUNE')
        self.assertEqual(deadline.by_month(), datetime.date(2022, 6, 1))
        # incorrect format
        deadline = Deadline('june and 3')
        self.assertEqual(deadline.by_month(), None)
        deadline = Deadline('june 21')
        self.assertEqual(deadline.by_month(), None)
        deadline = Deadline('june and february')
        self.assertEqual(deadline.by_month(), None)
    
    @freeze_time('2021-12-01')
    def test_by_month_and_day(self):
        # normal input
        deadline = Deadline('3 march')
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,3,3))
        deadline = Deadline('30 march')
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,3,30))
        deadline = Deadline('30 june')
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,6,30))
        deadline = Deadline('14 september')
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,9,14))
        deadline = Deadline('70 march')
        self.assertEqual(deadline.by_month_and_day(), None)
        deadline = Deadline('90 march')
        self.assertEqual(deadline.by_month_and_day(), None)       
        deadline = Deadline('3 March') 
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,3,3)) 
        deadline = Deadline('3 January')
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,1,3))
        deadline = Deadline('3 AugusT')
        self.assertEqual(deadline.by_month_and_day(), datetime.date(2022,8,3))
    
    @freeze_time('2021-12-01')
    def test_in_command(self):
        deadline = Deadline('5')
        self.assertEqual(deadline.in_command(), datetime.date(2021,12,6))
        deadline = Deadline('32')
        self.assertEqual(deadline.in_command(), datetime.date(2022,1,2))
        deadline = Deadline('90')
        self.assertEqual(deadline.in_command(), datetime.date(2022,3,1))
        deadline = Deadline(90)
        self.assertEqual(deadline.in_command(), datetime.date(2022,3,1))
        # wrong data
        deadline = Deadline(95)
        self.assertEqual(deadline.in_command(), None)
        deadline = Deadline('100')
        self.assertEqual(deadline.in_command(), None)

class TestDeadlinesMethods_version_2(unittest.TestCase):
    # a few test with this date
    @freeze_time('2021-7-01')
    def test_different_methods(self):
        manager = ManageDeadlines('february')
        self.assertEqual(manager.check_date(), datetime.date(2022, 2, 1))
        manager = ManageDeadlines('september')
        self.assertEqual(manager.check_date(), datetime.date(2021, 9, 1))
        manager = ManageDeadlines('3 december')
        self.assertEqual(manager.check_date(), datetime.date(2021, 12, 3))
        manager = ManageDeadlines('june')
        self.assertEqual(manager.check_date(), datetime.date(2022, 6, 1))


if __name__ == '__main__':
    unittest.main()