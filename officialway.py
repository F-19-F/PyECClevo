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

if __name__=='__main__':
    Clevo_EC.SetFanDuty(1,100)
    Clevo_EC.SetFanDuty(2,100)
    import time
    time.sleep(1)
    Clevo_EC.SetFanDutyAuto(1)
    Clevo_EC.SetFanDutyAuto(2)
