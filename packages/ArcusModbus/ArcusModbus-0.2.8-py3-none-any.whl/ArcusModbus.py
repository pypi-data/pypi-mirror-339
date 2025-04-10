import math
from pymodbus.client import AsyncModbusTcpClient as AClient
#from pymodbus.constants import Endian
#from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
import asyncio
import time


class Probes:
    def __init__(self, ip: str, insertRadius: int, COUNTSPERMM: int):
        self.ip = ip
        self.r = insertRadius
        self.CPMM = COUNTSPERMM
        self.client = 0
        self.speed = 0
        self.accel = 0
        self.homed = False

    async def connect(self):
        self.client = AClient(self.ip, port=5000)             # Create client object
        await self.client.connect()                # connect to device, reconnect automatically
        
        await self.client.write_coils(13, [False]) #clears errors
        await self.client.write_coils(13, [True])

    
    async def disconnect(self):
        await self.client.write_coils(8, [False])
        await self.client.write_coils(8, [True]) #turn off motor

        self.client.close() #close the connection
    
    async def initiate(self, speed: int, accel: int):
        payloadunbuilt = [speed, accel, 10000, 1, 0]
        addresses = [2, 4, 6, 8, 10]

        #in order, these addresses corrispond to:
        #target speed, target acceleration, target jerk, move pattern, homing mode
        await self.writeRegisters(addresses, payloadunbuilt)

        await self.client.write_coils(7, [False]) 
        await self.client.write_coils(7, [True]) #turn servo on

    async def checkRegisters(self, *registers):
        decodedValues = []
        for i in registers:
            encodedValue = await self.client.read_holding_registers(address=i, count=2)
            #decoded = BinaryPayloadDecoder.fromRegisters(encodedValue.registers, byteorder=Endian.BIG, wordorder=Endian.BIG).decode_32bit_int()
            decoded = self.client.convert_from_registers(encodedValue.registers,self.client.DATATYPE.INT32,"big")
            decodedValues.append(decoded)
        return decodedValues
    
    async def writeRegisters(self, register, value):
        #builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        for i in range(len(register)):
            #builder.add_32bit_int(value[i])
            #payload = builder.to_registers()
            payload = self.client.convert_to_registers(value[i],self.client.DATATYPE.INT32,"big")
            await self.client.write_registers(address=register[i], values=payload)
            #builder.reset()

    async def motorStatus(self):
        statusDecimal = await self.checkRegisters(10)
        statusBin = f'{statusDecimal[0]:0{5}b}'
        #the :0b specifies in decimal, while the {5} ensures there are 5 total digits, even if they are 0
        #if I used bin(statusDecimal[0]) it would trim the leading 0's and the info with it
    
        enabled = int(statusBin[4])
        inPos = int(statusBin[3])
        moving = int(statusBin[2])
        inFault = int(statusBin[1])
        homed = int(statusBin[0])
        return [enabled,inPos,moving,inFault,homed]
    
    async def move(self, distance: float): #give distance in mm
        
        isMoving = await self.motorStatus()
        if isMoving[2] == 1:
            print("already moving, ignoring command!")
            return
        elif self.homed != True:
            print("please home before moving. Ignoring command!")
            return

        MovDistance = -1*(distance * float(self.CPMM))
        print(math.floor(MovDistance))
        SoftLimit = -1*(self.r * self.CPMM)
        if MovDistance <= SoftLimit:
            raise Exception(f"You cannot move more than what this probe allows ({self.r})")


        #print(payload)
        await self.writeRegisters([0], [int(math.floor(MovDistance))])

        await self.client.write_coils(9, [False])
        await self.client.write_coils(9, [True]) #begin movement

        isMoving = await self.motorStatus()
        while isMoving[2] == 1:
            isMoving = await self.motorStatus()
            await asyncio.sleep(1)

    
    async def home(self):

        isMoving = await self.motorStatus()
        if isMoving[2] == 1:
            print("already moving, ignoring command!")
            return

        await self.client.write_coils(14, [False])
        await self.client.write_coils(14, [True]) #stop all motion

        await self.client.write_coils(12, [False])
        await self.client.write_coils(12, [True]) #homes the motor until limit switch is hit


        #TODO: somehow stop movement without interupting the flow of the program
        isHomed = await self.motorStatus()
        while isHomed[3] != 1: #check for a fault
            isHomed = await self.motorStatus()
            await asyncio.sleep(1)

        #once faulted, reenable then set encoder position to 0

        await self.client.write_coils(7, [False]) 
        await self.client.write_coils(7, [True]) #turn servo on

        await self.client.write_coils(13, [False]) #clears errors
        await self.client.write_coils(13, [True])

        await self.writeRegisters([14], [0]) #set encoder position to 0

        self.homed = True

        return True
    
    async def ESTOP(self):
        print("STOPPING MOTION")
        await self.client.write_coils(14, [False])
        await self.client.write_coils(14, [True]) #stop all motion
        print("MOTION STOPPED, SHUTTING DOWN")
        status = await self.motorStatus()
        faultCodes = await self.checkRegisters(12)
        print(f"Motor Status: {status} :: Fault Codes: {faultCodes}")
        await self.disconnect()



##### testing from here on out #####
#async def init(probe: Probes):
#    await probe.connect()
#    await probe.initiate(300, 4000)
#    status = await probe.motorStatus()
#    print(status)
#
#    homing = asyncio.create_task(probe.home()) #this will start homing
#    #you can do anything (except move) while this is running
#    #but to know when its done you will need to use await homing which will halt the program
#    #by doing it this way you can concurrently home an infinite number of probes
#
#    print("homing")
#
#    await asyncio.sleep(1) #it takes the motor a tiny amount of time to send the signal that it is moving
#
#    status = await probe.motorStatus()
#    print(status)
#
#    
#
#    await probe.move(5) #shouldnt work as the motor is already moving
#
#    await asyncio.sleep(1)
#
#    check = await homing
#
#    if check == True:
#        print("homed")
#
#    await probe.disconnect()
#
#if __name__ == "__main__":
#    probe1 = Probes("169.254.150.100", 100, 36000)
#    asyncio.run(init(probe1))