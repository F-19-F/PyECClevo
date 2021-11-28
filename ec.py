import ctypes
lib = ctypes.WinDLL(".\inpoutx64.dll")
inb = lib.DlPortReadPortUchar
outb = lib.DlPortWritePortUchar
EC_IBF_BIT = 0b10
EC_OBF_BIT = 0b01
EC_CMD_STATUS_REGISTER_PORT = 0x66
EC_DATA_REGISTER_PORT = 0x62


class EC:
    class Register():
        @staticmethod
        def WaitInputNFull():
            while EC.Register.GetStatus() & EC_IBF_BIT != 0:
                pass

        @staticmethod
        def WaitOutputFull():
            i = 0
            while EC.Register.GetStatus() & EC_OBF_BIT == 0:
                if i == 0xFFFF:
                    break
                i += 1

        @staticmethod
        def GetStatus():
            return inb(EC_CMD_STATUS_REGISTER_PORT)

        @staticmethod
        def SetCmd(cmd: int):
            EC.Register.WaitInputNFull()
            outb(EC_CMD_STATUS_REGISTER_PORT, cmd)

        @staticmethod
        def SetData(data: int):
            EC.Register.WaitInputNFull()
            outb(EC_DATA_REGISTER_PORT, data)

        @staticmethod
        def GetData():
            EC.Register.WaitOutputFull()
            return inb(EC_DATA_REGISTER_PORT)

    @staticmethod
    def Read(address: int):
        EC.Register.SetCmd(0x80)
        EC.Register.SetData(address)
        return EC.Register.GetData()