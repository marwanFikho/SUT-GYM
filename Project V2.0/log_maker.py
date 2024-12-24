from misc_funs import *

def log(who, action, what = "None"):
    log_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([who, action, what, log_date])
