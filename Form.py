##KWAZI ZUNGU
##GUI form must save data inserted by user to SQL database
##You must Enter your own MySQL server user details inplace of mine! 

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import mysql.connector
from mysql.connector import Error
import pw  # password file 'pw.py' 

# Instance details
host = '127.0.0.1'
user = 'root'
pw = pw.SQLpw  # MySQL terminal password
db = 'kwazi_prac'  # database name


# To connect to database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name,
                                             user=user_name,
                                             passwd=user_password,
                                             database=db_name)
        print('Database Connection Successfully!')
    except Error as err:
        print(f'Error: {err} OR email already in database !')
    return connection


# For executing mysql queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query Successful!')
    except Error as err:
        print(f'Error:{err}')


# Creating Form
class gridzo(GridLayout):

    def __init__(self, **kwargs):
        super(gridzo, self).__init__(**kwargs)  
        self.cols = 1  # for main grid

        self.inside = GridLayout()  # grid inside grid
        self.inside.cols = 2
        self.add_widget(self.inside)

        # name row
        self.inside.add_widget(Label(text='Name:'))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        # surname row
        self.inside.add_widget(Label(text='Surname:'))
        self.surname = TextInput(multiline=False)
        self.inside.add_widget(self.surname)

        # email row
        self.inside.add_widget(Label(text='Email'))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        # button
        self.submit = Button(text='SUBMIT', size_hint=(1, 0.2), bold=True)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)  # add button in main grid

    # When button is pressed
    def pressed(self, instance):
        name = self.name.text
        surname = self.surname.text
        email = self.email.text

        # Send info to database
        connection = create_db_connection(host, user, pw, db)
        query = f"INSERT INTO form VALUES('{email}','{name}','{surname}')"
        execute_query(connection, query)

        # After data has been sent / when 'SUBMIT' button is pressed
        self.name.text = ''
        self.surname.text = ''
        self.email.text = ''


class Form(App):
    def build(self):
        return gridzo()


if __name__ == '__main__':
    Form().run()
