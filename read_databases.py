    

import dbm,pickle,multiprocessing



if __name__ == "__main__":
    with dbm.open("control_unit_datas.db","c") as database:
        for key,value in database.items():
            print("*********************")
            print(key,"LENGHT:",len(pickle.loads(value)))
            print("*********************")
            print(key,pickle.loads(value))
        
