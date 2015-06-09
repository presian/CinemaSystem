from print_data import PrintData
from db_mapper import Db


class Client:

    def __init__(self):
        self.printer = PrintData()
        self.db = Db('cinemasystem.db')

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
        self.printer.show_movie_projection(result)

    def user_commands(self):
        exit = False
        list_commands = tuple()
        reservations = []
        while not exit:
            for command in ["Step 1 (User): Choose name>", "Step 1 (User): Choose number of tickets>", "Step 2 (Movie): Choose a movie>", "Step 3 (Projection): Choose a projection>"]:
                value = input(command)
                if command == "Step 1 (User): Choose name>":
                    username = value
                elif command == "Step 1 (User): Choose number of tickets>":
                    print("Current movies:")
                    tickets = int(value)
                    value = int(value)
                    self.show_movies()
                elif command == "Step 2 (Movie): Choose a movie>":
                    if " " in value:
                        array = value.split(" ")
                        digit = int(array[0])
                        movies = self.db.get_movie_rating(digit).fetchone()
                        data = array[1]
                        value = digit
                        print("Projecion for movie {}".format(movies[0]))
                        projection = self.db.getAllProjectionForMovie(digit, data)
                        self.printer.show_movie_projection(projection)
                    else:
                        value = int(value)
                        movies = self.db.get_movie_rating(value).fetchone()
                        print("Projecion for movie {}".format(movies[0]))
                        projection = self.db.getAllProjectionForMovie(value)
                        self.printer.show_movie_projection(projection)
                elif command == "Step 3 (Projection): Choose a projection>":
                    print("Available seats (marked with a dot):")
                    self.printer.print_table(self.db.seatsInRoom(int(value)))
                    value = int(value)
                    cnt = 1
                    free = False
                    while cnt <= tickets:
                        seat = self.choose_seat(cnt)
                        if self.db.chekIfSeatIsFree(value, seat[0],seat[1]) == True:
                            list_commands += (seat, )
                            print("""This is your reservation:
                                Movie: {} ({})
                                Seats: {}""".format(movies[0], movies[1], seat))
                            ready_data = (username, value, seat[0], seat[1])
                            confirm = input("Step 5 (Confirm - type 'finalize') > ")
                            if confirm == "finalize":
                                cnt += 1
                                self.db.make_reservation(ready_data)
                                self.printer.make_reservation()
                        else:
                            print('This seat is already taken!')
                list_commands += (value, )
            reservations.append(list_commands)
            enter_again = ''
            while enter_again != 'y':
                enter_again = input('Are you want to make another reservation!(y/n)')
                if enter_again == 'n':
                    enter_again = 'y'
                    exit = True

    def choose_seat(self, num):
        seats = tuple()
        print("Step 4 (Seats): Choose seat {}>".format(num))
        try:
            row = int(input('Please enter a row: '))
            col = int(input('Please enter a column: '))
            seats += (row, col)
            return seats
        except:
                return 'Your data is invalid! Please try again!'

    def start(self):
        command = "Enter 'Help' to see the commands:"
        print(command)
        while command != "Exit":
            command = input("Enter a command >")
            if command == "Help":
                self.printer.showMenu()
            elif command == "make_reservation":
                self.user_commands()
            elif command == "show_movies":
                self.show_movies()
            elif command == "show_movie_projections":
                self.show_movie_projections()
            elif command == "cancel_reservation":
                self.cancel_reservation()
        print("You exited the App!")

    def cancel_reservation(self):
        name = input('Enter a username: ')
        try:
            self.db.cancel_reservation(name)
            self.printer.cancel_reservation()
        except:
            print('Your data is invalid')


def main():
    client = Client()
    client.start()

if __name__ == '__main__':
    main()
