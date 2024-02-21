class SeatLayout:
    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns
    
    def gen_layout(self):
        FloorLayout = []
        Total_Seats = 0
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(0)
                Total_Seats += 1
            FloorLayout.append(row)
        print("Total Seats in the Movie Hall is ", Total_Seats)
        return FloorLayout
    
    def seat_availability(self,SeatMap = []):
        TotalSeats = 0
        for i in SeatMap:
            #print(i)
            row_count = i.count(0)
            TotalSeats += row_count
        return TotalSeats
    
    def display_Layout(self, SeatMap = []):
        for i in SeatMap:
            print(i)
        return
    
class Booking(SeatLayout):    
    def book_seat(self,SeatMap = [],row = 0, column = 0):
        if SeatMap[row][column] == 0:
            SeatMap[row][column] = 1
            return True
        else:
            return False

    def cancel_seat(self,SeatMap = [],row = 0, column = 0):
        if SeatMap[row][column] == 1:
            SeatMap[row][column] = 0
            return True
        else:
            return False
objSL = SeatLayout(10,10)

SeatMap = objSL.gen_layout()
total_count = objSL.seat_availability(SeatMap)            
print("Total Seats Available: ",total_count)

while True:
    user_input = input("Do you want to Proceed with Booking (yes/no): ")
    if user_input.lower() == "no":
        break
    if user_input.lower() == "yes":
        user_row = int(input("Please enter row number: "))
        user_column = int(input("Please enter column number: "))
    
        row_capacity = range(1,11)
        column_capacity = range(1,11)
    
        if user_row in row_capacity and user_column in column_capacity:
            objBooking = Booking(10,10)
            booking_status = objBooking.book_seat(SeatMap,int(user_row)-1,int(user_column)-1)
            if booking_status:
                print("Seat Booked Successfully")
            else:
                print("Seat is already booked")
            objBooking.display_Layout(SeatMap)
            total_count = objSL.seat_availability(SeatMap)            
            print("Total Seats Available: ",total_count)
