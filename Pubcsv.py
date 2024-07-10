import zmq
import time
import pandas as pd

csv_file_path = 'selected_rows.csv'
df = pd.read_csv(csv_file_path)

# Initialize ZeroMQ context and socket for publishing
context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://*:1132')

# Group the DataFrame rows based on the TIME column
groups = df.groupby('TIME')

# Infinite loop to continuously publish the data
while True:
    # Iterate over the groups and publish the data
    for time_value, group_df in groups:
        group_csv_data = group_df.to_csv(index=False)
        message = f'{time_value} {group_csv_data}'
        pub_socket.send_string(message)
        print(message)

        # Add some delay
        time.sleep(1)

    # Reset the DataFrame iterator when reaching the end
    groups = df.groupby('TIME')

# Close the ZeroMQ socket and context
pub_socket.close()
context.term()
