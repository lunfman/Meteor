from sqlalchemy.orm import query
from werkzeug.wrappers import response
from todoapp import category, create_app, db
from todoapp.models import Category, Tasks
import unittest
from  config import TestConfig

def add_data():
    category = Category(name = 'test')
    db.session.add(category)
    tasks_category = Category(name = 'tasks')
    db.session.add(tasks_category)
    task = Tasks(task='first', category=category)
    db.session.add(task)
    db.session.commit()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.from_object(TestConfig)
        self.client = app.test_client()
        db.init_app(app)
        
        with app.app_context():
            db.session.commit()
            db.drop_all()
            db.create_all()
            add_data()

    # Dashboard testing section
    def test_dashboard(self):
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'test' in response.data)
            self.assertTrue(b'Good Job' in response.data)
            self.assertTrue(b'0 optional' in response.data)
            self.assertTrue(b'0 / 1' in response.data)

    # Category testing section
    def test_category(self):
        with self.client as client:
            response = client.get('/category/test')
            self.assertTrue(b'test' in response.data)
            self.assertTrue(b'first' in response.data)

        with self.client as client:
            response = client.get('/category/test 1')
            self.assertTrue(b'test 1' not in response.data)

    # test category delete, complete, undo, delete completed
    def test_category_completed(self):
        with self.client as clinet:
            response = clinet.get('/completed', query_string=dict(id='1', category='test'),
                follow_redirects=True)
            # completed button not in html 1 but
            self.assertTrue(b'fas fa-check' not in response.data)
            self.assertTrue(b'fas fa-undo' in response.data)
    
    def test_category_undo(self):
        with self.client as clinet:
            response = clinet.get('/undo', query_string=dict(id='1', category='test'))
            self.assertTrue(b'fas fa-check' in response.data)
            self.assertTrue(b'fas fa-undo' not in response.data)
    
    def test_category_undo(self):
        with self.client as clinet:
            response = clinet.get('/delete', query_string=dict(id='1', category='test'))
            self.assertTrue(b'first' not in response.data)
            self.assertTrue(b'fas fa-check' not in response.data)
    
        # task = Tasks(task='first', category=category)
        # db.session.add(task)
        # db.session.commit()

    # Terminal testing section
    
    def terminal_req(self, input):
        with self.client as client:
            response = client.post('/terminal',
                data=dict(add=input),
                follow_redirects=True)
        return response


    def test_terminal_main_command(self):
        # test Main command
        response = self.terminal_req('Main')
        self.assertTrue(b'test' in response.data)
        self.assertTrue(b'0 / 1' in response.data)

        response = self.terminal_req('Main and one more')
        self.assertTrue(b'test' in response.data)
        self.assertTrue(b'0 / 1' in response.data)    


    def test_terminal_help_command(self):
        response = self.terminal_req('Help')
        self.assertTrue(b'Commands' in response.data)


    def test_terminal_rename_command(self):
        response = self.terminal_req('Rename test test1')
        self.assertTrue(b'test' in response.data)
        self.assertTrue(b'0 / 1' in response.data)
        # if blank to ..
        response = self.terminal_req('Rename test To    ')
        self.assertTrue(b'test' in response.data)
        self.assertTrue(b'0 / 1' in response.data)
        # test Rename 
        response = self.terminal_req('Rename test To test1')
        self.assertTrue(b'test1' in response.data)
        self.assertTrue(b'0 / 1' in response.data)


    def test_terminal_task_add(self):
        # todo rewrite
        response = self.terminal_req('new task')
        # maybe open task cat and check? cause test also have 0/1?
        self.assertTrue(b'tasks' in response.data)
        self.assertTrue(b'0 / 1' in response.data)

        # add to unique category ? it should redirect back to category!!!!
        with self.client as client:
            response = client.post('/terminal',
                data=dict(add='task'),
                query_string=dict(category='test'),
                follow_redirects=True)
            self.assertTrue(b'task' in response.data)
            self.assertTrue(b'first' in response.data)

            response = client.get('/')
            self.assertTrue(b'0 / 2' in response.data)
        
        with self.client as client:
            response = client.post('/terminal',
                data=dict(add='Add task11, task22, tasko tasko1'),
                query_string=dict(category='test'),
                follow_redirects=True)
            self.assertTrue(b'task11' in response.data)
            self.assertTrue(b'task22', response.data)
            self.assertTrue(b'tasko tasko1', response.data)
            self.assertTrue(b'Add task11' not in response.data)


        with self.client as client:
            response = client.post('/terminal',
                data=dict(add='Add task11, task22, task2, task3 By tomorrow'),
                query_string=dict(category='test'),
                follow_redirects=True)
            print(response.data.count(b'tomorrow'))
            self.assertTrue(4 <= response.data.count(b'tomorrow'))

    def test_terminal_by_command(self):
        # with redirect to main
        response = self.terminal_req('task By tomorrow')
        self.assertTrue(b'1 for tomorrow' in response.data)


    def test_terminal_create_command(self):
        # create empty category
        response = self.terminal_req('Create new category me')
        self.assertTrue(b'new category me' in response.data)
        self.assertTrue(b'0 / 0')

        # create category which already exists. error should not accure!
        response = self.terminal_req('Create new category me')
        self.assertTrue(b'new category me' in response.data)
        self.assertTrue(b'0 / 0')

        # Create new category and add many
        response = self.terminal_req('Create new category me3 Add test1, test2, test3,test4,test5')
        self.assertTrue(b'test1' in response.data)
        self.assertTrue(b'test2' in response.data)
        self.assertTrue(b'test3' in response.data)
        self.assertTrue(b'test4' in response.data)
        self.assertTrue(b'test5' in response.data)
        # Create new category and add data  by date

        response = self.terminal_req('Create new category me4 Add test1, test2, test3 By tomorrow')
        self.assertTrue(b'test1' in response.data)
        self.assertTrue(b'test2' in response.data)
        self.assertTrue(b'Add test1' not in response.data)
        self.assertTrue(b'new category me4' in response.data)
        self.assertTrue(b'test3 By tomorrow' not in response.data)

        # amount of task should be 3
        self.assertTrue(3 == response.data.count(b'tomorrow'))


    def test_terminal_hide_reveal_commands(self):
        response = self.terminal_req('Hide test')
        self.assertTrue(b'test' not in response.data)
        
        response = self.terminal_req('Reveal test')
        self.assertTrue(b'test' in response.data)


    def test_terminal_show_command(self):
        
        # Show deadlines
        with self.client as client:
            # add task with deadline by tomorrow for the test
            client.post('/terminal',
                data=dict(add='new me name By tomorrow'),
                query_string=dict(category='test'))

            response = client.post('/terminal',
                data=dict(add='Show deadlines'),
                query_string=dict(category='test'),
                follow_redirects=True)

            self.assertTrue(b'new me name' in response.data)
            self.assertTrue(b'first' not in response.data)
            self.assertTrue(b'task' in response.data)         

        # Show optional
        with self.client as client:
            response = client.post('/terminal',
                data=dict(add='Show optional'),
                query_string=dict(category='test'),
                follow_redirects=True)

            self.assertTrue(b'new me name' not in response.data)
            self.assertTrue(b'first' in response.data)

        # Show list
        with self.client as client:
            response = client.post('/terminal',
                data=dict(add='Show list'),
                query_string=dict(category='test'),
                follow_redirects=True)

            self.assertTrue(b'new me name' in response.data)
            self.assertTrue(b'task' in response.data)
            self.assertTrue(b'tomorrow')

    def test_terminal_open_command(self):
        # if category do not exists redirect to main page
        # if exists go to the page
        response = self.terminal_req('Open tasks 25')
        self.assertTrue(b'tasks 25' not in response.data)

        response = self.terminal_req('Open tasks task1 task2')
        self.assertTrue(b'tasks task1 task2'not in response.data)

        response = self.terminal_req('Open test')
        self.assertTrue(b'first' in response.data)


    def test_delete_command(self):
        response = self.terminal_req('Create new one')
        self.assertTrue(b'new one' in response.data)

        response = self.terminal_req('Delete test')
        self.assertTrue(b'test' in response.data)
        self.assertTrue(b'new one' in response.data)
        self.assertTrue(b'0 / 0' in response.data)

        response = self.terminal_req(b'Delete new one')
        self.assertTrue(b'new one' not in response.data)
        self.assertTrue(b'test' in response.data)

    def test_migrate_command(self):
        response = self.terminal_req('Delete test')
        self.assertTrue(b'test' in response.data)

        response = self.terminal_req('Migrate test To tasks')
        response = self.terminal_req('Delete test')

        self.assertTrue(b'test' not in response.data)





if __name__ == '__main__':
    unittest.main()