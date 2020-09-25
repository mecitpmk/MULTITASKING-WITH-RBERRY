import multiprocessing,threading,time,os,dbm,pickle,datetime,random



class DATAPROCESS:
    def __init__(self):
        self.data_dict = {"ALTITUDE":multiprocessing.Manager().list(),"PRESSUREIN":multiprocessing.Manager().list(),
                                "GPS":multiprocessing.Manager().list(),"PRESSUREOUT":multiprocessing.Manager().list(),
                                    "HALLEFFECT":multiprocessing.Manager().list(),"GYRO":multiprocessing.Manager().list(),
                                                "TEMP":multiprocessing.Manager().list()}

        self.data_dict2 = {"ALTITUDE":multiprocessing.Manager().list(),"PRESSUREIN":multiprocessing.Manager().list(),
                                "GPS":self.data_dict["GPS"],"PRESSUREOUT":multiprocessing.Manager().list(),
                                    "HALLEFFECT":multiprocessing.Manager().list(),"GYRO":multiprocessing.Manager().list(),
                                                "TEMP":multiprocessing.Manager().list()}
        self.testBOOL = multiprocessing.Manager().Value("boolean",True)
    def return_data(self):
        return random.randint(100,103)

    def READ_ALTITUDE(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data() #RETURN DATA MESELA SENSORDEN GELEN DEGER OLUR ORNEK VERECEK OLURSAK
                                    # self.bmp085= BMP085.BMP085(BMP085.BMP085_ULTRAHIGHRES)   # __init__'de tanımladığımızı varsayalım
                                    # value = self.bmp085.ALTITUDEREAD()
            
            if value == 101:        # 101.metredeysek servo motor çalışsın.
                # self.servo_control()
                pass
                
            self.data_dict["ALTITUDE"].append(value)

    def READ_PRESSUREIN(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data()
            self.data_dict["PRESSUREIN"].append(value)
    
    def READ_GPS(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data()
            self.data_dict["GPS"].append(value)
    
    def READ_PRESSUREOUT(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data()
            self.data_dict["PRESSUREOUT"].append(value)
    
    def READ_HALLEFFECT(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data()
            self.data_dict["HALLEFFECT"].append(value)
    def READ_GYRO(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data()
            self.data_dict["GYRO"].append(value)

    def READ_TEMP(self):
        for i in range(200):
            time.sleep(0.05)
            value = self.return_data()
            self.data_dict["TEMP"].append(value)
        self.testBOOL.value = False
    def servo_control(self):
        pass
        # time.sleep(0.05)
        # print("******************SERVO MOTOR 10DEGREES.***********************")
    def READ_VOLTAGE(self):
        return self.return_data()
    def READ_DATAS(self):
        """
        Özet : GPS HARİCİ 0.5 saniyede toplanan !!!verilerin ortalamasını!!! almakta. GPS HARİÇ ÇÜNKÜ ANLIK OLARAK NERDE OLDUĞUNU BULMAK İSTİYORUM.
                örnek : [100,101,102]    0.5 saniyede 3 data çekebildiğini varsayalım, haberleşme ile göndermeden önce (100+101+102)/3 yaparak
                                                                                        kesinliği arttıracağımızı düşündüm.

        Ekstra:  Düşüş anında işlemciyi rahatlatmak için if condition ile 1 metre ya da 0.5 m geldiğinde diğer sensörler veri göndermeyi durdurtabilirsin.
        Şu şekilde yaparsın, Manager().Value'den initial = True tanımlarsın, daha sonra initial false yaparsın. yukardaki condition çalışır.
        """ 
        #SENDDATAS ACTUALLY.
        time.sleep(0.5) # BI SANIYE BEKLE.
        while self.testBOOL.value: # LOOP SONA ERENE KADAR BEKLE. BURAYI WHILE TRUE YAPICAZ.
            print("--------")
            for key,value in self.data_dict.items():
                if key == "GPS":
                    continue
                else:
                    print(key,"LENGHT OF LIST:",len(value))
                    self.data_dict2[key].append(sum(value)/len(value))
                    value[:]=[]
            print("------")
            time.sleep(0.5) #HER YARIM SANIYEDE BIR VERI CEK.
            


    def first_cpu(self):
        # for i in range(100):
        #     self.READ_ALTITUDE()
        #     self.READ_PRESSUREIN()
        altitude_thread = threading.Thread(target=self.READ_ALTITUDE)
        pressure_in_thread = threading.Thread(target=self.READ_PRESSUREIN)
        thread_tuple = (altitude_thread,pressure_in_thread)
        for i in thread_tuple:i.start()
        for i in thread_tuple:i.join()


    def second_cpu(self):
        # for i in range(100):
        self.READ_DATAS()
    
    def third_cpu(self):
        # for i in range(100):
        #     self.READ_GPS()
        #     self.READ_PRESSUREOUT()
        #     self.READ_HALLEFFECT()
        """
            Her bir işlemci'de iş parçacığı görevlendirerek, daha hızlı çalışmasını sağladım.
        """
        gps_thread = threading.Thread(target=self.READ_GPS)
        pressure_out_thread = threading.Thread(target=self.READ_PRESSUREOUT)
        hall_effect_thread = threading.Thread(target=self.READ_HALLEFFECT)
        thread_tuple = (gps_thread,pressure_out_thread,hall_effect_thread)
        for i in thread_tuple:i.start()
        for i in thread_tuple:i.join()

    def fourth_cpu(self):
        # for i in range(100):
        #     self.READ_GYRO()
        #     self.READ_TEMP()
        gyro_thread = threading.Thread(target=self.READ_GYRO)
        temp_thread = threading.Thread(target=self.READ_TEMP)
        thread_tuple = (gyro_thread,temp_thread)
        for i in thread_tuple:i.start()
        for i in thread_tuple:i.join()
        
    def RUN_SYSTEM(self):

        """
        Raspberry Pi Quad-Core (4 Çekirdek).

        1.İşlemci'de : Altitude ve PRESSURE(CONTAINER INSIDE) Ölçülmekte.
        2.İşlemci'de :  SADECE DATALAR OKUNMAKTA ---ASLINDA PARAMETRELER HABERLEŞME İLE GÖNDERİLECEK---
        3.İşlemci'de : GPS , PRESSURE(CONTAINER OUTSIDE) ve HALL EFFECT SENSOR ÖLÇÜLMEKTE
        4.İşlemci'de : Gyroscope ve Temperature SENSOR ÖLÇÜLMEKTE
        
            NOT: Her bir işlemci' içinde threading işlemi yaparak, data toplama işlemi'nin Precision'u arttırıldı.
        """

        process1 = multiprocessing.Process(target=self.first_cpu)
        process2 = multiprocessing.Process(target=self.second_cpu)
        process3 = multiprocessing.Process(target=self.third_cpu)
        process4 = multiprocessing.Process(target=self.fourth_cpu)

        proccess_tuples = (process1,process2,process3,process4)
        self.t1 = multiprocessing.Manager().Value("time",time.time())
        for functs in proccess_tuples:functs.start()
        for functs in proccess_tuples:functs.join()


if __name__ == "__main__":
    
    system = DATAPROCESS()
    t1 = time.time()
    system.RUN_SYSTEM()
    t2 = time.time()
    print("GEÇEN SÜRE :",t2-t1)
    # print(system.data_dict)
    # print(system.data_dict2)
    for key,value in system.data_dict2.items():
        print(key,"LENGHT OF LIST:",len(value))
    with dbm.open("control_unit_datas.db","c") as database:
        for datas in system.data_dict2:
            test = list(system.data_dict2[datas])
            database[datas] = pickle.dumps(list(system.data_dict2[datas]))