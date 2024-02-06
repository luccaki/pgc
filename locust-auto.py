import subprocess
import time
import pandas as pd

result_df = pd.DataFrame()

for n in range(50, 1801, 50):
    for i in range(7):
        print(f"Step: {n} and {i}")
        locust_process = subprocess.Popen(f"locust --headless -u {n} -r {n} -H http://localhost:3001 --csv=teste".split())
        time.sleep(1)
        start_time = time.time()
        df = pd.read_csv("teste_stats.csv")
        df = df.tail(1)
        df = df[['Request Count','Failure Count','Average Response Time','Requests/s','Failures/s']]

        while(df.iloc[0, 0] < n):
            df = pd.read_csv("teste_stats.csv")
            df = df.tail(1)
            df = df[['Request Count','Failure Count','Average Response Time','Requests/s','Failures/s']]
            time.sleep(1)

        end_time = time.time()
        locust_process.send_signal(subprocess.signal.SIGINT)

        df['Execution Time'] = end_time - start_time
        result_df = pd.concat([result_df, df])
        result_df.to_csv('final_data.csv', index=False)

#locust --headless -u 1000 -r 1000 -H http://localhost:3001 --csv=teste