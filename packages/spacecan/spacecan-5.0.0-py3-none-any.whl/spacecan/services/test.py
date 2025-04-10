from .service_packet import ServicePacket


class TestServiceController:
    def __init__(self, parent):
        self.parent = parent

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        if case == (17, 2):
            self.received_connection_test_report(node_id)

        elif case == (17, 4):
            apid = int.from_bytes(data)
            self.received_application_connection_test_report(node_id, apid)

    def received_connection_test_report(self, node_id):
        # to be implemented by higher layer application
        pass

    def received_application_connection_test_report(self, node_id, apid):
        # to be implemented by higher layer application
        pass


class TestServiceResponder:
    def __init__(self, parent):
        self.parent = parent

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        if case == (17, 1):  # connection test
            # send success acceptance report
            self.parent.send(ServicePacket(1, 1, [service, subtype]))

            # reply
            self.parent.send(ServicePacket(17, 2))

            # send success completion report
            self.parent.send(ServicePacket(1, 7, [service, subtype]))

        elif case == (17, 3):  # onboard connection test
            apid = int.from_bytes(data)

            # send success acceptance report
            self.parent.send(ServicePacket(1, 1, [service, subtype]))

            # run the connection test
            result = self.received_application_connection_test(apid)

            if result is True:
                # reply
                self.parent.send(ServicePacket(17, 4, [apid]))

                # send success completion report
                self.parent.send(ServicePacket(1, 7, [service, subtype]))
            else:
                # send fail completion report
                self.parent.send(ServicePacket(1, 8, [service, subtype]))
        else:
            # send fail acceptance report
            self.parent.send(ServicePacket(1, 1, [service, subtype]))

    def received_application_connection_test(self, apid):
        # to be implemented by higher layer application
        return True
