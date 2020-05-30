import time

import aioserial
import asyncio
import serial.urlhandler.protocol_hwgrep
import logging

# Set Up Logging
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

async def read_and_print(aioserial_instance: aioserial.AioSerial):
    while True:
        print((await aioserial_instance.read_async()).decode(errors='ignore'), end='', flush=True)

async def write_and_read(aioserial_instance: aioserial.AioSerial):
    await aioserial_instance.write_async("V".encode('ascii')+b'\r')
    await asyncio.sleep(.001)
    b = aioserial_instance.in_waiting
    logger.debug(f"data: {(await aioserial_instance.read_async(size=b))}")
    asyncio.ensure_future(read_and_print(aioserial_instance))




def check_version(self):
    response = self.send_command("V")
    version_string = b'UBW32 Version 1.6.6'
    if not response.startswith(version_string):
        logger.error(f'The reported version {response} does not match {version_string}')

def read_version():
    port = serial.serial_for_url(f'hwgrep://{hwid}')
    start_time = time.time()
    port.write("V".encode('ascii')+b'\r')
    time.sleep(0.001)
    b = port.in_waiting
    print(port.read(size=b))
    duration = time.time() - start_time
    logger.debug(f"duration: {duration}")
    port.close()

if __name__ == "__main__":
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - <%(funcName)s:%(lineno)s> - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    hwid = 'VID:PID=04D8:FD92'
    # https://stackoverflow.com/questions/24683987/executable-out-of-script-containing-serial-for-url/24688413#24688413
    # __import__('serial.urlhandler.protocol_hwgrep')
    # self.port = sys.modules['serial.urlhandler.protocol_hwgrep'].Serial(f'hwgrep://{hwid}')
    read_version()

    # port =
    # asyncio.run(read_and_print(aioserial.serial_for_url(f'hwgrep://{hwid}')))
    # port = aioserial.AioSerial(port="COM5")
    port = aioserial.serial_for_url(f'hwgrep://{hwid}')
    port_com = port.name
    logger.debug(f'name: {port_com}')
    port.close()

    port = aioserial.AioSerial(port=port_com)
    # # port = serial.serial_for_url(f'hwgrep://{hwid}')
    # port.write("V".encode('ascii')+b'\r')
    # time.sleep(0.05)
    # b = port.in_waiting
    # print(port.read(size=b))
    # port.close()
    start_time = time.time()
    asyncio.run(write_and_read(port))
    duration = time.time() - start_time
    logger.debug(f"duration: {duration}")

