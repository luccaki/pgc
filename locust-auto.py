import subprocess
import time
import pandas as pd

result_df = pd.DataFrame()

for n in range(30):
    locust_process = subprocess.Popen("locust --headless -u 500 -H http://localhost --csv=teste".split())
    time.sleep(180)
    locust_process.send_signal(subprocess.signal.SIGINT)
    time.sleep(5)
    df = pd.read_csv("teste_stats_history.csv")
    max_value = df['User Count'].max()
    df = df[df['User Count'] == max_value]
    print(df)
    print("User count: ", df["User Count"])

    result_df = pd.concat([result_df, df])
    result_df.to_csv('final_data.csv', index=False)
