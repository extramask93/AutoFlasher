from koradserial import KoradSerial


class PowerSupply():
    def __init__(self,com_port):
        self.com_port = com_port
        self.device = KoradSerial(com_port, True)
        self.device.output.off()
        channel = self.device.channels[0]
        channel.voltage = 12.0
        channel.current = 2.0

    def poweroff(self):
        self.device.output.off()

    def poweron(self):
        self.device.output.on()

    def __del__(self):
        self.device.close()
