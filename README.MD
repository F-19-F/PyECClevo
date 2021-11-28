# clevoec
## a tool to control clevo fan and get temperature via EC on windows,and it is easy to work on linx (just call inb and outb), this project aims to show how to control clevo laptop via EC
## Usage
```python
from clevoec import Clevo_EC
# fanNr from 1,0-100 to set FanDuty
Clevo_EC.SetFanDuty(1,100)
# set fan1 to auto control by EC
Clevo_EC.SetFanDutyAuto(1)
# get temperature and duty of fan 1
print(Clevo_EC.GetTempFanDuty(1))
```
* If something error happen, try to install driver in InpOutBinaries_1501
### Acknowledgement
* Phil Gibbons for windows usersapce port io [driver](https://www.highrez.co.uk/Downloads/InpOut32/)
* [parallel64](https://github.com/tekktrik/parallel64)
* ECInfo.dll By Candy Yang
