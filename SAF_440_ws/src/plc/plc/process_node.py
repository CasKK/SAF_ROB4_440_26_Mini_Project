import rclpy
from rclpy.node import Node
import pandas as pd
import xml.etree.ElementTree as ET
from ament_index_python.packages import get_package_share_directory
from plc_interfaces.srv import ProcessXml          # custom service type
import os
from std_msgs.msg import String


class ProcessNode(Node):

    def __init__(self):
        super().__init__('process_node')

        # Create the service SERVER
        self.srv = self.create_service(ProcessXml, 'process_xml', self.handle_request)

        self.data_pub = self.create_publisher(String, 'data_broadcast', 10)

        package_path = get_package_share_directory('plc')
        csv_path = os.path.join(package_path, 'procssing_times_table.csv')
        self.df = pd.read_csv(csv_path, sep=';', index_col=0)

        self.get_logger().info('ProcessNode service ready.')

    def handle_request(self, request, response):
        """
        Called automatically by ROS2 when a client sends a request.
        Must fill in `response` fields and return it.
        """
        try:
            root = ET.fromstring(request.xml_data)
            carrier_id = root.find('CarrierID').text
            date_time  = root.find('DateTime').text
            station_id = root.find('StationID').text

            col = f'Station#0{station_id}' if int(station_id) < 10 else f'Station#{station_id}'
            value = self.df.loc[f'Carrier#{carrier_id}', col]

            self.get_logger().info(f'Processing time: {value}')
            
            msg = String()
            msg.data = '{},{},{}.{}'.format(carrier_id, date_time, station_id, value)

            self.data_pub.publish(msg)
            self.get_logger().info(
                f'Request — CarrierID: {carrier_id}, StationID: {station_id}, DateTime: {date_time}'
            )

            # Build XML response
            resp_root = ET.Element('root')
            ET.SubElement(resp_root, 'value').text = str(value)
            response.result = ET.tostring(resp_root, encoding='unicode')

        except Exception as e:
            self.get_logger().error(f'Service error: {e}')
            response.result = '<root><value>ERROR</value></root>'

        return response   # MUST return response


def main(args=None):
    rclpy.init(args=args)
    node = ProcessNode()
    rclpy.spin(node)


if __name__ == '__main__':
    main()