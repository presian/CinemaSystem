class PrintData:

    def __init__(self):
        self.start = 1
        self.end = 11

    def print_table(self, seat):
        a = [["." for x in range(self.start, self.end)] for y in range(self.start, self.end)]
        table = ""
        for s in seat:
            a[s[0] - 1][s[1] - 1] = 'X'

        for elem in a:
            for row in elem:
                table += row
                table += " "
            table += '\n'
        print(table)

    def showMenu(self):
        print("""========================
            \n1.show_movies
            \n2.show_movie_projections
            \n3.make_reservation
            \n4.cancel_reservation
            \n5.Exit
            \n6.Help
            \n========================""")

    def show_movies(self, movies):
        for movie in movies:
            print("[{}] - {} ({})".format(movie["id"], movie["name"], movie["rating"]))

    def show_movie_projection(self, movies_projections):
        for movie in movies_projections:
            print("[{}] - {} {} ({}) - {} spots available".format(movie["projection_id"],
                                                                  movie["date"], movie["time"], movie["type"], movie["spots_available"]))

    def make_reservation(self):
        print("Thanks.The reservation was made")

    def cancel_reservation(self):
        print("A reservation was cancelled")


def main():
    pass

if __name__ == '__main__':
    main()
