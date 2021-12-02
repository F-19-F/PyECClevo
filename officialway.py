import time
from ec import EC


class Clevo_EC():
    FCMD = 0xF8
    FDAT = 0xF9
    FBUF = 0xFA
    FBUF1 = 0xFB
    FBUF2 = 0xFC
    FBUF3 = 0xFD

    @staticmethod
    def SetFanDutyAuto(fanNr: int):
        EC.Write(Clevo_EC.FDAT, 0xFF)
        EC.Write(Clevo_EC.FBUF, fanNr)
        EC.Write(Clevo_EC.FCMD, 0xC1)

    @staticmethod
    def SetFanDuty(fanNr: int, percent: int):
        duty = int(percent*255/100+0.5)
        EC.Write(Clevo_EC.FDAT, fanNr)
        EC.Write(Clevo_EC.FBUF, duty)
        EC.Write(Clevo_EC.FCMD, 0xC1)

    @staticmethod
    def SetWhiteLedKB(level: int):
        EC.Write(Clevo_EC.FDAT, 0x0)
        EC.Write(Clevo_EC.FBUF, level)
        EC.Write(Clevo_EC.FCMD, 0xCA)

    @staticmethod
    def GetWhiteLedKB():
        EC.Write(Clevo_EC.FDAT, 0x01)
        EC.Write(Clevo_EC.FCMD, 0xCA)
        res = EC.Read(Clevo_EC.FBUF)
        EC.Write(Clevo_EC.FCMD, 0x00)
        return res

    @staticmethod
    def Fan1Info():
        EC.Write(Clevo_EC.FDAT, 0x02)
        EC.Write(Clevo_EC.FCMD, 0xC0)
        time.sleep(0.0001)
        unknown = EC.Read(Clevo_EC.FBUF2)
        EC.Write(Clevo_EC.FCMD, 0x00)
        EC.Write(Clevo_EC.FDAT, 0x03)
        EC.Write(Clevo_EC.FCMD, 0xC0)
        time.sleep(0.0001)
        duty = EC.Read(Clevo_EC.FDAT)
        temp = EC.Read(Clevo_EC.FBUF2)
        return {
            "temp": temp,
            "duty": int(100*duty/255+0.5)
        }

    @staticmethod
    def Fan2Info():
        EC.Write(Clevo_EC.FDAT, 0x00)
        EC.Write(Clevo_EC.FCMD, 0xC0)
        temp = EC.Read(Clevo_EC.FDAT)
        unknown = EC.Read(Clevo_EC.FBUF)
        duty = EC.Read(Clevo_EC.FBUF1)
        EC.Write(Clevo_EC.FCMD, 0x00)
        return {
            "temp": temp,
            "duty": int(100*duty/255+0.5)
        }

    @staticmethod
    def GetFan12RPM():
        EC.Write(Clevo_EC.FDAT, 0x03)
        EC.Write(Clevo_EC.FCMD, 0xC0)
        data1 = EC.Read(Clevo_EC.FBUF)
        data2 = EC.Read(Clevo_EC.FBUF1)
        fan1rpm = (data1 << 0x08) | data2
        EC.Write(Clevo_EC.FCMD, 0x00)
        EC.Write(Clevo_EC.FDAT, 0x04)
        EC.Write(Clevo_EC.FCMD, 0xC0)
        data3 = EC.Read(Clevo_EC.FDAT)
        data4 = EC.Read(Clevo_EC.FBUF)
        fan2rpm = (data3 << 0x08) | data4
        EC.Write(Clevo_EC.FCMD, 0x00)
        if fan1rpm != 0:
            fan1rpm = int(2156220/fan1rpm + 0.5)
        if fan2rpm != 0:
            fan2rpm = int(2156220/fan2rpm + 0.5)
        return {
            'fan1rpm': fan1rpm,
            'fan2rpm': fan2rpm
        }

    @staticmethod
    def GetPowerStateForCamera():
        EC.Write(Clevo_EC.FDAT, 0xA1)
        EC.Write(Clevo_EC.FCMD, 0xB8)
        stat = EC.Read(Clevo_EC.FDAT)
        EC.Write(Clevo_EC.FCMD, 0x00)
        if (stat & 0b01 == 1):
            # True to enable
            return True
        else:
            return False


if __name__ == '__main__':
    Clevo_EC.SetFanDuty(1, 100)
    Clevo_EC.SetFanDuty(2, 100)
    Clevo_EC.SetWhiteLedKB(5)
    print("FAN1:", Clevo_EC.Fan1Info())
    print("FAN2:", Clevo_EC.Fan2Info())
    print(Clevo_EC.GetFan12RPM())
    if Clevo_EC.GetPowerStateForCamera():
        print("Camera on")
    else:
        print("camera off")
    time.sleep(1)
    print("FAN1:", Clevo_EC.Fan1Info())
    print("FAN2:", Clevo_EC.Fan2Info())
    Clevo_EC.SetWhiteLedKB(0)
    Clevo_EC.SetFanDutyAuto(1)
    Clevo_EC.SetFanDutyAuto(2)
    # while True: #tricks
    #     if i <= 1:
    #         toadd = True
    #     Clevo_EC.SetWhiteLedKB(i)
    #     if i == 5:
    #         toadd = False
    #     if toadd:
    #         i+=1
    #     else:
    #         i-=1
    #     time.sleep(0.05)
