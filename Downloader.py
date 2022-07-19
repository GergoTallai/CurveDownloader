import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import os

# GORBE MENTESE
class Downloader(object):
    file_path = ''
    def downloader(self):
        dest_folder = "curve"
        filename = "last_curve"
        ip_address = 'XXX.XXX.XXX.XXX'
        url_address = 'http://{}/cgi-bin/cgiread?site=12&dlfile=/mnt/mmc/curvedata/graph.bin&dltype=csv'.format(ip_address)

        # GORBE ELERESI UTVONAL
        Downloader.file_path = os.getcwd() + "\\" + dest_folder + "\\" + filename

        # MAPPA LETREHOZASA
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            print('folder created...')

        start = time.perf_counter()

        print('download started...')
        get_bin = requests.get(url_address)
        if get_bin.ok:
            print("saving to..." + Downloader.file_path)
            output = open(Downloader.file_path + '.csv', 'wb')
            output.write(get_bin.content)
            output.close()

        finish = time.perf_counter()

        print('download time: ', round(finish - start), 's')
        CSV_Reader().csv_reader()

# LETOLTOTT CSV BEOLVASA
class CSV_Reader(Downloader):
    def csv_reader(self):
        print(Downloader.file_path + '.csv')
        curve_datas = pd.read_csv(Downloader.file_path + '.csv', encoding = "ISO-8859-1")

        # CSV ADATOK BETOLTESE ES LEVALOGATASA
        headers = ['Time (ms)', 'Torque', 'Angle', 'Motor Torque', 'Motor Angle', 'Speed', 'Step', 'Current (A)', 'Temperature (C)']
        time = []
        torque = []
        angle = []
        motor_torque = []
        motor_angle = []
        speed = []
        step = []
        current = []
        temperature = []

        for i in range(0, len(curve_datas.columns)):
            for j in range(0, curve_datas[curve_datas.columns[0]].count()):
                match i:
                    case 0:
                        time.append(curve_datas.iat[j,i])
                    case 1:
                        torque.append(curve_datas.iat[j,i])
                    case 2:
                        angle.append(curve_datas.iat[j,i])
                    case 3:
                        motor_torque.append(curve_datas.iat[j,i])
                    case 4:
                        motor_angle.append(curve_datas.iat[j,i])
                    case 5:
                        speed.append(curve_datas.iat[j,i])
                    case 6:
                        step.append(curve_datas.iat[j,i])
                    case 7:
                        current.append(curve_datas.iat[j,i])
                    case 8:
                        temperature.append(curve_datas.iat[j,i])
        fig = plt.figure()
        ax1 = fig.add_subplot()
        ax1.plot(time, torque, '-', label='Torque', color='blue')
        ax2 = ax1.twinx()
        ax2.plot(time, angle, '-', label='Angle', color='red')
        ax3 = ax1.twinx()
        ax3.plot(time, speed, '-', label='Speed', color='black')
        ax3.spines['right'].set_position(('axes', 1.10))

        ax1.grid()
        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel("Torque")
        ax1.set_ylim(min(torque) * 0.9, max(torque) * 1.1)
        ax2.set_ylabel("Angle")
        ax2.set_ylim(min(angle) * 0.9, max(angle) * 1.1)
        ax3.set_ylabel("Speed")
        ax3.set_ylim(min(speed) * 0.9, max(speed) * 1.1)
        plt.subplots_adjust(right=0.8)
        plt.show()

# START MAIN
if __name__ == "__main__":
    print('Start Downloader')
    Downloader().downloader()
