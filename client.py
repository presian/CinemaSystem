from print_data import PrintData
from db_mapper import Db


class Client:

    def __init__(self):
        self.printer = PrintData()
        self.db = Db('cinemasystem')

    def showMenu(self):
        print("""========================
            \n1.show_movies
            \n2.show_movie_projections
            \n3.make_reservation
            \n4.cancel_reservation
            \n5.Exit
            \n6.Help
            \n========================""")

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

        # list_commands = tuple()
        # for command in ["Step 1 (User): Choose name>", "Step 1 (User): Choose number of tickets>", "Step 2 (Movie): Choose a movie>", "Step 3 (Projection): Choose a projection> 5", "Step 4 (Seats): Choose seat 1>","Step 5 (Confirm - type 'finalize') >"]:
        #     value = input(command)
        #     if command == "Step 1 (User): Choose number of tickets>":
        #         print("Current movies:")
        #         self.show_movies()
        #     elif command == "Step 2 (Movie): Choose a movie>":
        #         self.show_movie_projection()
        #         movies = self.data.getAllMoviesOrderedByRating()
        #         for movie in movies:
        #             movie_name = movie["{}".format(value)]
        #         print("Projections for movie {}:".format(movie_name))

        #     list_commands += (value, )
        # return list_commands

    def make_reservation(self):
        list_commands = tuple()
        for command in ["Step 1 (User): Choose name>", "Step 1 (User): Choose number of tickets>", "Step 2 (Movie): Choose a movie>", "Step 3 (Projection): Choose a projection> 5", "Step 4 (Seats): Choose seat 1>", "Step 5 (Confirm - type 'finalize') >"]:
            if command == "Step 1 (User): Choose number of tickets>":
                print("Current movies:")
                self.printer.show_movies()
            elif command == "Step 2 (Movie): Choose a movie>":
                self.printer.show_movie_projection()
                movies = self.data.getAllMoviesOrderedByRating()
                self.printer.show_movies(movies)
            value = input(command)

            list_commands += (value, )
        exit = False
        username = input('Enter username: ')
        reservations = []
        while not exit:
            try:
                projection_id = int(input('Enter projection_id: '))

                # todo make validation for id -> raise exception
                row = int(input('Please enter a row: '))
                # todo make validation for row -> raise exception
                col = int(input('Please enter a column: '))
                # todo make validation for column -> raise exception

                reservations.append((username, projection_id, row, col))
            except:
                print('Ypur data is invalid! Please try again!')
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

if __name__ == '__main__':
    client = Client()
    exit = False
    while not exit:
        client.showMenu()
        option = client.getUserOption()
        client.commandExecutor(option)
