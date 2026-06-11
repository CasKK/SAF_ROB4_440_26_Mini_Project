import rclpy
from rclpy.node import Node
import socket
from plc_interfaces.srv import ProcessXml          # service type


class TcpNode(Node):

    def __init__(self):
        super().__init__('tcp_node')

        # Create the service CLIENT
        self.cli = self.create_client(ProcessXml, 'process_xml')

        # Wait until the server is running
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for process_node service...')

        self.host = '0.0.0.0'
        self.port = 12343
        self.conn = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen()
        self.s.settimeout(0.05)

        self.get_logger().info(f'TCP server started on {self.host}:{self.port}')

    def call_process_service(self, xml_string):
        """Send request to process_node, block until response arrives."""
        req = ProcessXml.Request()
        req.xml_data = xml_string

        # call_async() returns a Future; spin_until_future_complete() blocks
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        return future.result().result   # the response.result string

    def plc_code(self):
        if self.conn is None:
            try:
                self.conn, addr = self.s.accept()
                self.conn.settimeout(0.01)
                self.get_logger().info(f'Connected by {addr}')
            except socket.timeout:
                return

        try:
            data = self.conn.recv(1024)
            if not data:
                return

            xml_string = data.decode('utf-8')
            self.get_logger().info(f'Received from PLC: {xml_string}')

            result_xml = self.call_process_service(xml_string)
            self.get_logger().info(f'Service response: {result_xml}')

            self.conn.sendall((result_xml + '\r\n').encode('utf-8'))

        except socket.timeout:
            return
        except Exception as e:
            self.get_logger().error(f'Error: {e}')
            self.conn = None


def main(args=None):
    rclpy.init(args=args)
    node = TcpNode()

    while rclpy.ok():
        node.plc_code()
        rclpy.spin_once(node, timeout_sec=0)


if __name__ == '__main__':
    main()