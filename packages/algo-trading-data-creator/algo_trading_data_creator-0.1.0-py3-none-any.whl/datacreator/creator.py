import pymssql
import pandas as pd

class DataCreator:
    def __init__(self, server=None, user=None, password=None, database=None, as_dict=True):
        self._server = server
        self._user = user
        self._password = password
        self._database = database
        self._as_dict = as_dict
        self._connected = False

    def SetConnectionInfo(self, server, user, password, database, as_dict=True):
        self._server = server
        self._user = user
        self._password = password
        self._database = database
        self._as_dict = as_dict

    def ReadData(self, df_params):
        try:
            conn = pymssql.connect(
                server=self._server,
                user=self._user,
                password=self._password,
                database=self._database,
                as_dict=self._as_dict
            )
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to the database. Please make sure your connection parameters are correct "
                f"and try again using the SetConnection() method. Original error: {e}"
            )

        query = """
            SELECT *
            FROM GetKlineData2(%s, %s, %s, %s)
            ORDER BY time
        """

        df_dict = {}
        for params in df_params:
            key = params[-1]
            print(f"{key} için veri okunuyor")
            cursor = conn.cursor()
            cursor.execute(query, params[:-1])
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            df_dict[key] = df
        conn.close()
        return df_dict

    def FormatData(self, df):
        df = df.drop('TimeStamp', axis=1)
        df["Time"] = pd.to_datetime(df["Time"], format='%d.%m.%Y %H:%M:%S')
        df.set_index("Time", inplace=True)
        df = df.apply(pd.to_numeric, errors='coerce')
        df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)
        return df

    def GetReadyData(self, df_params):
        df_list = self.ReadData(df_params)
        for key, df in df_list.items():
            df_list[key] = self.FormatData(df)
        return df_list
