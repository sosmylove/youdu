import schedule,datetime
import time
from upload_book_youdu import upload_biqu_book


def job():
	print('\n', "i am working-----", time.strftime("%Y-%m-%d %H:%M:%S"))
	oldTime = datetime.datetime.now()
	aa.uploadBook()
	newTime = datetime.datetime.now()
	print("更新数据花了__:", newTime-oldTime)


schedule.every().day.at("19:07").do(job)
schedule.every().day.at("09:30").do(job)
schedule.every().day.at("11:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("14:16").do(job)
schedule.every().day.at("16:00").do(job)
schedule.every().day.at("17:00").do(job)
schedule.every().day.at("20:00").do(job)
schedule.every().day.at("21:30").do(job)
schedule.every().day.at("23:30").do(job)
schedule.every().day.at("03:00").do(job)


while True:
    aa = upload_biqu_book()
    schedule.run_pending()
