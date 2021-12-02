import platform
EC_IBF_BIT = 0b10
EC_OBF_BIT = 0b01
EC_CMD_STATUS_REGISTER_PORT = 0x66
EC_DATA_REGISTER_PORT = 0x62
if (platform.system() =="Windows"):
    import ctypes
    lib = ctypes.WinDLL(".\inpoutx64.dll")
    inb = lib.DlPortReadPortUchar
    outb = lib.DlPortWritePortUchar
elif (platform.system() =="Linux"):
    # pip3 install portio
    import portio
    def linux_inb(port):
        return portio.inb(port)
    inb = linux_inb
    def linux_outb(port,data):
        return portio.outb(data,port)
    outb = linux_outb
    res_sc = portio.ioperm(EC_CMD_STATUS_REGISTER_PORT,1,1)
    res_data = portio.ioperm(EC_DATA_REGISTER_PORT,1,1)
    if (res_sc != 0 or res_data !=0):
        raise Exception("ioperm error")


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
    
    @staticmethod
    def Write(address:int,data:int):
        EC.Register.SetCmd(0x81)
        EC.Register.SetData(address)
        EC.Register.SetData(data)
    