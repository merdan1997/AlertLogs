import mysql.connector
from multiprocessing import Pool
from datetime import datetime
print("OK")
def process_row():
    print("ok")
def process_row1(row):
    # db1 bağlantısı
    connection_db1 = mysql.connector.connect(
        host="192.168.0.254",
        user="kiber",
        password="kibeR@2023@Kiber",
        database="logsdb"
    )
    cursor_db1 = connection_db1.cursor()
    cursor_db1_1 = connection_db1.cursor()

    connection_db2 = mysql.connector.connect(
        host="192.168.9.25",
        user="alert",
        password="P@ssword1234560",
        database="Alertsystem"
    )
    cursor_db2 = connection_db2.cursor()


    role_name = row[1]
    description = row[2]
    severity_in = row[3]
    application_role = row[4]
    index_number = row[5]
    split_character = row[6]
    start_message = row[7]
    severity_out = row[8]
    own_text = row[9]

    delete_log = "SELECT id FROM table_kiber LIMIT 1"
    cursor_db1_1.execute(delete_log)
    logs_id = cursor_db1_1.fetchall()
    #print(type(logs_id), "id  =", logs_id)

    if start_message:
        #print("ookokk")
        cursor_db1.execute("SELECT id, hostname, severity, facility, application, message, timestamp FROM table_kiber WHERE severity = %s  AND application = %s AND  message LIKE %s AND message LIKE %s  LIMIT 500", (severity_in, application_role, (description+"%"), ("" + start_message + "%")))
        filtered_data = cursor_db1.fetchall()
        #print(" filterdata : ", filtered_data)

    else:
        cursor_db1.execute("SELECT id, hostname, severity, facility, application, message, timestamp FROM table_kiber WHERE severity = %s  AND application = %s AND  message = %s   LIMIT 500", (severity_in, application_role, description))
        filtered_data = cursor_db1.fetchall()
        #print(" filterdata : ", filtered_data)

    # Verileri db2.filterlog tablosuna yazma
    for filtered_row in filtered_data:
        id, hostname, severity, facility, application, message, timestamp = filtered_row
        my_message = " "
        if index_number:
            my_message = message.split(split_character)
            my_message = my_message[int(index_number)]
            #print("test ip  ", my_message)
        else:
            my_message = message

        #print(my_message)
        text_message = my_message + "   " + own_text
        #print("my text  =", text_message)
        insert_query = "INSERT INTO alertlog_filterlog (hostname, severity, facility, application, role, timestamp, message, text_message) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        values = (hostname, severity, facility, application, role_name, timestamp, message, text_message)
        cursor_db2.execute(insert_query, values)

        #print("yazgy gosuldy")
        connection_db2.commit()
    #print("delete gecdi")

    delete_query = "DELETE FROM table_kiber WHERE id  = %s"
    for log in logs_id:
        cursor_db1.execute(delete_query, log)
        #print("delete edildi")
        connection_db1.commit()

    # Bağlantıları kapatma
    cursor_db1.close()
    connection_db1.close()
    cursor_db2.close()
    connection_db2.close()

if __name__ == '__main__':
    # db2 bağlantısı
    connection_db2 = mysql.connector.connect(
        host="192.168.9.25",
        user="alert",
        password="P@ssword1234560",
        database="Alertsystem"
    )
    cursor_db2 = connection_db2.cursor()
    cursor_db2.execute("SELECT * FROM alertlog_roles")
    db2_data = cursor_db2.fetchall()

    # Create a multiprocessing Pool
    pool = Pool()

    # Apply the process_row function to each row in db2_data
    pool.map(process_row, db2_data)

    # Close the pool to prevent any more tasks from being submitted
    pool.close()

    # Wait for all processes to complete
    pool.join()

    # Bağlantıyı kapatma
    cursor_db2.close()
    connection_db2.close()

