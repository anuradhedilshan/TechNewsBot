import schedule
import time

def fetch_data():
    try:
        print(hello)
    except Exception as e:
        print("error" ,e.with_traceback())

schedule.every(5).seconds.do(fetch_data)




if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)