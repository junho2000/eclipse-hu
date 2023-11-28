import tkinter as tk
import pymysql
import time

class HUDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Head-Up Display")
        self.geometry("1080x640")

        # Initialize database connection
        self.connection = pymysql.connect(
            host="db-hackathon.ciskedsbhsct.us-east-2.rds.amazonaws.com",
            port=3306,
            user="root",
            passwd="12341234",
            db="piracer"
        )

        self.is_mysql_connected()

        # Create labels
        self.speed_label = tk.Label(self, text="Speed: 0 km/h", font=("Helvetica", 40))
        self.speed_label.pack()

        self.battery_label = tk.Label(self, text="Battery: 0 %", font=("Helvetica", 40))
        self.battery_label.pack()

        self.temp_label = tk.Label(self, text="Motor Temp: 0 °C", font=("Helvetica", 40))
        self.temp_label.pack()

        self.air_label = tk.Label(self, text="Air Conditioner: Off", font=("Helvetica", 40))
        self.air_label.pack()

        self.window_label = tk.Label(self, text="Window Open: 0 %", font=("Helvetica", 40))
        self.window_label.pack()

        # Start the periodic update
        self.update_data()

    def is_mysql_connected(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("Success to connect to MySQL")
        except pymysql.MySQLError as e:
            print(f"Failed to connect to MySQL: {e}")

    def update_data(self):
        connection = pymysql.connect(
            host="db-hackathon.ciskedsbhsct.us-east-2.rds.amazonaws.com",
            port=3306,
            user="root",
            passwd="12341234",
            db="piracer"
        )
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT speed, battery, motor_temp, is_aircondition_active, window_position 
                    FROM piracer_status 
                    ORDER BY data_id DESC 
                    LIMIT 1
                """)
                result = cursor.fetchone()

            if result:
                current_speed = float(result[0])
                current_battery = float(result[1])
                current_temp = int(result[2])
                current_air = "On" if result[3] == 1 else "Off"
                current_window = int(result[4])
                
                self.speed_label.config(text=f"Speed: {current_speed:.2f} km/h")
                self.battery_label.config(text=f"Battery: {current_battery:.2f}%")
                self.temp_label.config(text=f"Motor Temp: {current_temp} °C")
                self.air_label.config(text=f"Air Conditioner: {current_air}")
                self.window_label.config(text=f"Window: {current_window} %")
                
                print("speed :", current_speed)
                print("battery :", current_battery)
                print("temp :", current_temp)
                print("air :", current_air)
                print("window :", current_window)

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")

        self.after(10, self.update_data)

# Create and run the application
root = HUDApp()
root.mainloop()
