from print_data import PrintData
from db_mapper import Db


class Client:

    def __init__(self):
        self.printer = PrintData()
        self.db = Db('cinemasystem.db')

    def getUserOption(self):
        return int(input('Please choise a option(digit): '))

    def commandExecutor(self, option):
        if option == 1:
            self.show_movies()
        elif option == 2:
            self.show_movie_projections()
        elif option == 3:
            self.make_reservation()
        elif option == 4:
            self.cancel_reservation()
        elif option == 5:
            return
        elif option == 6:
            self.printer.print_help()

    def show_movies(self):
        result = self.db.getAllMoviesOrderedByRating()
        self.printer.show_movies(result)

    def show_movie_projections(self):
        try:
            movie_id = int(input('Enter a movie_id: '))
            date = input('Enter a date (optional-> if you want live it blank): ')
        except:
            print('Your data is invalid!')
        result = self.db.getAllProjectionForMovie(movie_id, date if not date == '' else None)
        self.printer.show_movie_projections(result)

    def user_commands(self):
        list_commands = tuple()
        for command in ["Step 1 (User): Choose name>", "Step 1 (User): Choose number of tickets>", "Step 2 (Movie): Choose a movie>", "Step 3 (Projection): Choose a projection>"]:
            value = input(command)
            if command == "Step 1 (User): Choose number of tickets>":
                print("Current movies:")
                self.show_movies()
            elif command == "Step 2 (Movie): Choose a movie>":
                print("Projecion for movie .....")
                array = value.split(" ")
                digit = int(array[0])
                data = array[1]
                projection = self.db.getAllProjectionForMovie(digit, data)
                self.printer.show_movie_projection(projection)
            elif command == "Step 3 (Projection): Choose a projection>":
                print("Available seats (marked with a dot):")
                self.printer.print_table(self.db.seatsInRoom(int(value)))
                self.choose_seat()
            list_commands += (value, )
        return list_commands

    def choose_seat(self):
        seats = tuple()
        print("Step 4 (Seats): Choose seat 1>")
        try:
            row = int(input('Please enter a row: '))
            col = int(input('Please enter a column: '))
            seats += (row, col)
            return seats
        except:
                return 'Your data is invalid! Please try again!'

"""    def make_reservation(self):

        exit = False
        commands = self.user_commands()
        reservations = []
        while not exit:
            try:

            enter_again = ''
            while enter_again != 'n' or enter_again != 'y':
                enter_again = input('Are you want to make another reservation!(y/n)')
            if enter_again == 'n':
                exit = True
        if len(reservations) > 0:
            self.db.make_reservation()
            # print success message or error (try/catch)
        else:
            self.showMenu()

    def cancel_reservation(self):
        name = input('Enter a username: ')
        try:
            self.db.cancel_reservation(name)
        except:
            print('Your data is invalid')
"""

def main():
    client = Client()
    #exit = False
    #while not exit:
    #    client.showMenu()
    #    option = client.getUserOption()
    #    client.commandExecutor(option)
    #print(client.user_commands())
    print(client.db.chekIfSeatIsFree(1, 2, 1))
if __name__ == '__main__':
    main()
