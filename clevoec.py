from ec import EC
class Clevo_EC():
    # 255 to set all to auto
    @staticmethod
    def SetFanDutyAuto(fanNr: int):
        EC.Register.SetCmd(0x99)
        EC.Register.SetData(0xFF)
        EC.Register.SetData(fanNr)

    @staticmethod
    def SetFanDuty(fanNr: int, percent: int):
        duty = int(percent*255/100+0.5)
        EC.Register.SetCmd(0x99)
        EC.Register.SetData(fanNr)
        EC.Register.SetData(duty)

    @staticmethod
    def GetTempFanDuty(fanNr: int):
        EC.Register.SetCmd(0x9E)
        EC.Register.SetData(fanNr)
        temp = EC.Register.GetData()
        unknown = EC.Register.GetData()
        duty = EC.Register.GetData()
        return {
            "temp": temp,
            "duty": int(100*duty/255+0.5)
        }

    @staticmethod
    def GetFanCount():
        return EC.Read(0xC8)

    # standard read EC
    @staticmethod
    def GetFanRpm(fanNr: int):
        offset = (fanNr - 1)*2
        value = (EC.Read(0xD0+offset) << 8 | EC.Read(0xD1+offset))
        if value == 0:
            return 0
        return int((2156220/value)+0.5)


if __name__ == '__main__':
    Clevo_EC.SetFanDuty(1,100)
    import time
    time.sleep(2)
    print(Clevo_EC.GetTempFanDuty(1))
    print(Clevo_EC.GetFanRpm(1))
    Clevo_EC.SetFanDutyAuto(1)
    print(Clevo_EC.GetFanRpm(1))
    
    
