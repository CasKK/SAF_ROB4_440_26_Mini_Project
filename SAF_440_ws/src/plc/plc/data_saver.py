import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv

class Save(Node):

    def __init__(self):
        super().__init__('tcp_node')

        self.message = self.create_subscription(String, 'data_broadcast', self.handle_data_callback, 10)


    def handle_data_callback(self, msg):
        xml_string = msg.data
        self.get_logger().info(f'Received from PLC: {xml_string}')

        data_seperated = xml_string.split(',')

        with open('data_from_plc.csv', 'a', newline='') as csvfile:
            fieldnames = ['CarrierID', 'DateTime', 'StationID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'CarrierID': data_seperated[0], 'DateTime': data_seperated[1], 'StationID': data_seperated[2]})
            
def main(args=None):
    rclpy.init(args=args)

    node = Save()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()