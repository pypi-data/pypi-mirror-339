import json
import os
import datetime
import paramiko
import socket
import threading
import sqlite3
import pymysql
import psycopg

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

from pathlib import Path
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from scipy.optimize import curve_fit
from statsmodels.robust.scale import huber
from sklearn.metrics import r2_score
from sklearn.linear_model import QuantileRegressor


class Tunnel:
    def __init__(self, ssh_host, ssh_port, ssh_user, ssh_pwd, ssh_pkey, remote_host, remote_port, local_port=5433, keybased=False):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_port = local_port
        self.keybased = keybased
        self.ssh_pwd = ssh_pwd
        self.ssh_pkey = ssh_pkey
        self.transport = None
        self.thread = None

    def start(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.keybased:
            self.client.connect(
                hostname=self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_user,
                key_filename=self.ssh_pkey,
            )
        else:
            self.client.connect(
                hostname=self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_user,
                password=self.ssh_pwd,
            )

        self.transport = self.client.get_transport()

        def forward():
            sock = socket.socket()
            sock.bind(('127.0.0.1', self.local_port))
            sock.listen(1)
            while True:
                conn, addr = sock.accept()
                channel = self.transport.open_channel(
                    "direct-tcpip",
                    (self.remote_host, self.remote_port),
                    conn.getsockname(),
                )
                threading.Thread(target=self._handle, args=(conn, channel)).start()

        self.thread = threading.Thread(target=forward, daemon=True)
        self.thread.start()

    def _handle(self, client_sock, ssh_channel):
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            ssh_channel.send(data)
            reply = ssh_channel.recv(1024)
            client_sock.send(reply)

    def stop(self):
        self.client.close()

class DB_connect(object):
    """
    The class 'LT_connect' can be used to connect to the LT postgres database
    via a ssh connection.\n

    Functions:
    ----------

    tables(self, db, schema, sql_user, sql_pass)\n
    print_columns(self, db, table_name, sql_user, sql_pass)\n
    query(self, db, query, sql_user, sql_pass)\n
    execute(self, db, query, sql_user, sql_pass)\n
    insert(self, db, query, data, sql_user, sql_pass)\n
    ret_con(self, db, sql_user, sql_pass)\n
    create_db(self, db, sql_user, sql_pass)

    Parameters
    ----------

    db : name of a postgres database that should be accessed \n
    p_host : address of the database of the system
    (usually localhost - 127.0.0.1) \n
    p_port : port for postgresql (usually 5432) \n
    ssh : if a ssh connection is necessary insert 'True' \n
    ssh_user : account name of the ssh user \n
    ssh_host : ip address of the server to which to connect \n
    ssh_pkey : filepath to the ssh key for faster access \n
    sql_user : account name of the postgres user \n
    sql_pass : password for the postgres account \n

    Return
    ------

    None


    """

    def __init__(
        self,
        ssh,
        ssh_host,
        ssh_port,
        ssh_user,
        keybased,
        ssh_pwd,
        ssh_pkey,
        db_host,
        db_port,
        db,
        sql_user,
        sql_pass,
        dbtype,
        sqlitepath,
    ):
        """
        __init__(self, db_host, db_port, db, ssh, ssh_user, ssh_host, ssh_pkey, sql_user, sql_pass):
        -----------------------------------------------
        defines global class parameters for ssh connection\n

        Parameters
        ----------
        ssh : if a ssh connection is necessary insert 'True' \n
        ssh_host : ip address of the server to which to connect \n
        ssh_port : port of the server to which to connect \n
        ssh_user : account name of the ssh user \n
        keybased : boolean - True if ssh-key is used to connect to server \n
        ssh_pwd : password for ssh connection \n
        ssh_pkey : filepath to the ssh key for faster access \n
        db_host : address of the database of the system
        (usually localhost - 127.0.0.1) \n
        db_port : port for postgresql (usually 5432) \n
        db : name of a postgres database that should be accessed \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n
        dbtype : dbtype used (postgres, mysql, sqlite)

        Returns:
        --------
        None
        """
        local_port = 5433
        # SSH Tunnel Variables
        self.db_host = db_host
        self.db_port = db_port
        self.sql_user = sql_user
        self.sql_pass = sql_pass
        self.ssh_port = ssh_port
        self.dbtype = dbtype
        self.db = db
        self.echoparam = False

        if ssh == True:
            self.tunnel = Tunnel(
                ssh_host=ssh_host,
                ssh_port=ssh_port,
                ssh_user=ssh_user,
                ssh_pwd=ssh_pwd,
                ssh_pkey=ssh_pkey,
                remote_host=db_host,
                remote_port=db_port,
                local_port=local_port,
                keybased=keybased
            )
            self.tunnel.start()
            self.local_port = local_port
            print(f"Server connected via SSH using paramiko tunnel ...")

        else:
            self.local_port = db_port

        if dbtype == "postgres":
            self.enginestr = f"postgresql+psycopg://{self.sql_user}:{self.sql_pass}@127.0.0.1:{self.local_port}/{self.db}"

        elif dbtype == "mysql":
            self.enginestr = f"mysql+pymysql://{self.sql_user}:{self.sql_pass}@127.0.0.1:{self.local_port}/{self.db}"

        elif dbtype == "sqlite":
            if not os.path.exists(sqlitepath):
                os.makedirs(sqlitepath)
            self.enginestr = f"sqlite:///{sqlitepath}\\{self.db}.db"

    def tables(self, schema):
        """
        tables(self, db, schema, sql_user, sql_pass):
        -----------------------------------------------
        returns all table names in a given 'schema' of a database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        schema : name of the schema that should be analyzed\n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        tables_df (pandas dataframe of table names)

        """

        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/

        if self.dbtype == "sqlite":
            engine = create_engine(self.enginestr, echo=True)
        else:
            engine = create_engine(self.enginestr)
        conn = engine.connect()
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema=schema)
        self.tables_df = pd.DataFrame(tables, columns=["table name"])
        engine.dispose()
        return self.tables_df

    def print_columns(self, table_name):
        """
        print_columns(self, db, table_name, sql_user, sql_pass)
        -----------------------------------------------
        returns all table names in a given 'schema' of a database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        table_name : name of the table for which the columns schould be checked \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        tables_df (pandas dataframe of column names)

        """

        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/

        engine = create_engine(self.enginestr, echo=self.echoparam)

        if " " in table_name:
            if '"' in table_name:
                pass
            else:
                table_name = "'" + table_name + "'"
        query = (
            """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        ;
        """
            % table_name
        )
        self.table_df = pd.read_sql(query, engine)
        engine.dispose()
        return self.table_df

    def query(self, query):
        """
        query(self, db, query, sql_user, sql_pass)
        -----------------------------------------------
        executes a postgreSQL query in the database 'db' (return = true)\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        query : insert char string of postgreSQL code that should be queried \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        query_df (pandas dataframe of query result)

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)
        self.query_df = pd.read_sql(query, engine)
        engine.dispose()
        return self.query_df

    def execute(self, query):
        """
        execute(self, db, query, sql_user, sql_pass)
        -----------------------------------------------
        executes a postgreSQL query in the database 'db' (return = false)\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        query : insert char string of postgreSQL code that should be queried \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        None

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)
        with engine.begin() as connection:
            connection.execute(text(query))
        # engine.execute(text(query))
        engine.dispose()

    def insert(self, query, data):
        """
        insert(self, db, query, data, sql_user, sql_pass)
        -----------------------------------------------
        executes a postgreSQL query in the database 'db' (return = false),
        used to insert data with parameter data, use '%(name)s' in the query text
        and a dictionary ({name : value}) for data \n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        query : insert char string of postgreSQL code that should be queried \n
        data : dictionary of data that should be used in the query \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        None

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)

        with engine.begin() as connection:
            connection.execute(text(query), data)
        # engine.execute(text(query), data[0])
        engine.dispose()

    def ret_con(self):
        """
        ret_con(self, db, sql_user, sql_pass)
        -----------------------------------------------
        returns the engine to connect to the database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        engine

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/
        engine = create_engine(self.enginestr, echo=self.echoparam)
        return engine
    
    def close_tunnel(self):
        if hasattr(self, 'tunnel'):
            self.tunnel.stop()

    def create_db(self):
        """
        create_db(self, db, sql_user, sql_pass)
        -----------------------------------------------
        creates the database 'db'\n

        Parameters:
        ----------

        db : name of a postgres database that should be accessed \n
        sql_user : account name of the postgres user \n
        sql_pass : password for the postgres account \n

        Returns:
        --------
        None

        """
        # create an engine to connect to the postgreSQL database, documentation
        # of functions can be found at https://docs.sqlalchemy.org/en/14/

        print(self.dbtype)
        if self.dbtype == "sqlite":
            engine = create_engine(self.enginestr, echo=self.echoparam)
            Base = declarative_base()
            Base.metadata.create_all(engine)
        else:
            engine = create_engine(self.enginestr)
            if not database_exists(engine.url):
                create_database(engine.url)
            else:
                print('A database with the name "' + self.db + '" already exists')


def connCowBaseDB(rootdir):
    """
    Returns connection to database, specify parameters in settings file

    Parameters
    ----------
    rootdir : str
        path to cowbase rootdir
    """

    settingsPath = os.path.join(rootdir, "config", "serverSettings.json")

    with open(settingsPath) as file:
        serverSettings = json.load(file)

    # Create a connection to the database
    db_connect = DB_connect(**serverSettings)

    return db_connect

def correct_first_mi(group):
    """
    Corrects the first milk yield measurement if it is greater than or equal to 48.

    This function checks the first milk yield measurement (mi) in each group. If the value
    is greater than or equal to 48, it sets the value to None.

    Parameters
    ----------
    group (DataFrame): A group of rows from the input DataFrame, grouped by 'lactation_id'.

    Returns
    -------
    DataFrame: The group with the corrected first milk yield measurement.
    """
    if group.iloc[0]["mi"] >= 48:
        group.loc[group.index[0], "mi"] = None
    return group


def calculate_milk_corr(group, column, incomplete_set):
    """
    Calculates corrected milk yield for a specified column based on incomplete sets.

    This function iterates through the group and calculates corrected milk yield values
    for the specified column. It handles incomplete sets by summing the milk yields and
    milk intervals, and then distributing the corrected values proportionally.

    Parameters
    ----------
    group (DataFrame): A group of rows from the input DataFrame, grouped by 'lactation_id'.
    column (str): The name of the column to be corrected.
    incomplete_set (list): A list of incomplete set identifiers.

    Returns
    -------
    DataFrame: A DataFrame with the corrected milk yield values for the specified column.
    """
    milk_corr_list = []
    i = 0
    while i < len(group):
        if group.iloc[i]["incomplete"] not in incomplete_set:
            milk_corr_list.append(group.iloc[i][column])
            i += 1
        else:
            sum_milk = 0
            sum_mi = 0
            start = i
            while i < len(group) and group.iloc[i]["incomplete"] in incomplete_set:
                sum_milk += group.iloc[i][column]
                sum_mi += group.iloc[i]["mi"]
                i += 1
            if i < len(group) and group.iloc[i]["incomplete"] not in incomplete_set:
                sum_milk += group.iloc[i][column]
                sum_mi += group.iloc[i]["mi"]
                i += 1
            for j in range(start, i):
                milk_corr_list.append((sum_milk / sum_mi) * group.iloc[j]["mi"])
    return pd.DataFrame({f"{column}_corr": milk_corr_list}, index=group.index)

def corr_incomplete(data):
    """
    Corrects incomplete milk yield data for each lactation and day in milk (DIM).

    This function processes the input data by sorting, grouping, and applying corrections
    to the first milk yield measurement. It then applies a correction function to each
    specified column based on predefined incomplete sets. Finally, it calculates the total
    corrected milk yield (tmy_corr) as the sum of the corrected yields for the four quarters.

    Parameters
    ----------
    data (DataFrame): The input DataFrame containing milk yield data with columns 'lactation_id',
                      'dim', and the quarter-level milk yields ('mylf', 'myrf', 'mylr', 'myrr').

    Returns
    -------
    DataFrame: A DataFrame with corrected milk yields for each quarter and the total corrected
               milk yield (tmy_corr).
    """
    # Define the columns and their corresponding incomplete sets
    columns_incomplete_sets = {
        "mylf": [1, 3, 5, 7, 9, 11, 13, 15],
        "myrf": [2, 3, 6, 7, 10, 11, 14, 15],
        "mylr": [4, 5, 6, 7, 12, 13, 14, 15],
        "myrr": [8, 9, 10, 11, 12, 13, 14, 15],
    }
    data = (
        data.sort_values(by=["lactation_id", "dim"])
        .reset_index(drop=True)
        .groupby(by=["lactation_id"])
        .apply(correct_first_mi)
        .reset_index(drop=True)
    )
    data_corrected = (
        data.sort_values(by=["lactation_id", "dim"])
        .reset_index(drop=True)
        .copy()
    )
    # Apply the function to each column
    for column, incomplete_set in columns_incomplete_sets.items():
        data_corrected = data_corrected.join(
            data_corrected.groupby("lactation_id")
            .apply(calculate_milk_corr, column, incomplete_set)
            .reset_index(level=0, drop=True)
        )
    # Calculate tmy_corr as the sum of the four quarter-level corrected milk yields
    data_corrected["tmy_corr"] = (
        data_corrected["mylf_corr"]
        + data_corrected["myrf_corr"]
        + data_corrected["mylr_corr"]
        + data_corrected["myrr_corr"]
    )

    return data_corrected

def quality_control(
    farm_id,
    cowbase_rootdir,
    thresholds={
        "mi": 48,
        # "BHB": [0.01, 3],
        # "P4": [0.01, 40],
        # "LDH": [0.01, 1000],
        "tmy": 40,
        "qlmy": 15,
        "qlec": 8,
    },
):
    """
    Defines a set of quality control steps on animal level

    Parameters
    ----------
    farm_id: int
        ID of the farm for which the quality control should be run
    cowbase_rootdir: str
        Filepath of the cowbase rootdir including the settings.
        In the CowBase directory a new folder will be created 'quality_control' in which all figures for the quality
        control will be saved.
    thresholds: dict
        A dictionary containing all thresholds that should be applied for out of control measurements. If a lactation
        has a value out of control, this will be indecated in the output lists and a time series plot will be created
        to check manually if the animal/lactation should be excluded from further analysis

    Returns
    -------
    suspected_animals: list
        List of animals that are suspected to contain faulty data. Check manually in CowBase/animal_level if an
        animal should be excluded from further analysis

    suspected_lactations: list
        List of lactations that are suspected to contain faulty data. Check manually in CowBase/data_overview &
        CowBase/lactation_level if an lactations should be excluded from further analysis

    """

    rootdir = Path(cowbase_rootdir)

    # initialize folder structure
    rootdir_cowbase = rootdir / "CowBase"
    rootdir_cowbase.mkdir(exist_ok=True, parents=True)

    rootdir_quality_control = rootdir_cowbase / "quality_control"
    rootdir_quality_control.mkdir(exist_ok=True)

    outdir = rootdir_quality_control / f"farm_{farm_id}"
    outdir.mkdir(exist_ok=True)

    outdir_animal_level = (
        rootdir_quality_control / f"farm_{farm_id}" / "animal_level"
    )
    outdir_animal_level.mkdir(exist_ok=True)

    outdir_data_overview = (
        rootdir_quality_control / f"farm_{farm_id}" / "data_overview"
    )
    outdir_data_overview.mkdir(exist_ok=True)

    outdir_lactation_level = (
        rootdir_quality_control / f"farm_{farm_id}" / "lactation_level"
    )
    outdir_lactation_level.mkdir(exist_ok=True)

    dbconn = connCowBaseDB(rootdir_cowbase)

    sqlscript = f"SELECT farm_id, animal_id, parity, calving, age_at_first_calving, lactation_length FROM lactation_corrected WHERE farm_id={farm_id} AND parity < 90"

    df_lac_corr = dbconn.query(query=sqlscript)

    df_lac_corr.calving = pd.to_datetime(df_lac_corr.calving)

    sqlscript = f"SELECT farm_id, animal_id, parity, calving FROM lactation WHERE farm_id={farm_id}"

    df_lac = dbconn.query(query=sqlscript)

    df_lac.calving = pd.to_datetime(df_lac.calving)

    ####################################################################################################################
    # Step 1: Check for differences between the corrected lactation information and the farmer-entered lactation information
    merged = pd.merge(
        df_lac_corr[
            [
                "farm_id",
                "animal_id",
                "parity",
                "calving",
                "age_at_first_calving",
                "lactation_length",
            ]
        ],
        df_lac[["farm_id", "animal_id", "parity", "calving"]],
        on=["farm_id", "animal_id", "parity", "calving"],
        how="outer",
        indicator=True,
    )

    # Identify rows that are present in one DataFrame but not the other
    differences = merged[merged["_merge"] == "left"]
    differences = differences.loc[
        pd.isnull(differences.lactation_length) | (differences.lactation_length <= 270)
    ]

    unusual_aafc = df_lac_corr.loc[
        (df_lac_corr.age_at_first_calving <= 400)
        | (df_lac_corr.age_at_first_calving >= 1050)
    ]

    # Sort the DataFrame by animal_id and parity
    data_sorted = df_lac_corr.sort_values(by=["animal_id", "parity"])
    # Calculate the difference in calving dates between subsequent rows
    data_sorted["calving_diff"] = data_sorted.groupby("animal_id")["calving"].diff()
    # Select rows where the difference in calving dates is less than 270 days
    short_lac = data_sorted[
        (data_sorted["calving_diff"] < pd.Timedelta(days=270))
        & (data_sorted["calving_diff"].notnull())
    ]

    # Concatenate the lists and remove duplicates
    suspected_animals = np.unique(
        np.concatenate(
            [
                differences.animal_id.unique(),
                unusual_aafc.animal_id.unique(),
                short_lac.animal_id.unique(),
            ]
        )
    )

    if len(suspected_animals) > 0:
        for ani_id in suspected_animals:
            sqlscript = f"SELECT farm_id, animal_id, lactation_id, milking_id, parity, started_at, ended_at, dim, mi, tmy, mylf, myrf, mylr, myrr FROM milking WHERE farm_id={farm_id} AND animal_id={ani_id}"
            df_animal_milk = dbconn.query(query=sqlscript)

            sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, calving FROM lactation WHERE farm_id={farm_id} AND animal_id={ani_id}"
            df_animal_lac = dbconn.query(query=sqlscript)

            sqlscript = f"SELECT farm_id, animal_id, parity, calving, birth_date FROM lactation_corrected WHERE farm_id={farm_id} AND animal_id={ani_id} AND parity < 90"
            df_animal_lac_corr = dbconn.query(query=sqlscript)

            df_animal_milk["tmy_prod"] = (df_animal_milk.tmy / df_animal_milk.mi) * 24
            df_animal_milk_uncorr = df_animal_milk.copy()

            if not df_animal_milk.empty:

                df_animal_milk = (
                    df_animal_milk.sort_values(by=["lactation_id", "dim"])
                    .reset_index(drop=True)
                    .groupby(by=["lactation_id"])
                    .apply(correct_first_mi)
                    .reset_index(drop=True)
                )
                df_animal_milk.loc[df_animal_milk.mi == 48] = None

                for lacids in list(
                    df_animal_lac.sort_values(by=["animal_id", "parity"]).lactation_id
                ):
                    calvingdate = (
                        df_animal_lac.loc[
                            df_animal_lac.lactation_id == lacids, "calving"
                        ]
                        .apply(pd.to_datetime)
                        .values[0]
                    )
                    lacno = df_animal_lac.loc[
                        df_animal_lac.lactation_id == lacids, "parity"
                    ].values[0]
                    df_animal_milk_uncorr.loc[
                        (df_animal_milk_uncorr.ended_at >= calvingdate),
                        "calvingdate",
                    ] = calvingdate
                    df_animal_milk_uncorr.loc[
                        (df_animal_milk_uncorr.ended_at >= calvingdate),
                        "parity",
                    ] = lacno

                # Create a figure with two subplots
                fig, axes = plt.subplots(2, 1, figsize=(21, 10), sharex=True)

                # Plot the scatterplot for df_animal_milk_daily
                sns.scatterplot(
                    data=df_animal_milk,
                    x="ended_at",
                    y="tmy_prod",
                    hue="parity",
                    ax=axes[0],
                )
                axes[0].set_title(
                    f"Animal_id={ani_id};Daily milk yield - corrected lactation information"
                )

                # Add horizontal lines for birth date and calving dates in the upper graph
                axes[0].axvline(
                    pd.to_datetime(df_animal_lac_corr["birth_date"].iloc[0]),
                    color="red",
                    linestyle="--",
                    label="Birth Date",
                )
                for i, calving_date in enumerate(df_animal_lac_corr["calving"]):
                    label = "Calving Date" if i == 0 else None
                    axes[0].axvline(
                        pd.to_datetime(calving_date),
                        color="blue",
                        linestyle="--",
                        label=label,
                    )

                # Plot the scatterplot for df_animal_milk_daily_uncorr
                sns.scatterplot(
                    data=df_animal_milk_uncorr,
                    x="ended_at",
                    y="tmy_prod",
                    hue="parity",
                    ax=axes[1],
                )
                axes[1].set_title(
                    f"Animal_id={ani_id};Daily milk yield - not-corrected lactation information"
                )

                # Add horizontal lines for birth date and calving dates in the lower graph
                axes[1].axvline(
                    pd.to_datetime(df_animal_lac_corr["birth_date"].iloc[0]),
                    color="red",
                    linestyle="--",
                    label="Birth Date",
                )
                for i, calving_date in enumerate(df_animal_lac["calving"]):
                    label = "Calving Date" if i == 0 else None
                    axes[1].axvline(
                        pd.to_datetime(calving_date),
                        color="blue",
                        linestyle="--",
                        label=label,
                    )

                # Customize the plots
                for ax in axes:
                    ax.set_xlabel("Date")
                    ax.set_ylabel("TMY_PROD")
                    ax.legend()

                # Show the plots
                plt.tight_layout()
                plt.savefig(
                    outdir_animal_level / f"{ani_id}_lactation_overview.png"
                )
                plt.close(fig=fig)

    ####################################################################################################################
    # Step 2: Extract data for the milking table, and additional time series data where applicable

    sqlscript = f"SELECT farm_id, animal_id, lactation_id, milking_system_id, parity, ended_at, dim, mi, tmy, mylf, myrf, mylr, myrr, eclf, ecrf, eclr, ecrr FROM milking WHERE farm_id={farm_id}"
    df_milking = dbconn.query(query=sqlscript)

    sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, dim, type_measurement, raw, smooth FROM milkbiomarkers WHERE farm_id={farm_id}"
    df_milkbiomarkers = dbconn.query(query=sqlscript)

    sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, dim, activity_total, rumination_acc, rumination_time FROM activity WHERE farm_id={farm_id}"
    df_activity = dbconn.query(query=sqlscript)

    sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, dim, bcs_value FROM bcs WHERE farm_id={farm_id}"
    df_bcs = dbconn.query(query=sqlscript)

    ####################################################################################################################
    # Plot histograms of the available values

    df_milking_filtered = (
        df_milking.sort_values(by=["lactation_id", "dim"])
        .reset_index(drop=True)
        .groupby(by=["lactation_id"])
        .apply(correct_first_mi)
        .reset_index(drop=True)
    )
    df_milking_filtered.loc[df_milking_filtered.mi == 48] = None

    # Create a figure with subplots for df_milking
    fig1, axes1 = plt.subplots(2, 2, figsize=(18, 12))
    fig1.suptitle("Milking Data")

    # Plot the remaining columns
    remaining_columns = ["mi", "tmy"]
    for ax, col in zip(axes1[0, :], remaining_columns):
        sns.violinplot(
            data=df_milking_filtered if col == "mi" else df_milking,
            y=col,
            ax=ax,
            inner="quartile",
        )
        # Sample 5% of the data for the swarmplot
        total_data_points = len(df_milking_filtered if col == "mi" else df_milking)
        sampled_data = (df_milking_filtered if col == "mi" else df_milking).sample(
            frac=100 / total_data_points, random_state=1
        )
        sns.swarmplot(data=sampled_data, y=col, ax=ax, color=".25", size=2)
        ax.set_title(f"{col} (Total: {total_data_points})")
        # Add horizontal line for thresholds
        ax.axhline(y=thresholds[col], color="r", linestyle="--")

    # Define combined columns for my and ec values
    my_columns = ["mylf", "myrf", "mylr", "myrr"]
    ec_columns = ["eclf", "ecrf", "eclr", "ecrr"]

    # Melt the DataFrame for my and ec values
    df_my_melted = df_milking.melt(
        value_vars=my_columns, var_name="Quarter", value_name="my"
    )
    df_ec_melted = df_milking.melt(
        value_vars=ec_columns, var_name="Quarter", value_name="ec"
    )

    # Plot the combined my values
    sns.violinplot(
        data=df_my_melted,
        x="Quarter",
        y="my",
        ax=axes1[1, 0],
        inner="quartile",
    )
    # Sample 5% of the data for the swarmplot
    total_data_points_my = len(df_my_melted)
    sampled_data = df_my_melted.sample(frac=100 / total_data_points_my, random_state=1)
    sns.swarmplot(data=sampled_data, x="Quarter", y="my", ax=axes1[1, 0], color=".25", size=2)
    axes1[1, 0].set_title(f"Quarter-level MY values (Total: {total_data_points_my})")
    # Add horizontal line for quarter-level my threshold
    axes1[1, 0].axhline(y=thresholds["qlmy"], color="r", linestyle="--")

    # Plot the combined ec values
    sns.violinplot(
        data=df_ec_melted,
        x="Quarter",
        y="ec",
        ax=axes1[1, 1],
        inner="quartile",
    )
    # Sample 5% of the data for the swarmplot
    total_data_points_ec = len(df_ec_melted)
    sampled_data = df_ec_melted.sample(frac=100 / total_data_points_ec, random_state=1)
    sns.swarmplot(data=sampled_data, x="Quarter", y="ec", ax=axes1[1, 1], color=".25", size=2)
    axes1[1, 1].set_title(f"Quarter-level EC values (Total: {total_data_points_ec})")
    # Add horizontal line for quarter-level ec threshold
    axes1[1, 1].axhline(y=thresholds["qlec"], color="r", linestyle="--")

    # Adjust layout
    plt.tight_layout()
    plt.savefig(outdir_data_overview / f"milking_data_overview.png")
    plt.close(fig=fig1)

    # List of DataFrames and their corresponding columns to plot
    additional_data = [
        (
            df_milkbiomarkers.loc[
                df_milkbiomarkers.type_measurement == 1, ["raw", "smooth"]
            ],
            "BHB",
        ),
        (
            df_milkbiomarkers.loc[
                df_milkbiomarkers.type_measurement == 2, ["raw", "smooth"]
            ],
            "P4",
        ),
        (
            df_milkbiomarkers.loc[
                df_milkbiomarkers.type_measurement == 3, ["raw", "smooth"]
            ],
            "LDH",
        ),
        (df_activity[["activity_total"]], "Activity Total"),
        (df_activity[["rumination_acc"]], "Rumination Acc"),
        (df_activity[["rumination_time"]], "Rumination Time"),
        (df_bcs[["bcs_value"]], "BCS Value"),
    ]

    # Filter out empty DataFrames
    non_empty_data = [(df, title) for df, title in additional_data if not df.empty]

    # Determine the layout based on the number of non-empty DataFrames
    num_plots = len(non_empty_data)
    if num_plots != 0:
        if num_plots == 1:
            rows = 1
            cols = 1
        elif num_plots == 2:
            rows = 1
            cols = 2
        elif num_plots == 3:
            rows = 1
            cols = 3
        elif num_plots == 4:
            rows = 2
            cols = 2
        elif num_plots == 5:
            rows = 2
            cols = 3
        elif num_plots == 6:
            rows = 2
            cols = 3
        elif num_plots == 7:
            rows = 2
            cols = 4

        # Create a figure with the appropriate number of subplots
        fig2, axes2 = plt.subplots(rows, cols, figsize=(6 * cols, 6 * rows))
        fig2.suptitle("Additional Data")

        # Flatten axes2 for easy iteration if it's a 2D array
        if num_plots > 1:
            axes2 = axes2.flatten()
        else:
            axes2 = [axes2]

        # Plot the violin plots for additional data
        for ax, (df, title) in zip(axes2, non_empty_data):
            if "raw" in df.columns and "smooth" in df.columns:
                sns.violinplot(
                    data=df.melt(var_name="Measurement", value_name="Value"),
                    x="Measurement",
                    y="Value",
                    ax=ax,
                    inner="quartile",
                )
                # Sample 5% of the data for the swarmplot
                total_data_points = len(df)
                sampled_data = df.melt(
                    var_name="Measurement", value_name="Value"
                ).sample(frac=100 / total_data_points, random_state=1)
                sns.swarmplot(
                    data=sampled_data, x="Measurement", y="Value", ax=ax, color=".25", size=2
                )
                ax.set_title(f"{title} (Total: {total_data_points})")
                # Add horizontal lines for thresholds if they exist
                if title in thresholds:
                    for threshold in thresholds[title]:
                        ax.axhline(y=threshold, color="r", linestyle="--")
            else:
                for col in df.columns:
                    sns.violinplot(data=df, y=col, ax=ax, inner="quartile")
                    # Sample 5% of the data for the swarmplot
                    total_data_points = len(df)
                    sampled_data = df.sample(
                        frac=100 / total_data_points, random_state=1
                    )
                    sns.swarmplot(data=sampled_data, y=col, ax=ax, color=".25", size=2)
                    ax.set_title(f"{title} (Total: {total_data_points})")
                    # Add horizontal line for thresholds if they exist
                    if title in thresholds:
                        for threshold in thresholds[title]:
                            ax.axhline(y=threshold, color="r", linestyle="--")

        # Remove any unused axes
        for ax in axes2[len(non_empty_data) :]:
            fig2.delaxes(ax)

        # Adjust layout
        plt.tight_layout()
        plt.savefig(outdir_data_overview / f"additional_data_overview.png")
        plt.close(fig=fig2)

        # Create a figure with the appropriate number of subplots
        fig3, axes2 = plt.subplots(rows, cols, figsize=(6 * cols, 6 * rows))
        fig3.suptitle("Additional Data")

        # Flatten axes2 for easy iteration if it's a 2D array
        if num_plots > 1:
            axes2 = axes2.flatten()
        else:
            axes2 = [axes2]

        # Plot the violin plots for additional data
        for ax, (df, title) in zip(axes2, non_empty_data):
            if "raw" in df.columns and "smooth" in df.columns:
                sns.violinplot(
                    data=df.melt(var_name="Measurement", value_name="Value"),
                    x="Measurement",
                    y="Value",
                    ax=ax,
                    inner="quartile",
                )
                # Sample 5% of the data for the swarmplot
                total_data_points = len(df)
                sampled_data = df.melt(
                    var_name="Measurement", value_name="Value"
                ).sample(frac=100 / total_data_points, random_state=1)
                sns.swarmplot(
                    data=sampled_data, x="Measurement", y="Value", ax=ax, color=".25", size=2
                )
                ax.set_title(f"{title} (Total: {total_data_points})")
                if title == "BHB":
                    ax.set_ylim(-0.05, 0.3)
                elif title == "LDH":
                    ax.set_ylim(-10, 150)
                # Add horizontal lines for thresholds if they exist
                if title in thresholds:
                    for threshold in thresholds[title]:
                        ax.axhline(y=threshold, color="r", linestyle="--")
            else:
                for col in df.columns:
                    sns.violinplot(data=df, y=col, ax=ax, inner="quartile")
                    # Sample 5% of the data for the swarmplot
                    total_data_points = len(df)
                    sampled_data = df.sample(
                        frac=100 / total_data_points, random_state=1
                    )
                    sns.swarmplot(data=sampled_data, y=col, ax=ax, color=".25", size=2)
                    ax.set_title(f"{title} (Total: {total_data_points})")
                    # Add horizontal line for thresholds if they exist
                    if title in thresholds:
                        for threshold in thresholds[title]:
                            ax.axhline(y=threshold, color="r", linestyle="--")

        # Remove any unused axes
        for ax in axes2[len(non_empty_data) :]:
            fig3.delaxes(ax)

        # Adjust layout
        plt.tight_layout()
        plt.savefig(outdir_data_overview / f"additional_data_overview_detailed.png")
        plt.close(fig=fig3)

    # Ensure 'ended_at' is in datetime format
    df_milking_filtered["ended_at"] = pd.to_datetime(df_milking_filtered["ended_at"])

    # Convert relevant columns to numeric types
    numeric_columns = ["eclf", "ecrf", "eclr", "ecrr"]
    df_milking_filtered[numeric_columns] = df_milking_filtered[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )

    # Group by 'milking_system_id' and resample data to daily frequency, then calculate the median
    grouped = df_milking_filtered.groupby("milking_system_id")

    # Create a new DataFrame to store the daily medians for all milking_system_ids
    daily_median_all = pd.DataFrame()

    for milking_system_id, group in grouped:
        daily_median = (
            group.resample("D", on="ended_at")[numeric_columns].median().reset_index()
        )
        daily_median["milking_system_id"] = milking_system_id
        daily_median_all = pd.concat(
            [daily_median_all, daily_median], ignore_index=True
        )

    # Create a figure with 4 subplots arranged vertically
    fig, axes = plt.subplots(4, 1, figsize=(21, 16), dpi=200, sharex=True)

    # Plot eclf vs ended_at (daily median) for all milking_system_ids
    sns.lineplot(
        ax=axes[0],
        x="ended_at",
        y="eclf",
        hue="milking_system_id",
        data=daily_median_all,
    )
    axes[0].set_ylabel("eclf")
    axes[0].set_title("Daily Median of eclf vs ended_at for all milking_system_ids")
    axes[0].legend(title="Milking System ID")

    # Plot ecrf vs ended_at (daily median) for all milking_system_ids
    sns.lineplot(
        ax=axes[1],
        x="ended_at",
        y="ecrf",
        hue="milking_system_id",
        data=daily_median_all,
    )
    axes[1].set_ylabel("ecrf")
    axes[1].set_title("Daily Median of ecrf vs ended_at for all milking_system_ids")
    axes[1].legend(title="Milking System ID")

    # Plot eclr vs ended_at (daily median) for all milking_system_ids
    sns.lineplot(
        ax=axes[2],
        x="ended_at",
        y="eclr",
        hue="milking_system_id",
        data=daily_median_all,
    )
    axes[2].set_ylabel("eclr")
    axes[2].set_title("Daily Median of eclr vs ended_at for all milking_system_ids")
    axes[2].legend(title="Milking System ID")

    # Plot ecrr vs ended_at (daily median) for all milking_system_ids
    sns.lineplot(
        ax=axes[3],
        x="ended_at",
        y="ecrr",
        hue="milking_system_id",
        data=daily_median_all,
    )
    axes[3].set_xlabel("ended_at")
    axes[3].set_ylabel("ecrr")
    axes[3].set_title("Daily Median of ecrr vs ended_at for all milking_system_ids")
    axes[3].legend(title="Milking System ID")

    # Adjust layout
    plt.tight_layout()
    plt.savefig(outdir_data_overview / f"ec_over_time.png")
    plt.close(fig=fig)

    ####################################################################################################################
    # Make a list of lactations that might contain faulty data

    # Select lactation_id from df_milking based on the specified conditions
    milking_lactation_ids = df_milking_filtered[
        ((df_milking_filtered["mi"] >= thresholds["mi"]))
        | (
            (df_milking_filtered["mi"] < thresholds["mi"])
            & (
                (df_milking_filtered["tmy"] > thresholds["tmy"])
                | (df_milking_filtered["mylf"] > thresholds["qlmy"])
                | (df_milking_filtered["myrf"] > thresholds["qlmy"])
                | (df_milking_filtered["mylr"] > thresholds["qlmy"])
                | (df_milking_filtered["myrr"] > thresholds["qlmy"])
                | (df_milking_filtered["eclf"] > thresholds["qlec"])
                | (df_milking_filtered["ecrf"] > thresholds["qlec"])
                | (df_milking_filtered["eclr"] > thresholds["qlec"])
                | (df_milking_filtered["ecrr"] > thresholds["qlec"])
            )
        )
    ]["lactation_id"].unique()

    # # Select lactation_id from df_milkbiomarkers based on the specified conditions
    # milkbiomarkers_lactation_ids = df_milkbiomarkers[
    #     (
    #         (df_milkbiomarkers["type_measurement"] == 1)
    #         & (df_milkbiomarkers["raw"] < thresholds["BHB"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["BHB"][1])
    #     )
    #     | (
    #         (df_milkbiomarkers["type_measurement"] == 2)
    #         & (df_milkbiomarkers["raw"] < thresholds["P4"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["P4"][1])
    #     )
    #     | (
    #         (df_milkbiomarkers["type_measurement"] == 3)
    #         & (df_milkbiomarkers["raw"] < thresholds["LDH"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["LDH"][1])
    #     )
    # ]["lactation_id"].unique()

    # # Combine the lists of lactation_id and remove duplicates
    # suspected_lactations = sorted(
    #     pd.unique(
    #         pd.concat(
    #             [
    #                 pd.Series(milking_lactation_ids),
    #                 pd.Series(milkbiomarkers_lactation_ids),
    #             ]
    #         )
    #     )
    # )

    suspected_lactations = sorted(pd.Series(milking_lactation_ids))

    ####################################################################################################################
    # Create time series plots of the lactation suspected

    if len(suspected_lactations) > 0:
        for lactation_id in suspected_lactations:
            parity = int(
                df_milking.loc[
                    (df_milking_filtered["lactation_id"] == lactation_id), "parity"
                ].unique()[0]
            )
            min_date = df_milking.loc[
                (df_milking_filtered["lactation_id"] == lactation_id), "ended_at"
            ].min()

            # Filter data for the current lactation_id
            df_milking_select = df_milking_filtered[
                (df_milking_filtered["lactation_id"] == lactation_id)
            ]

            df_milkbiomarkers_filtered = df_milkbiomarkers[
                df_milkbiomarkers["lactation_id"] == lactation_id
            ]
            df_activity_filtered = df_activity[
                df_activity["lactation_id"] == lactation_id
            ]
            df_bcs_filtered = df_bcs[df_bcs["lactation_id"] == lactation_id]

            # List of data and titles for subplots
            plot_data = [
                (df_milking_select[["dim", "tmy"]], "DIM vs TMY"),
                (
                    df_milking_select[["dim", "mylf", "myrf", "mylr", "myrr"]],
                    "DIM vs MYLF/MYRF/MYLR/MYRR",
                ),
                (
                    df_milking_select[["dim", "eclf", "ecrf", "eclr", "ecrr"]],
                    "DIM vs ECLF/ECRF/ECLR/ECRR",
                ),
                (df_milking_select[["dim", "mi"]], "DIM vs MI"),
                (
                    df_milkbiomarkers_filtered[
                        df_milkbiomarkers_filtered["type_measurement"] == 1
                    ][["dim", "raw", "smooth"]],
                    "BHB Raw/Smooth",
                ),
                (
                    df_milkbiomarkers_filtered[
                        df_milkbiomarkers_filtered["type_measurement"] == 2
                    ][["dim", "raw", "smooth"]],
                    "P4 Raw/Smooth",
                ),
                (
                    df_milkbiomarkers_filtered[
                        df_milkbiomarkers_filtered["type_measurement"] == 3
                    ][["dim", "raw", "smooth"]],
                    "LDH Raw/Smooth",
                ),
                (
                    df_activity_filtered[["dim", "activity_total"]],
                    "DIM vs Activity Total",
                ),
                (df_bcs_filtered[["dim", "bcs_value"]], "DIM vs BCS Value"),
            ]

            # Filter out empty DataFrames
            non_empty_plot_data = [
                (df, title) for df, title in plot_data if not df.empty
            ]

            # Determine the number of non-empty plots
            num_plots = len(non_empty_plot_data)

            # Create a figure with the appropriate number of subplots
            fig, axes = plt.subplots(
                num_plots, 1, figsize=(21, 3 * num_plots), sharex=True
            )
            fig.suptitle(
                f"Lactation ID: {lactation_id}, parity: {parity}, min_date: {min_date}"
            )

            # Flatten axes for easy iteration if it's a 2D array
            if num_plots > 1:
                axes = axes.flatten()
            else:
                axes = [axes]

            # Plot the data for each subplot
            for ax, (df, title) in zip(axes, non_empty_plot_data):
                if "raw" in df.columns and "smooth" in df.columns:
                    sns.scatterplot(
                        data=df.melt(
                            id_vars="dim", var_name="Measurement", value_name="Value"
                        ),
                        x="dim",
                        y="Value",
                        hue="Measurement",
                        ax=ax,
                    )
                    # if title == "BHB Raw/Smooth":
                    #     for threshold in thresholds["BHB"]:
                    #         ax.axhline(y=threshold, color="red", linestyle="--")
                    # elif title == "P4 Raw/Smooth":
                    #     for threshold in thresholds["P4"]:
                    #         ax.axhline(y=threshold, color="red", linestyle="--")
                    # elif title == "LDH Raw/Smooth":
                    #     for threshold in thresholds["LDH"]:
                    #         ax.axhline(y=threshold, color="red", linestyle="--")
                elif "mylf" in df.columns:
                    sns.scatterplot(
                        data=df.melt(
                            id_vars="dim", var_name="Measurement", value_name="Value"
                        ),
                        x="dim",
                        y="Value",
                        hue="Measurement",
                        ax=ax,
                    )
                    ax.axhline(y=thresholds["qlmy"], color="red", linestyle="--")
                elif "eclf" in df.columns:
                    sns.scatterplot(
                        data=df.melt(
                            id_vars="dim", var_name="Measurement", value_name="Value"
                        ),
                        x="dim",
                        y="Value",
                        hue="Measurement",
                        ax=ax,
                    )
                    ax.axhline(y=thresholds["qlec"], color="red", linestyle="--")
                else:
                    for col in df.columns[1:]:
                        sns.scatterplot(data=df, x="dim", y=col, ax=ax, label=col)
                        if col in thresholds:
                            ax.axhline(y=thresholds[col], color="red", linestyle="--")
                ax.set_title(title)
                ax.legend()

            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.savefig(outdir_lactation_level / f"{lactation_id}_time_series.png")
            plt.close(fig=fig)

            # # Reset variables to free up memory
            # del df_milking_select, df_milkbiomarkers_filtered, df_activity_filtered, df_bcs_filtered, plot_data, non_empty_plot_data, num_plots, fig, axes

    ####################################################################################################################

    # Calculate the number of unique animal_id and lactation_id in each DataFrame
    unique_animal_id_milking = df_milking_filtered["animal_id"].nunique()
    unique_lactation_id_milking = df_milking_filtered["lactation_id"].nunique()

    unique_animal_id_milkbiomarkers = df_milkbiomarkers["animal_id"].nunique()
    unique_lactation_id_milkbiomarkers = df_milkbiomarkers["lactation_id"].nunique()

    unique_animal_id_activity = df_activity["animal_id"].nunique()
    unique_lactation_id_activity = df_activity["lactation_id"].nunique()

    unique_animal_id_bcs = df_bcs["animal_id"].nunique()
    unique_lactation_id_bcs = df_bcs["lactation_id"].nunique()

    # Calculate the total number of measurements (length) for each DataFrame
    total_measurements_milking = len(df_milking)
    total_measurements_milkbiomarkers = len(df_milkbiomarkers)
    total_measurements_activity = len(df_activity)
    total_measurements_bcs = len(df_bcs)

    # Calculate the number of suspected errors in measurement per variable defined in thresholds
    suspected_errors_milking = {
        "mi": (df_milking_filtered["mi"] > thresholds["mi"]).sum(),
        "tmy": (df_milking_filtered["tmy"] > thresholds["tmy"]).sum(),
        "qlmy": sum(
            (df_milking_filtered[col] > thresholds["qlmy"]).sum()
            for col in ["mylf", "myrf", "mylr", "myrr"]
        ),
        "qlec": sum(
            (df_milking_filtered[col] > thresholds["qlec"]).sum()
            for col in ["eclf", "ecrf", "eclr", "ecrr"]
        ),
    }

    # suspected_errors_milkbiomarkers = {
    #     "BHB": (
    #         (df_milkbiomarkers["type_measurement"] == 1)
    #         & (df_milkbiomarkers["raw"] < thresholds["BHB"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["BHB"][1])
    #     ).sum(),
    #     "P4": (
    #         (df_milkbiomarkers["type_measurement"] == 2)
    #         & (df_milkbiomarkers["raw"] < thresholds["P4"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["P4"][1])
    #     ).sum(),
    #     "LDH": (
    #         (df_milkbiomarkers["type_measurement"] == 3)
    #         & (df_milkbiomarkers["raw"] < thresholds["LDH"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["LDH"][1])
    #     ).sum(),
    # }

    # Calculate the number of rows with no error measurements vs rows with 1 or more errors
    rows_with_errors_milking = df_milking_filtered[
        (df_milking_filtered["mi"] > thresholds["mi"])
        | (df_milking_filtered["tmy"] > thresholds["tmy"])
        | (df_milking_filtered[["mylf", "myrf", "mylr", "myrr"]] > thresholds["qlmy"]).any(
            axis=1
        )
        | (df_milking_filtered[["eclf", "ecrf", "eclr", "ecrr"]] > thresholds["qlec"]).any(
            axis=1
        )
    ].shape[0]

    # rows_with_errors_milkbiomarkers = df_milkbiomarkers[
    #     (
    #         (df_milkbiomarkers["type_measurement"] == 1)
    #         & (df_milkbiomarkers["raw"] < thresholds["BHB"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["BHB"][1])
    #     )
    #     | (
    #         (df_milkbiomarkers["type_measurement"] == 2)
    #         & (df_milkbiomarkers["raw"] < thresholds["P4"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["P4"][1])
    #     )
    #     | (
    #         (df_milkbiomarkers["type_measurement"] == 3)
    #         & (df_milkbiomarkers["raw"] < thresholds["LDH"][0])
    #         & (df_milkbiomarkers["raw"] > thresholds["LDH"][1])
    #     )
    # ].shape[0]

    # Create a DataFrame to store the overview
    data_overview = pd.DataFrame(
        {
            "DataFrame": ["df_milking", "df_milkbiomarkers", "df_activity", "df_bcs"],
            "Unique Animal ID": [
                unique_animal_id_milking,
                unique_animal_id_milkbiomarkers,
                unique_animal_id_activity,
                unique_animal_id_bcs,
            ],
            "Unique Lactation ID": [
                unique_lactation_id_milking,
                unique_lactation_id_milkbiomarkers,
                unique_lactation_id_activity,
                unique_lactation_id_bcs,
            ],
            "Total Measurements": [
                total_measurements_milking,
                total_measurements_milkbiomarkers,
                total_measurements_activity,
                total_measurements_bcs,
            ],
            "Suspected Errors (mi)": [suspected_errors_milking["mi"], None, None, None],
            "Suspected Errors (tmy)": [
                suspected_errors_milking["tmy"],
                None,
                None,
                None,
            ],
            "Suspected Errors (qlmy)": [
                suspected_errors_milking["qlmy"],
                None,
                None,
                None,
            ],
            "Suspected Errors (qlec)": [
                suspected_errors_milking["qlec"],
                None,
                None,
                None,
            ],
            # "Suspected Errors (BHB)": [
            #     None,
            #     suspected_errors_milkbiomarkers["BHB"],
            #     None,
            #     None,
            # ],
            # "Suspected Errors (P4)": [
            #     None,
            #     suspected_errors_milkbiomarkers["P4"],
            #     None,
            #     None,
            # ],
            # "Suspected Errors (LDH)": [
            #     None,
            #     suspected_errors_milkbiomarkers["LDH"],
            #     None,
            #     None,
            # ],
            "Rows with Errors": [
                rows_with_errors_milking,
                None,
                None,
                None,
            ],
            "Rows without Errors": [
                total_measurements_milking - rows_with_errors_milking,
                None,
                None,
                None,
            ],
        }
    )

    # Save the DataFrame as a CSV file
    data_overview.to_csv(outdir_data_overview / "data_overview.csv", index=False)

    ####################################################################################################################

    return suspected_animals, suspected_lactations



def data_selection(
    farm_id,
    cowbase_rootdir,
    exclude_animals,
    exclude_lactations,
    start_date=datetime.datetime(2010, 1, 1),
    end_date=datetime.date.today(),
    min_dim=5,
    at_least_dim=65,
    max_dim=400,
    max_gap=5,
    my_ec_cutoff=0.3,
    load_data=["bcs", "activity", "milkbiomarkers"],
):
    """
    Selection of time-series data based on previously defined animals/lactations to exclude + restrictions on milk yield data

    Parameters
    ----------
    farm_id : int
        The ID of the farm.
    cowbase_rootdir : str
        The root directory of the cowbase.
    exclude_animals : list
        List of animal IDs to exclude.
    exclude_lactations : list
        List of lactation IDs to exclude.
    start_date : datetime
        The start date for data selection.
    end_date : datetime
        The end date for data selection.
    min_dim : int
        Minimum DIM (Days in Milk).
    at_least_dim : int
        Minimum DIM for selection.
    max_dim : int
        Maximum DIM for selection.
    max_gap : int
        Maximum gap allowed in the data.
    remove_4wk_bf_dry_off : bool
        Whether to remove data 4 weeks before dry off.
    load_data : list
        List of data types to load.

    Returns
    -------
    dict
        A dictionary containing the selected data for each data type.
    """
    rootdir = Path(cowbase_rootdir)

    # initialize folder structure
    rootdir_cowbase = rootdir / "CowBase"
    rootdir_cowbase.mkdir(exist_ok=True, parents=True)

    dbconn = connCowBaseDB(rootdir_cowbase)

    exclude_animals_str = ", ".join(map(str, exclude_animals))
    exclude_lactations_str = ", ".join(map(str, exclude_lactations))

    sqlscript = f"""
    SELECT * FROM milking 
    WHERE farm_id = {farm_id}
    """

    if exclude_animals_str:
        sqlscript += f" AND animal_id NOT IN ({exclude_animals_str})"

    if exclude_lactations_str:
        sqlscript += f" AND lactation_id NOT IN ({exclude_lactations_str})"

    sqlscript += f"""
    AND started_at > '{start_date}' 
    AND ended_at < '{end_date}'
    """

    df_milking = dbconn.query(query=sqlscript)

    # Step 1: Select all lactation_id where there is data for at least dim <= min_dim and dim >= at_least_dim
    valid_lactations_lower = df_milking[(df_milking["dim"] <= min_dim)][
        "lactation_id"
    ].unique()
    valid_lactations_upper = df_milking[(df_milking["dim"] >= at_least_dim)][
        "lactation_id"
    ].unique()

    # Step 2: Select df_milking for these lactation_ids
    df_milking_filtered = df_milking[
        df_milking["lactation_id"].isin(valid_lactations_lower)
    ]
    df_milking_filtered = df_milking_filtered[
        df_milking_filtered["lactation_id"].isin(valid_lactations_upper)
    ]

    # Step 3: Remove dim > max_dim
    df_milking_filtered = df_milking_filtered[df_milking_filtered["dim"] < max_dim]

    # Step 4: Check for gaps between dim, for lactations where there is a gap >= max_gap, remove lactation from df_milking
    def check_gaps(group):
        group = group.sort_values("dim")
        gaps = group["dim"].diff().fillna(1)  # Fill the first diff with 1
        if gaps.max() >= max_gap:
            return pd.DataFrame()  # Return an empty DataFrame to exclude this lactation
        return group

    df_milking_filtered = (
        df_milking_filtered.groupby("lactation_id")
        .apply(check_gaps)
        .reset_index(drop=True)
    )


    df_milking_filtered = (
        df_milking_filtered.sort_values(by=["lactation_id", "dim"])
        .reset_index(drop=True)
        .groupby(by=["lactation_id"])
        .apply(correct_first_mi)
        .reset_index(drop=True)
    )

    df_milking_corrected = df_milking_filtered.copy()

    sqlscript = f"""
        SELECT milking_system_type FROM farm 
        WHERE farm_id = {farm_id}
    """
    farm_type = dbconn.query(query=sqlscript)

    if farm_type.milking_system_type[0] == "AMS delaval":
        df_milking_corrected = df_milking_corrected.sort_values(
            by=["lactation_id", "dim"]
        )

        # Define the columns and their corresponding incomplete sets
        columns_incomplete_sets = {
            "mylf": [1, 3, 5, 7, 9, 11, 13, 15],
            "myrf": [2, 3, 6, 7, 10, 11, 14, 15],
            "mylr": [4, 5, 6, 7, 12, 13, 14, 15],
            "myrr": [8, 9, 10, 11, 12, 13, 14, 15],
        }

        # Apply the function to each column
        for column, incomplete_set in columns_incomplete_sets.items():
            df_milking_corrected[f"{column}_corr"] = (
                df_milking_corrected.groupby("lactation_id")
                .apply(calculate_milk_corr, column, incomplete_set)
                .reset_index(level=0, drop=True)
            )

        # Calculate tmy_corr as the sum of the four quarter-level corrected milk yields
        df_milking_corrected["tmy_corr"] = (
            df_milking_corrected["mylf_corr"]
            + df_milking_corrected["myrf_corr"]
            + df_milking_corrected["mylr_corr"]
            + df_milking_corrected["myrr_corr"]
        )

    df_milking_corrected["eclf_corr"] = df_milking_corrected["eclf"]
    df_milking_corrected["ecrf_corr"] = df_milking_corrected["ecrf"]
    df_milking_corrected["eclr_corr"] = df_milking_corrected["eclr"]
    df_milking_corrected["ecrr_corr"] = df_milking_corrected["ecrr"]

    # Apply the condition to set exlf, exrf, exlr, and exrr to None if mylf, myrf, mylr, or myrr are less than my_ec_cutoff
    df_milking_corrected.loc[
        df_milking_corrected["mylf"] < my_ec_cutoff, "eclf_corr"
    ] = None
    df_milking_corrected.loc[
        df_milking_corrected["myrf"] < my_ec_cutoff, "ecrf_corr"
    ] = None
    df_milking_corrected.loc[
        df_milking_corrected["mylr"] < my_ec_cutoff, "eclr_corr"
    ] = None
    df_milking_corrected.loc[
        df_milking_corrected["myrr"] < my_ec_cutoff, "ecrr_corr"
    ] = None

    # Extract lactation_ids from df_milking_filtered
    filtered_lactation_ids = df_milking_corrected["lactation_id"].unique()
    filtered_lactation_ids_str = ", ".join(map(str, filtered_lactation_ids))

    # Load data for each entry in load_data
    data_dict = {"milking": df_milking_corrected}
    for data_type in load_data:
        sqlscript = f"""
        SELECT * FROM {data_type} 
        WHERE farm_id = {farm_id} 
        AND lactation_id IN ({filtered_lactation_ids_str})
        AND measured_on > '{start_date}' 
        AND measured_on < '{end_date}'
        """
        data_dict[data_type] = dbconn.query(query=sqlscript)

    return data_dict


def dailyMY(df_milking):
    """
    Converts raw SESSION milk yield data to standardized DAILY milk yield data
    + some data selection steps (outliers deleted)

    Parameters
    ----------
    df_milking : df
        raw data of one farm from the database containing variables
            * milking_id
            * farm_id
            * animal_id
            * lactation_id
            * parity
            * started_at
            * ended_at
            * mi
            * dim
            * tmy & qmy (mylf, myrf, mylr, myrr)
            * quarter ec (eclf, ecrf, eclr, ecrr)

    Yields
    ------
    df_milking_daily : df
        (daily milk yield) data of one farm containing variables
            * farm_id
            * animal_id
            * lactation_id
            * dim
            * tdmy
            * dmylf, dmyrf, dmylr, dmyrr

    Steps
    -----
        - calculate the proportion of the MI before and after midnight
        - assign that proportion of the MY to the current or previous day (at udder and quarter level)
        - sum the milk yields of each day
        - add 1 to the DIM to avoid problems with log later on
        - standardize by dividing by the sum of all MI assigned to the current day (to account for missing milkings)
        - calculate a 7 day rolling median of the TDMY: delete tdmy values that are lower than 1.5*the rolling median
        - delete observations with TDMY below 75 kg

    """

    # Kick out all entries where mi could not be calculated/was not recorded.
    # This might lead to loss of information, creating a
    # total daily milk yield though would have large deviations if the mi was not guessed correctly.
    df_milking = df_milking.sort_values(
        by=["farm_id", "animal_id", "lactation_id", "milking_id"]
    ).reset_index(drop=True)
    milking = df_milking[df_milking["mi"].notna()].copy()

    # Floor dim for the calculation of daily milk yield
    milking["dim_floor"] = milking["dim"].apply(np.floor)

    # IV_dim_floor gives the time in hours at which the milking started at
    milking["IV_dim_floor"] = 24 * (milking["dim"] - milking["dim_floor"])

    # calculate the time between milkings that was during the previous day (compared to the dim floored)
    milking["mi_day_before"] = milking["mi"] - milking["IV_dim_floor"]
    # you put it to 0 because there was a previous milking on the same day
    milking.loc[milking["mi_day_before"] < 0, "mi_day_before"] = 0

    # calculate the time between milkings that was during the day (dim floored)
    milking["mi_on_day"] = milking["mi"] - milking["mi_day_before"]

    # calulate the proportions of mi on the day and day before
    milking["mi_day_before"] = milking["mi_day_before"] / milking["mi"]
    milking["mi_on_day"] = milking["mi_on_day"] / milking["mi"]

    # create a new table where the time between milkings was spread over two days
    MY_daily_add = milking.loc[milking["mi_day_before"] > 0].copy()

    # multiply the tmy in the first dataset (MY) with the mi in the day to get the propotion of milk yield 'produced' on that day
    # all parts of the milking session before midnight are set to 0. The only milk yields in THIS dataset, are from the sessions completely produced in the current day AND the proportion produced after midnight.
    milking["mi_day_before"] = 0
    milking["tmy"] = milking["tmy"] * milking["mi_on_day"]
    milking["mylf"] = milking["mylf"] * milking["mi_on_day"]
    milking["myrf"] = milking["myrf"] * milking["mi_on_day"]
    milking["mylr"] = milking["mylr"] * milking["mi_on_day"]
    milking["myrr"] = milking["myrr"] * milking["mi_on_day"]

    # multiply the tmy in the second dataset (df_milking_add) with the mi on the day before to get the propotion of milk yield 'produced' on the previous day
    # all complete milk sessions and the part of the milking interval after midnight, are equaled to 0. The only milk yields in THIS dataset are milk yields from the proportion before midnight.
    MY_daily_add["mi_on_day"] = 0
    # change the DIM to the DIM of the previous day (so later you will add this MY to the corresponding day - before midnight)
    MY_daily_add["dim_floor"] -= 1
    # if proportion of MI on the previous day is lower than 0, set equal to 0 (no milk yield assigned to the previous day)
    MY_daily_add.loc[MY_daily_add["dim_floor"] < 0, "dim_floor"] = 0
    MY_daily_add["tmy"] = MY_daily_add["tmy"] * MY_daily_add["mi_day_before"]
    MY_daily_add["mylf"] = MY_daily_add["mylf"] * MY_daily_add["mi_day_before"]
    MY_daily_add["myrf"] = MY_daily_add["myrf"] * MY_daily_add["mi_day_before"]
    MY_daily_add["mylr"] = MY_daily_add["mylr"] * MY_daily_add["mi_day_before"]
    MY_daily_add["myrr"] = MY_daily_add["myrr"] * MY_daily_add["mi_day_before"]

    # combine both tables and lose unnecessary information
    # df_milking contains the data of milking sessions of the current day (full MI on current day & proportion produced on current day of 'overnight' MI)
    # df_milking_add contains data of milking sessions of the previous day (proportion produced on previous day of 'overnight' MI)
    milking = pd.concat([milking, MY_daily_add])
    milking = milking[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "mi",
            "dim_floor",
            "tmy",
            "mylf",
            "myrf",
            "mylr",
            "myrr",
            "mi_day_before",
            "mi_on_day",
        ]
    ]
    del MY_daily_add

    # multiply the mi with the proportion of each day to get the true values of mi per period
    # In df_milking (contains current day info): mi_day_before is always 0, mi_on_day is either 1 (full MI on current day) or smaller than 1 (proportion produced on current day of 'overnight' MI)
    # In df_milking_add (contains previous day): mi_on_day is always 0, mi_day_before lies between 0 and 1 (proportion produced on previous day)
    milking["mi"] = milking["mi"] * (milking["mi_day_before"] + milking["mi_on_day"])

    # group by dim_floor to get the daily milk yields. Add all measurements to the assigned day
    MY_daily = milking.groupby(
        ["farm_id", "animal_id", "lactation_id", "parity", "dim_floor"], dropna=False
    ).sum()
    MY_daily.reset_index(inplace=True)
    MY_daily = MY_daily.rename(
        columns={
            "dim_floor": "dim",
            "tmy": "tdmy",
            "mylf": "dmylf",
            "myrf": "dmyrf",
            "mylr": "dmylr",
            "myrr": "dmyrr",
        }
    )
    del milking

    # add 1 to dim to avoid errors during the fitting process (allow any y offset, might cause problems if y=0 in some models)
    MY_daily["dim"] += 1

    # correct the milk yields to true daily milk yield by deviding through the mi for each my calculation and multiply by 24h (correct for missing data)
    MY_daily["tdmy"] = (MY_daily["tdmy"] / MY_daily["mi"]) * 24
    MY_daily["dmylf"] = (MY_daily["dmylf"] / MY_daily["mi"]) * 24
    MY_daily["dmyrf"] = (MY_daily["dmyrf"] / MY_daily["mi"]) * 24
    MY_daily["dmylr"] = (MY_daily["dmylr"] / MY_daily["mi"]) * 24
    MY_daily["dmyrr"] = (MY_daily["dmyrr"] / MY_daily["mi"]) * 24

    MY_daily = MY_daily[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "dim",
            "tdmy",
            "dmylf",
            "dmyrf",
            "dmylr",
            "dmyrr",
        ]
    ]

    # calculate a 7 day rolling median of the tdmy and select for tdmy values that are lower than
    # 1.5*the rolling median and below 75 kg daily milk yield
    MY_daily["tdmy7dm"] = MY_daily["tdmy"].rolling(7).median()
    MY_daily.loc[(MY_daily["dim"] < 7), "tdmy7dm"] = MY_daily.loc[
        (MY_daily["dim"] < 7), "tdmy"
    ]
    MY_daily = MY_daily[(MY_daily["tdmy"] < 1.5 * MY_daily["tdmy7dm"])]
    MY_daily = MY_daily[(MY_daily["tdmy"] < 75)]

    MY_daily = MY_daily[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "dim",
            "tdmy",
            "dmylf",
            "dmyrf",
            "dmylr",
            "dmyrr",
        ]
    ]

    return MY_daily


def dailyMY_single(dim, my, mi, ended_at):
    """
    Converts raw SESSION milk yield data to standardized DAILY milk yield data
    and performs data selection steps to remove outliers.

    Parameters
    ----------
    dim : array-like
        Days in milk for each milking session.
    my : array-like
        Milk yield for each milking session.
    mi : array-like
        Milking interval for each milking session.
    ended_at : array-like
        End time for each milking session.

    Returns
    -------
    df_milking_daily : DataFrame
        Standardized daily milk yield data containing:
            * dim : Days in milk
            * dmy : Daily milk yield

    Steps
    -----
        - Filter out entries where milking interval (mi) is not available.
        - Calculate the proportion of the milking interval (mi) before and after midnight.
        - Assign the corresponding proportion of the milk yield (my) to the current or previous day.
        - Sum the milk yields for each day.
        - Add 1 to the days in milk (dim) to avoid issues with logarithmic transformations.
        - Standardize the daily milk yield by dividing by the sum of all milking intervals for the day.
        - Calculate a 7-day rolling median of the daily milk yield and remove outliers.
        - Remove observations with daily milk yield below 75 kg.
    """

    # Create DataFrame from input arrays
    df_milking = pd.DataFrame({"dim": dim, "my": my, "mi": mi, "ended_at": ended_at})

    # Filter out entries where milking interval (mi) is not available
    milking = df_milking[df_milking["mi"].notna()].copy()

    # Floor dim for the calculation of daily milk yield
    milking["dim_floor"] = milking["dim"].apply(np.floor)

    # Calculate the time in hours at which the milking started
    milking["IV_dim_floor"] = 24 * (milking["dim"] - milking["dim_floor"])

    # Calculate the time between milkings that was during the previous day
    milking["mi_day_before"] = milking["mi"] - milking["IV_dim_floor"]
    milking.loc[milking["mi_day_before"] < 0, "mi_day_before"] = 0

    # Calculate the time between milkings that was during the current day
    milking["mi_on_day"] = milking["mi"] - milking["mi_day_before"]

    # Calculate the proportions of mi on the current day and the previous day
    milking["mi_day_before"] = milking["mi_day_before"] / milking["mi"]
    milking["mi_on_day"] = milking["mi_on_day"] / milking["mi"]

    # Create a new DataFrame for milkings that span two days
    MY_daily_add = milking.loc[milking["mi_day_before"] > 0].copy()

    # Assign the proportion of milk yield to the current day
    milking["mi_day_before"] = 0
    milking["my"] = milking["my"] * milking["mi_on_day"]

    # Assign the proportion of milk yield to the previous day
    MY_daily_add["mi_on_day"] = 0
    MY_daily_add["dim_floor"] -= 1
    MY_daily_add.loc[MY_daily_add["dim_floor"] < 0, "dim_floor"] = 0
    MY_daily_add["my"] = MY_daily_add["my"] * MY_daily_add["mi_day_before"]

    # Combine both DataFrames and retain necessary columns
    milking = pd.concat([milking, MY_daily_add])
    milking = milking[["mi", "dim_floor", "my", "mi_day_before", "mi_on_day"]]
    del MY_daily_add

    # Calculate the true values of mi per period
    milking["mi"] = milking["mi"] * (milking["mi_day_before"] + milking["mi_on_day"])

    # Group by dim_floor to get the daily milk yields
    MY_daily = milking.groupby(["dim_floor"], dropna=False).sum()
    MY_daily.reset_index(inplace=True)
    MY_daily = MY_daily.rename(columns={"dim_floor": "dim", "my": "dmy"})
    del milking

    # Add 1 to dim to avoid errors during the fitting process
    MY_daily["dim"] += 1

    # Correct the milk yields to true daily milk yield
    MY_daily["dmy"] = (MY_daily["dmy"] / MY_daily["mi"]) * 24

    MY_daily = MY_daily[["dim", "dmy"]]

    # Calculate a 7-day rolling median of the daily milk yield and remove outliers
    MY_daily["dmy7dm"] = MY_daily["dmy"].rolling(7).median()
    MY_daily.loc[(MY_daily["dim"] < 7), "dmy7dm"] = MY_daily.loc[
        (MY_daily["dim"] < 7), "dmy"
    ]
    MY_daily = MY_daily[(MY_daily["dmy"] < 1.5 * MY_daily["dmy7dm"])]
    MY_daily = MY_daily[(MY_daily["dmy"] < 75)]

    MY_daily = MY_daily[["dim", "dmy"]]

    return MY_daily


def plot_lactation(
    cowbase_rootdir,
    lactation_id,
    data=["mi", "tmy", "qlmy", "ec", "bhb", "ldh", "p4", "activity", "bcs"],
    dim_lim=[0, 400],
    showfig=True,
    savefig=False,
):
    """
    Creating a plot of a full lactation given a certain lactation number.

    Parameters
    ----------
    cowbase_rootdir : str
        The root directory of the cowbase.
    lactation_id : int
        The ID of the lactation to plot.
    data : list, optional
        List of data types to include in the plot. Default is ["mi", "tmy", "qlmy", "ec", "bhb", "ldh", "p4", "activity", "bcs"].
    dim_lim : list, optional
        List containing the lower and upper limits for DIM (Days in Milk). Default is [0, 400].
    showfig : bool, optional
        Whether to display the figure. Default is True.
    savefig : bool, optional
        Whether to save the figure. Default is False.

    Returns
    -------
    None
    """
    ####################################################################################################################
    # Load required data
    rootdir = Path(cowbase_rootdir)

    # initialize folder structure
    rootdir_cowbase = rootdir / "CowBase"
    dbconn = connCowBaseDB(rootdir_cowbase)

    rootdir_individual_plots = rootdir_cowbase / "individual_plots"
    rootdir_individual_plots.mkdir(exist_ok=True)

    if "tmy" in data or "qlmy" in data or "ec" in data or "mi" in data:
        sqlscript = f"SELECT farm_id, animal_id, lactation_id, milking_system_id, parity, ended_at, dim, mi, tmy, mylf, myrf, mylr, myrr, eclf, ecrf, eclr, ecrr FROM milking WHERE lactation_id={lactation_id}"
        df_milking = dbconn.query(query=sqlscript)
        df_milking = df_milking.sort_values(by="dim").reset_index(drop=True)
        df_milking.loc[df_milking.index == 0, "mi"] = None

    if "bhb" in data or "ldh" in data or "p4" in data:
        sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, dim, type_measurement, raw, smooth FROM milkbiomarkers WHERE lactation_id={lactation_id}"
        df_milkbiomarkers = dbconn.query(query=sqlscript)

    if "activity" in data:
        sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, dim, activity_total, rumination_acc, rumination_time FROM activity WHERE lactation_id={lactation_id}"
        df_activity = dbconn.query(query=sqlscript)

    if "bcs" in data:
        sqlscript = f"SELECT farm_id, animal_id, lactation_id, parity, dim, bcs_value FROM bcs WHERE lactation_id={lactation_id}"
        df_bcs = dbconn.query(query=sqlscript)

    ####################################################################################################################

    parity = int(
        df_milking.loc[(df_milking["lactation_id"] == lactation_id), "parity"].unique()[
            0
        ]
    )
    min_date = df_milking.loc[
        (df_milking["lactation_id"] == lactation_id), "ended_at"
    ].min()

    # List of data and titles for subplots
    plot_data = []

    if "tmy" in data:
        plot_data.append((df_milking[["dim", "tmy"]], "DIM vs TMY"))

    if "qlmy" in data:
        plot_data.append(
            (
                df_milking[["dim", "mylf", "myrf", "mylr", "myrr"]],
                "DIM vs MYLF/MYRF/MYLR/MYRR",
            )
        )

    if "ec" in data:
        plot_data.append(
            (
                df_milking[["dim", "eclf", "ecrf", "eclr", "ecrr"]],
                "DIM vs ECLF/ECRF/ECLR/ECRR",
            )
        )

    if "mi" in data:
        plot_data.append((df_milking[["dim", "mi"]], "DIM vs MI"))

    if "bhb" in data:
        plot_data.append(
            (
                df_milkbiomarkers[df_milkbiomarkers["type_measurement"] == 1][
                    ["dim", "raw", "smooth"]
                ],
                "BHB Raw/Smooth",
            )
        )

    if "p4" in data:
        plot_data.append(
            (
                df_milkbiomarkers[df_milkbiomarkers["type_measurement"] == 2][
                    ["dim", "raw", "smooth"]
                ],
                "P4 Raw/Smooth",
            )
        )

    if "ldh" in data:
        plot_data.append(
            (
                df_milkbiomarkers[df_milkbiomarkers["type_measurement"] == 3][
                    ["dim", "raw", "smooth"]
                ],
                "LDH Raw/Smooth",
            )
        )

    if "activity" in data:
        plot_data.append(
            (df_activity[["dim", "activity_total"]], "DIM vs Activity Total")
        )

    if "bcs" in data:
        plot_data.append((df_bcs[["dim", "bcs_value"]], "DIM vs BCS Value"))

    # Filter out empty DataFrames
    non_empty_plot_data = [(df, title) for df, title in plot_data if not df.empty]

    # Determine the number of non-empty plots
    num_plots = len(non_empty_plot_data)

    # Create a figure with the appropriate number of subplots
    fig, axes = plt.subplots(num_plots, 1, figsize=(21, 3 * num_plots), sharex=True)
    fig.suptitle(
        f"Lactation ID: {lactation_id}, parity: {parity}, min_date: {min_date}"
    )

    # Flatten axes for easy iteration if it's a 2D array
    if num_plots > 1:
        axes = axes.flatten()
    else:
        axes = [axes]

    # Plot the data for each subplot
    for ax, (df, title) in zip(axes, non_empty_plot_data):
        if "raw" in df.columns and "smooth" in df.columns:
            sns.scatterplot(
                data=df.melt(id_vars="dim", var_name="Measurement", value_name="Value"),
                x="dim",
                y="Value",
                hue="Measurement",
                ax=ax,
            )
        elif "mylf" in df.columns:
            sns.scatterplot(
                data=df.melt(id_vars="dim", var_name="Measurement", value_name="Value"),
                x="dim",
                y="Value",
                hue="Measurement",
                ax=ax,
            )
        elif "eclf" in df.columns:
            sns.scatterplot(
                data=df.melt(id_vars="dim", var_name="Measurement", value_name="Value"),
                x="dim",
                y="Value",
                hue="Measurement",
                ax=ax,
            )
        else:
            for col in df.columns[1:]:
                sns.scatterplot(data=df, x="dim", y=col, ax=ax, label=col)
        ax.set_xlim(dim_lim[0], dim_lim[1])
        ax.set_title(title)
        ax.legend()

    if showfig == True:
        plt.show()

    if savefig == True:
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(rootdir_individual_plots / f"{lactation_id}_time_series.png")
        plt.close(fig=fig)

    # Reset variables to free up memory
    del df_milking, df_milkbiomarkers, df_activity, df_bcs, plot_data, non_empty_plot_data, num_plots, fig, axes

    return


def wood(x, params):
    """
    Wood's Model: y = a * x^b * exp(-c * x)

    Parameters
    ----------
    x : array-like
        Days in milk (DIM).
    params : list
        Model parameters [a, b, c].

    Returns
    -------
    array-like
        Predicted milk yield.
    """
    a, b, c = params
    return a * np.power(x, b) * np.exp(-c * x)


def wilmink(x, params):
    """
    Wilmink Model: y = a + b * x + c * exp(-d * x)

    Parameters
    ----------
    x : array-like
        Days in milk (DIM).
    params : list
        Model parameters [a, b, c, d].

    Returns
    -------
    array-like
        Predicted milk yield.
    """
    a, b, c, d = params
    return a + b * x + c * np.exp(-d * x)


def ali_schaeffer(x, params):
    """
    Ali and Schaeffer Model: y = a + b * x + c * log(x) + d * x^2

    Parameters
    ----------
    x : array-like
        Days in milk (DIM).
    params : list
        Model parameters [a, b, c, d].

    Returns
    -------
    array-like
        Predicted milk yield.
    """
    a, b, c, d = params
    return a + b * x + c * np.log(x) + d * np.power(x, 2)


def cobby_le_du(x, params):
    """
    Cobby and Le Du Model: y = a * (1 - exp(-b * x)) * exp(-c * x)

    Parameters
    ----------
    x : array-like
        Days in milk (DIM).
    params : list
        Model parameters [a, b, c].

    Returns
    -------
    array-like
        Predicted milk yield.
    """
    a, b, c = params
    return a * (1 - np.exp(-b * x)) * np.exp(-c * x)


def dijkstra(x, params):
    """
    Dijkstra Model: y = a * (x / b)^c * exp(-d * (x / b))

    Parameters
    ----------
    x : array-like
        Days in milk (DIM).
    params : list
        Model parameters [a, b, c, d].

    Returns
    -------
    array-like
        Predicted milk yield.
    """
    a, b, c, d = params
    return a * np.power(x / b, c) * np.exp(-d * (x / b))

def poppe(x, params):
    """
    Dijkstra Model: y = a + bx + cx**2 + dx**3 + ex**4

    Parameters
    ----------
    x : array-like
        Days in milk (DIM).
    params : list
        Model parameters [a, b, c, d].

    Returns
    -------
    array-like
        Predicted milk yield.
    """
    a, b, c, d, e = params
    return a + b*x + c*x**2 + d*x**3 + e*x**4

def curve_fit_daily(
    dim, my, model="wood", init_param=None, lowerB=None, upperB=None, dim_lim=305, ls_weighted=True
):
    """
    Curve fitting function.

    Parameters
    ----------
    dim : array-like
        Days in milk (DIM).
    my : array-like
        Milk yield.
    model : str
        Model name (wood, wilmink, ali_schaeffer, cobby_le_du, dijkstra).
    init_param : list, optional
        Initial parameters for the model.
    lowerB : list, optional
        Lower boundaries for the parameters.
    upperB : list, optional
        Upper boundaries for the parameters.

    Returns
    -------
    array-like
        Fitted model parameters.
    """
    df = pd.DataFrame({"x": dim, "y": my})
    df_select = df.loc[df.x <= dim_lim]

    if model == "wood":
        model_function = wood
        if init_param is None:
            init_param = [15, 0.25, 0.003]
        if lowerB is None:
            lowerB = [0, 0, 0]
        if upperB is None:
            upperB = [100, 5, 1]
    elif model == "wilmink":
        model_function = wilmink
        if init_param is None:
            init_param = [40, -0.1, -10, 0.06]
        if lowerB is None:
            lowerB = [0, -1, -20, 0]
        if upperB is None:
            upperB = [100, 1, 100, 1]
    elif model == "ali_schaeffer":
        model_function = ali_schaeffer
        if init_param is None:
            init_param = [20, -0.1, 5, 0.01]
        if lowerB is None:
            lowerB = [0, -1, -10, -0.1]
        if upperB is None:
            upperB = [100, 1, 10, 0.1]
    elif model == "cobby_le_du":
        model_function = cobby_le_du
        if init_param is None:
            init_param = [20, 0.1, 0.01]
        if lowerB is None:
            lowerB = [0, 0, 0]
        if upperB is None:
            upperB = [100, 1, 1]
    elif model == "dijkstra":
        model_function = dijkstra
        if init_param is None:
            init_param = [20, 50, 0.1, 0.01]
        if lowerB is None:
            lowerB = [0, 1, 0, 0]
        if upperB is None:
            upperB = [100, 100, 1, 1]
    elif model == "poppe":
        model_function = poppe
        if init_param is None:
            init_param = [50, 0.2, -0.001, 0.001, -0.001]
        if lowerB is None:
            lowerB = [0, 0, -np.inf, 0, -np.inf]
        if upperB is None:
            upperB = [np.inf, np.inf, 0, np.inf, 0]
    else:
        raise ValueError(f"Model '{model}' is not supported.")

    # Ensure initial parameters are within bounds
    init_param = np.clip(init_param, lowerB, upperB)

    xdata = df_select.x
    ydata = df_select.y

    # Create weights: 3x weight for the first 60 days
    sigma_values = np.ones_like(xdata)
    if ls_weighted == True:
        sigma_values[xdata <= 120] = 3 / 4
        sigma_values[xdata <= 20] = 1 / 3

    # Find initial fit of the model
    model_parameter, _ = curve_fit(
        lambda xdata, *params: model_function(xdata, params),
        xdata,
        ydata,
        p0=init_param,
        bounds=(lowerB, upperB),
        sigma=sigma_values,
        method="trf",
    )

    my_model = model_function(x=df.x, params=model_parameter)

    return my_model, model_parameter


def iterative_curve_fit_daily(
    dim,
    my,
    model="wood",
    init_param=None,
    lowerB=None,
    upperB=None,
    dim_lim=305,
    iter_max=20,
    rmse_thr=0.1,
):

    if model == "wood":
        model_function = wood
        if init_param is None:
            init_param = [15, 0.25, 0.003]
        if lowerB is None:
            lowerB = [0, 0, 0]
        if upperB is None:
            upperB = [100, 5, 1]
    elif model == "wilmink":
        model_function = wilmink
        if init_param is None:
            init_param = [40, -0.1, -10, 0.06]
        if lowerB is None:
            lowerB = [0, -1, -20, 0]
        if upperB is None:
            upperB = [100, 1, 100, 1]
    elif model == "ali_schaeffer":
        model_function = ali_schaeffer
        if init_param is None:
            init_param = [20, -0.1, 5, 0.01]
        if lowerB is None:
            lowerB = [0, -1, -10, -0.1]
        if upperB is None:
            upperB = [100, 1, 10, 0.1]
    elif model == "cobby_le_du":
        model_function = cobby_le_du
        if init_param is None:
            init_param = [20, 0.1, 0.01]
        if lowerB is None:
            lowerB = [0, 0, 0]
        if upperB is None:
            upperB = [100, 1, 1]
    elif model == "dijkstra":
        model_function = dijkstra
        if init_param is None:
            init_param = [20, 50, 0.1, 0.01]
        if lowerB is None:
            lowerB = [0, 1, 0, 0]
        if upperB is None:
            upperB = [100, 100, 1, 1]
    elif model == "poppe":
        model_function = poppe
        if init_param is None:
            init_param = [50, 0.2, -0.001, 0.001, -0.001]
        if lowerB is None:
            lowerB = [0, 0, -np.inf, 0, -np.inf]
        if upperB is None:
            upperB = [np.inf, np.inf, 0, np.inf, 0]
    else:
        raise ValueError(f"Model '{model}' is not supported.")

    df = pd.DataFrame({"x": dim, "y0": my})
    # Ensure initial parameters are within bounds
    init_param = np.clip(init_param, lowerB, upperB)
    df_select = df.loc[df.x <= dim_lim].copy()
    no_iter = 0
    rmse0 = 1000
    rmse1 = 1001
    lendata = len(df_select)
    list_model_parameter = []
    if lendata <= 50:
        print("Too little data to apply iterative fitting!")
        return

    while (lendata > 50) and (no_iter < iter_max) and ((rmse1 - rmse0) > rmse_thr):

        xdata = df_select.loc[~pd.isnull(df_select[f"y{no_iter}"]), "x"]
        ydata = df_select.loc[~pd.isnull(df_select[f"y{no_iter}"]), f"y{no_iter}"]

        # add to no_iter
        no_iter = no_iter + 1

        # Find initial fit of the model
        model_parameter, _ = curve_fit(
            lambda xdata, *params: model_function(xdata, params),
            xdata,
            ydata,
            p0=init_param,
            bounds=(lowerB, upperB),
            method="trf",
        )
        list_model_parameter.append(model_parameter)

        df_select.loc[:, f"my_model{no_iter}"] = model_function(
            x=xdata, params=model_parameter
        )

        df_select.loc[:, "my_residuals"] = (
            df_select[f"y{no_iter-1}"] - df_select[f"my_model{no_iter}"]
        )

        try:
            sd = huber(df_select.my_residuals)[1]  # robust sd
        except:
            sd = df_select.my_residuals.std()

        if no_iter == 1:
            df_select.loc[:, "my_threshold"] = (
                df_select[f"my_model{no_iter}"] - 0.6 * sd
            )  # threshold
        else:
            df_select.loc[:, "my_threshold"] = (
                df_select[f"my_model{no_iter}"] - 1.6 * sd
            )  # threshold

        df_select.loc[:, f"y{no_iter}"] = df_select[f"y{no_iter-1}"].copy()

        # find all residuals below threshold of 1.6*sd
        df_select.loc[
            (df_select.x > 7) & (df_select[f"y{no_iter}"] < df_select.my_threshold),
            f"y{no_iter}",
        ] = None
        # find all residuals below threshold of 1.6*sd
        df_select.loc[
            (df_select.x > 7) & (df_select[f"y{no_iter}"] < df_select.my_threshold),
            "my_residuals",
        ] = None

        # prepare iterative procedure
        rmse1 = rmse0
        rmse0 = np.sqrt((df_select.my_residuals.dropna() ** 2).mean())
        lendata = len(df_select.my_residuals.dropna())  # needs to be larger than 50

    my_model_final = model_function(x=df.x, params=model_parameter)

    return my_model_final, df_select, list_model_parameter


def qreg_model_daily(dim, my, model, quantile=0.5, dim_lim=305):
    """
    Quantile regression fitting function using scikit-learn.

    Parameters
    ----------
    dim : array-like
        Days in milk (DIM).
    my : array-like
        Milk yield.
    model : str
        Model name (wood, wilmink, poppe).
    quantile : float
        Quantile to be estimated.
    dim_lim : int
        Limit for days in milk (DIM).

    Returns
    -------
    array-like
        Fitted model parameters.
    """

    df = pd.DataFrame({"x": dim, "y": my})
    df["logy"] = np.log(df.y)
    df["logx"] = np.log(df.x)
    df["sqx"] = np.power(df.x, 2)
    df["x3"] = np.power(df.x, 3)
    df["x4"] = np.power(df.x, 4)
    df_select = df.loc[df.x <= dim_lim]

    if model == "wood":
        model_function = wood
        X = df_select[["logx", "x"]]
        y = df_select["logy"]
    elif model == "ali_schaeffer":
        model_function = ali_schaeffer
        X = df_select[["x", "logx", "sqx"]]
        y = df_select["y"]
    elif model == "poppe":
        model_function = poppe
        X = df_select[["x", "sqx", "x3", "x4"]]
        y = df_select["y"]
    else:
        raise ValueError(f"Model '{model}' is not supported.")

    # Fit the quantile regression model
    quantile_reg = QuantileRegressor(quantile=quantile, alpha=0)
    quantile_reg.fit(X, y)
    qreg_params = quantile_reg.coef_
    intercept = quantile_reg.intercept_

    if model == "wood":
        model_parameter = [
            np.exp(intercept),
            qreg_params[0],
            -qreg_params[1],
        ]
    elif model == "ali_schaeffer":
        model_parameter = [
            intercept,
            qreg_params[0],
            qreg_params[1],
            qreg_params[2]
        ]
    elif model == "poppe":
        model_parameter = [
            intercept,
            qreg_params[0],
            qreg_params[1],
            qreg_params[2],
            qreg_params[3],
        ]

    my_model = model_function(x=df.x, params=model_parameter)

    return my_model, model_parameter


def lreg_model_daily(dim, my, model, dim_lim=305):
    """
    Quantile regression fitting function.

    Parameters
    ----------
    dim : array-like
        Days in milk (DIM).
    my : array-like
        Milk yield.
    model : str
        Model name (wood, wilmink, ali_schaeffer, cobby_le_du, dijkstra).
    init_param : list, optional
        Initial parameters for the model.
    lowerB : list, optional
        Lower boundaries for the parameters.
    upperB : list, optional
        Upper boundaries for the parameters.

    Returns
    -------
    array-like
        Fitted model parameters.
    """

    df = pd.DataFrame({"x": dim, "y": my})
    df["logy"] = np.log(df.y)
    df["logx"] = np.log(df.x)
    df["sqx"] = np.power(df.x, 2)
    df_select = df.loc[df.x <= dim_lim]

    if model == "wood":
        model_function = wood
        model_function_qreg = "logy ~ 1 + logx + x"
    elif model == "ali_schaeffer":
        model_function = ali_schaeffer
        model_function_qreg = "y ~ 1 + x + logx + sqx"
    else:
        raise ValueError(f"Model '{model}' is not supported.")

    quantile_reg = smf.ols(formula=model_function_qreg, data=df_select)
    qreg_params = quantile_reg.fit().params

    if model == "wood":
        model_parameter = [
            np.exp(qreg_params["Intercept"]),
            qreg_params["logx"],
            -qreg_params["x"],
        ]
    elif model == "ali_schaeffer":
        model_parameter = [
            qreg_params["Intercept"],
            qreg_params["x"],
            qreg_params["logx"],
            qreg_params["sqx"],
        ]

    my_model = model_function(x=df.x, params=model_parameter)

    return my_model, qreg_params


def lreg_model_session(dim, my, mi, parity, model, dim_lim=305):
    """
    Quantile regression fitting function.

    Parameters
    ----------
    dim : array-like
        Days in milk (DIM).
    my : array-like
        Milk yield.
    model : str
        Model name (wood, wilmink, ali_schaeffer, cobby_le_du, dijkstra).
    init_param : list, optional
        Initial parameters for the model.
    lowerB : list, optional
        Lower boundaries for the parameters.
    upperB : list, optional
        Upper boundaries for the parameters.

    Returns
    -------
    array-like
        Fitted model parameters.
    """

    df = pd.DataFrame({"dim": dim, "my": my, "mi": mi, "parity": parity})

    # df = pd.DataFrame({"x1": df_single.dim, "x2": df_single.mi_diff_dim, "y": df_single.tmy})
    df = df.sort_values(by="dim").reset_index(drop=True)
    # df.loc[df.mi_diff_dim > 48, 'mi_diff_dim'] = None
    df["logmy"] = np.log(df.my)
    df["logdim"] = np.log(df.dim)
    df["logmi"] = np.log(df.mi)
    df["sqdim"] = np.power(df.dim, 2)
    df_select = df.loc[df.dim <= dim_lim]

    if model == "wood":
        model_function = wood
        model_function_lreg = "logmy ~ 1 + dim + logdim + logmi"
    elif model == "ali_schaeffer":
        model_function = ali_schaeffer
        model_function_lreg = "my ~ 1 + dim + logdim + sqdim + mi"
    else:
        raise ValueError(f"Model '{model}' is not supported.")

    quantile_reg = smf.ols(formula=model_function_lreg, data=df_select)
    lreg_params = quantile_reg.fit().params

    if model == "wood":
        model_parameter = [
            np.exp(lreg_params["Intercept"]),
            lreg_params["logdim"],
            -lreg_params["dim"],
            np.exp(lreg_params["logmi"]),
        ]
    elif model == "ali_schaeffer":
        model_parameter = [
            lreg_params["Intercept"],
            lreg_params["dim"],
            lreg_params["logdim"],
            lreg_params["sqdim"],
            lreg_params["mi"],
        ]
    if model == "wood":
        my_model = np.exp(
            lreg_params["Intercept"]
            + lreg_params["dim"] * df.dim
            + lreg_params["logdim"] * df.logdim
            + lreg_params["logmi"] * df.logmi
        )
    elif model == "ali_schaeffer":
        my_model = (
            lreg_params["Intercept"]
            + lreg_params["dim"] * df.dim
            + lreg_params["logdim"] * df.logdim
            + lreg_params["sqdim"] * df.sqdim
            + lreg_params["mi"] * df.mi
        )

    return my_model, model_parameter

def pert(dim, my, my_model, pert_threshold = 0.85):
    """
    definitions perturbations:
        - If less than 5 days below my_model
                                                        no perturbation         [pert_severity = 0]
        - If >= 5 and less than 10	days below my_model
                never < 0.85*my_model		                very mild perturbation  [pert_severity = 1]
                1 or 2 days < 0.85*my_model				    mild perturbation       [pert_severity = 2]
                3 or more days < 0.85*my_model				moderate perturbation   [pert_severity = 3]
        - If more than 10 days below my_model
                0, 1 or 2 days < 0.85*my_model			    mild perturbation       [pert_severity = 2]
                3 or more days,
                    never >3 successive days	        moderate perturbation   [pert_severity = 3]
                3 or more days,
                    at least once >3 successive days    severe perturbation     [pert_severity = 4]
    Parameters
    ----------
    dim : Array (dtype = float)
        Contains the DIM values of each milking session within one (quarter or udder level) lactation
    my : Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation
    my_model : Array (dtype = float)
        Contains the DMY values of each milking session within one (quarter or udder level) lactation (given by e.g.
        either the applied iterative wood model or the qreg model)

    Returns
    -------
    df : pd.DataFrame (dtype = float)
        Dataframe containing the input data, and
            "res" : residuals between the real data (dmy) and the model (my_model),
            "thres" : Threshold of 0.85*dmy, cutoff for perturbation definition,
            "pert_no" : Number of the perturbation in the lactation,
            "pert_dur" : Duration of each perturbation,
            "pert_low_count" : Count of days where the milk yield is below thres,
            "pert_severity" : Parameter defining the severity of the perturbation (description see above),

    """
    # create data frame and calculate model residuals
    df = pd.DataFrame({"dim": dim, "my": my, "mod": my_model})

    df["res"] = df["my"] - df["mod"]
    df["thres"] = df["mod"] * pert_threshold

    # find std robust of residual time series
    try:
        sd = huber(df["res"])[1]  # robust sd
    except:
        sd = df["res"].std()

    # find negative
    df["is_neg"] = 0
    df.loc[df["my"] < df["mod"], "is_neg"] = 1

    # find below 1.6*robust_std
    df["is_low"] = 0
    df.loc[df["my"] < df["thres"], "is_low"] = 1

    # Step 1: Identify where 'is_neg' changes from the previous row
    df["change"] = df["is_neg"].ne(df["is_neg"].shift()).astype(int)

    # Step 2: Group consecutive rows
    df["group"] = df["change"].cumsum()
    df.group = (df.group + 1) / 2
    df.loc[df["group"] % 2 == 0.5, "group"] = 0

    # Step 3: Number periods of consecutive ones
    # This step is slightly modified to keep the group numbers for consecutive ones
    # and reset numbering for periods where 'is_neg' is 0.
    df["pert_no"] = (df["group"] * df["is_neg"]).astype(int)

    # Step 3: Count consecutive '1's for each group and assign back to rows where 'is_neg' is 1
    df["pert_dur"] = (
        df.groupby("group")["is_neg"].transform("sum") * df["is_neg"]
    ).astype(int)

    # Cleanup: Remove temporary columns if no longer needed
    df.drop(["change", "group"], axis=1, inplace=True)

    # Step 1: Group by 'pert_no' and calculate the count of rows where 'is_low' == 1 for each group
    df["pert_low_count"] = df.groupby("pert_no")["is_low"].transform(
        lambda x: (x == 1).sum()
    )

    # Step 1: Identify sequences of consecutive days where 'is_low' == 1 within each 'pert_no'
    df["is_low_change"] = df["is_low"].ne(df["is_low"].shift()) | df["pert_no"].ne(
        df["pert_no"].shift()
    )
    df["is_low_seq"] = df["is_low_change"].cumsum()

    # Step 2: Count the length of each sequence where 'is_low' == 1
    df["is_low_seq_len"] = df.groupby("is_low_seq")["is_low"].transform("sum")

    # Step 3: Determine if each 'pert_no' has at least one sequence of 3 or more consecutive 'is_low' == 1
    df["has_3_consec_low"] = df.groupby("pert_no")["is_low_seq_len"].transform(
        lambda x: (x >= 3).any()
    )

    # Cleanup: Remove temporary columns if no longer needed
    df.drop(["is_low_change", "is_low_seq", "is_low_seq_len"], axis=1, inplace=True)

    df.loc[(df.pert_dur < 5), "pert_severity"] = 0
    df.loc[
        (df.pert_dur >= 5) & (df.pert_dur < 10) & (df.pert_low_count == 0),
        "pert_severity",
    ] = 1
    df.loc[
        (df.pert_dur >= 5)
        & (df.pert_dur < 10)
        & (df.pert_low_count >= 1)
        & (df.pert_low_count <= 2),
        "pert_severity",
    ] = 2
    df.loc[
        (df.pert_dur >= 5) & (df.pert_dur < 10) & (df.pert_low_count >= 3),
        "pert_severity",
    ] = 3
    df.loc[(df.pert_dur >= 10) & (df.pert_low_count <= 2), "pert_severity"] = 2
    df.loc[
        (df.pert_dur >= 10) & (df.pert_low_count >= 3) & (df.has_3_consec_low == False),
        "pert_severity",
    ] = 3
    df.loc[
        (df.pert_dur >= 10) & (df.pert_low_count >= 3) & (df.has_3_consec_low == True),
        "pert_severity",
    ] = 4

    # Cleanup: Remove temporary columns if no longer needed
    df.drop(["has_3_consec_low"], axis=1, inplace=True)

    df.pert_severity = df.pert_severity.astype(int)

    return df[
        [
            "dim",
            "my",
            "mod",
            "res",
            "thres",
            "pert_no",
            "pert_dur",
            "pert_low_count",
            "pert_severity",
        ]
    ]

def select_healthy_lac_dest_ec(
    df_milking, number_separated=9, number_eclim=9, ec_cutoff=1.15
):
    """
    Select healthy lactations based on destination and electrical conductivity (EC) criteria.

    This function filters the input dataframe to select lactations that meet specific criteria:
    1. Lactations with less than 9 consecutive days of separated milk.
    2. Lactations with no blocks of more than 9 consecutive measurements where the EC of any quarter
       is above a certain cutoff of the mean EC of the other three quarters.

    Parameters:
    df_milking (pd.DataFrame): DataFrame containing milking session data with the following columns:
        - milking_id
        - farm_id
        - animal_id
        - lactation_id
        - parity
        - started_at
        - dim (days in milk)
        - destination
        - eclf_corr (EC of left front quarter)
        - ecrf_corr (EC of right front quarter)
        - eclr_corr (EC of left rear quarter)
        - ecrr_corr (EC of right rear quarter)

    Returns:
    pd.DataFrame: Filtered DataFrame containing only the healthy lactations.
    """

    # Filter sessions with DIM (days in milk) <= 305
    sessionMY = df_milking.loc[df_milking["dim"] <= 305].reset_index(drop=True)

    # Remove rows with missing essential columns
    sessionMY = sessionMY.dropna(
        subset=[
            "milking_id",
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "started_at",
        ]
    ).reset_index(drop=True)

    # Sort by lactation_id and DIM
    sessionMY = sessionMY.sort_values(by=["lactation_id", "dim"])

    if len(sessionMY.loc[~pd.isnull(sessionMY.destination)]) > 0:
        # SELECTION BASED ON CONSECUTIVE DAYS OF SEPARATED MILK (DESTINATION)
        # Mark separated milkings
        sessionMY.loc[sessionMY.destination != 1, "separated"] = 1
        sessionMY.loc[sessionMY.destination == 1, "separated"] = 0

        # Identify blocks of consecutive separated milkings
        sessionMY["block_of_n_separated"] = (
            sessionMY.destination.groupby(
                [sessionMY.lactation_id, sessionMY.separated.diff().ne(0).cumsum()]
            )
            .transform("size")
            .ge(number_separated)
            .astype(int)
        )
        sessionMY.loc[sessionMY.destination == 1, "block_of_n_separated"] = 0

        # List lactations with blocks of separated milkings
        list_lac_seperated = sessionMY.loc[
            sessionMY["block_of_n_separated"] == 1, "lactation_id"
        ].unique()
    else:
        list_lac_seperated = []

    # Remove lactations with blocks of separated milkings
    sessionMY_remsep = sessionMY.loc[
        ~sessionMY.lactation_id.isin(list_lac_seperated)
    ].copy()

    # SELECTION BASED ON INTERQUARTILE RATIO OF ELECTRICAL CONDUCTIVITY
    # Calculate EC cutoff for each quarter
    sessionMY_remsep["meanrr_eccutoff"] = ec_cutoff * sessionMY_remsep[
        ["eclf_corr", "ecrf_corr", "eclr_corr"]
    ].mean(axis=1, skipna=True)
    sessionMY_remsep["meanlr_eccutoff"] = ec_cutoff * sessionMY_remsep[
        ["eclf_corr", "ecrf_corr", "ecrr_corr"]
    ].mean(axis=1, skipna=True)
    sessionMY_remsep["meanrf_eccutoff"] = ec_cutoff * sessionMY_remsep[
        ["eclf_corr", "eclr_corr", "ecrr_corr"]
    ].mean(axis=1, skipna=True)
    sessionMY_remsep["meanlf_eccutoff"] = ec_cutoff * sessionMY_remsep[
        ["ecrf_corr", "eclr_corr", "ecrr_corr"]
    ].mean(axis=1, skipna=True)

    # Identify measurements where EC of any quarter is above the cutoff
    sessionMY_remsep.loc[
        (sessionMY_remsep["ecrr_corr"] > sessionMY_remsep["meanrr_eccutoff"])
        | (sessionMY_remsep["eclr_corr"] > sessionMY_remsep["meanlr_eccutoff"])
        | (sessionMY_remsep["ecrf_corr"] > sessionMY_remsep["meanrf_eccutoff"])
        | (sessionMY_remsep["eclf_corr"] > sessionMY_remsep["meanlf_eccutoff"]),
        "above_mean_EC",
    ] = 1
    sessionMY_remsep.loc[
        (sessionMY_remsep["ecrr_corr"] <= sessionMY_remsep["meanrr_eccutoff"])
        & (sessionMY_remsep["eclr_corr"] <= sessionMY_remsep["meanlr_eccutoff"])
        & (sessionMY_remsep["ecrf_corr"] <= sessionMY_remsep["meanrf_eccutoff"])
        & (sessionMY_remsep["eclf_corr"] <= sessionMY_remsep["meanlf_eccutoff"]),
        "above_mean_EC",
    ] = 0

    # Identify blocks of consecutive measurements with above mean EC
    sessionMY_remsep["block_of_n_outlierQEC"] = (
        sessionMY_remsep.above_mean_EC.groupby(
            [
                sessionMY_remsep.lactation_id,
                sessionMY_remsep.above_mean_EC.diff().ne(0).cumsum(),
            ]
        )
        .transform("size")
        .ge(number_eclim)
        .astype(int)
    )
    sessionMY_remsep.loc[
        sessionMY_remsep.above_mean_EC == 0, "block_of_n_outlierQEC"
    ] = 0

    # List lactations with blocks of above mean EC
    list_lac_ec = sessionMY_remsep.loc[
        sessionMY_remsep["block_of_n_outlierQEC"] == 1, "lactation_id"
    ].unique()

    # Remove lactations with blocks of above mean EC
    sessionMY_remsep_remec = sessionMY_remsep.loc[
        ~sessionMY_remsep.lactation_id.isin(list_lac_ec)
    ].copy()

    return sessionMY_remsep_remec, list_lac_seperated, list_lac_ec

def select_healthy_lac_my_pert(df_milking):

    healthy_lac = []
    healthy_qlac = []

    # Melt the DataFrame to separate tmy, mylf, myrf, mylr, myrr into milk_yield
    sessionMY_quarter = df_milking.melt(
        id_vars=[
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "started_at",
            "ended_at",
            "mi",
            "dim",
        ],
        value_vars=["tmy_corr", "mylf_corr", "myrf_corr", "mylr_corr", "myrr_corr"],
        var_name="quarter",
        value_name="my",
    )

    # Map the quarter names to their corresponding values
    quarter_map = {"tmy_corr": 99, "mylf_corr": 1, "myrf_corr": 2, "mylr_corr": 3, "myrr_corr": 4}
    sessionMY_quarter["quarter"] = sessionMY_quarter["quarter"].map(quarter_map)

    sessionMY_quarter = sessionMY_quarter.loc[~pd.isnull(sessionMY_quarter.lactation_id)]

    # Create the quarterlactation_id column
    sessionMY_quarter["quarterlactation_id"] = (
        sessionMY_quarter["lactation_id"].astype(int).astype(str)
        + sessionMY_quarter["quarter"].astype(int).astype(str).str.zfill(2)
    ).astype(int)

    for qlac_id in tqdm(sessionMY_quarter.quarterlactation_id.unique()):
        singleLacMY_session = sessionMY_quarter.loc[
            sessionMY_quarter.quarterlactation_id == qlac_id
        ].copy()
        singleLacMY_daily = dailyMY_single(
            singleLacMY_session.dim,
            singleLacMY_session.my,
            singleLacMY_session.mi,
            singleLacMY_session.ended_at,
        )
        quarter = singleLacMY_session.quarter.unique().astype(int)
        if len(singleLacMY_daily) < 100:
            continue
        if quarter <= 4:
            init_param = [10, 0.25, 0.003]
            lowerB = [0, 0, 0]
            upperB = [40, 2, 1]
        else:
            init_param = [15, 0.25, 0.003]
            lowerB = [0, 0, 0]
            upperB = [100, 5, 1]
        my_model, _ = curve_fit_daily(
            singleLacMY_daily.dim,
            singleLacMY_daily.dmy,
            model="wood",
            init_param=init_param,
            lowerB=lowerB,
            upperB=upperB,
            dim_lim=305,
        )
        singleLacMY_daily["dmy_pred"] = my_model
        pert_results = pert(
            singleLacMY_daily.dim,
            singleLacMY_daily.dmy,
            singleLacMY_daily.dmy_pred,
            pert_threshold=0.8,
        )
        if pert_results.pert_severity.max() < 4:
            if quarter <= 4:
                healthy_qlac.append(qlac_id)
            else:
                healthy_lac.append(qlac_id)
    return sessionMY_quarter, healthy_lac, healthy_qlac

def fixed_effect_estimation(df_milking, level):

    # Sort by quarterlactation_id and dim
    df_milking = df_milking.sort_values(by=["quarterlactation_id", "dim"]).reset_index(drop=True)

    # Add pmi column by shifting mi within each quarterlactation_id group
    df_milking['pmi'] = df_milking.groupby('quarterlactation_id')['mi'].shift(1)


    data = df_milking[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "quarterlactation_id",
            "parity",
            "started_at",
            "ended_at",
            "mi",
            "pmi",
            "dim",
            "my",
            "quarter",
        ]
    ]

    # Add column with previous milking interval
    data = data.sort_values(by=["lactation_id", "dim"]).reset_index(drop=True)

    # Add necessary parameters - my
    data.loc[data.parity == 1, "lp"] = 1
    data.loc[data.parity > 1, "lp"] = 2

    data.loc[data.dim != 0, "logdim"] = np.log(data.loc[data.dim != 0, "dim"])
    data.loc[data.dim == 0, "logdim"] = np.nan

    data.loc[data.mi != 0, "logmi"] = np.log(data.loc[data.mi != 0, "mi"])
    data.loc[data.mi == 0, "logmi"] = np.nan

    data.loc[data.my != 0, "logmy"] = np.log(data.loc[data.my != 0, "my"] * 1000)
    data.loc[data.my == 0, "logmy"] = np.nan

    # Add necessary parameters - qmy
    if level == 1:
        data.loc[(data.quarter == 1) | (data.quarter == 2), "qp"] = 1
        data.loc[(data.quarter == 3) | (data.quarter == 4), "qp"] = 2

    # Create dataframe with summarizing information
    summary = pd.DataFrame(
        {
            "FarmN": data.farm_id.unique(),
            "NLac": [len(data[["farm_id", "lactation_id"]].drop_duplicates())],
            "Nmeas": [len(data)],
            "NmeasSel": [0],
            "NmeasProc": [0],
            "NDIM305": [0],
        }
    )

    summary.NDIM305 = len(data.loc[data.dim > 305])
    if level == 1:
        data_select = data.loc[
            (data.dim < 305)
            & (data.my > 0.25)
            & (data.mi > 4)
            & (data.mi < 24)
            & (data.pmi > 4)
            & (data.pmi < 24)
            & ~pd.isnull(data.logmi)
            & ~pd.isnull(data.my)
        ]
    elif level == 2:
        data_select = data.loc[
            (data.dim < 305)
            & (data.my > 1)
            & (data.mi > 4)
            & (data.mi < 24)
            & (data.pmi > 4)
            & (data.pmi < 24)
            & ~pd.isnull(data.logmi)
            & ~pd.isnull(data.my)
        ]

    summary.NmeasSel = len(data_select)
    summary.NmeasProc = summary.NmeasSel / summary.Nmeas

    ############################################################################
    # Step 1: define model
    ############################################################################
    if level == 1:
        formula = (
            "logmy ~ 1 + dim + logdim + logmi + lp*qp + dim:lp + logdim:qp + logmi:dim"
        )
        formula_re = "~ 1 + dim + logdim + logmi"
        formula_groups = "quarterlactation_id"

    elif level == 2:
        formula = "logmy ~ 1 + dim + logdim + logmi + lp + dim:lp + logmi:dim"
        formula_re = "~ 1 + dim + logdim + logmi"
        formula_groups = "quarterlactation_id"

    ############################################################################
    # Step 2: Fit model and save model parameters
    ############################################################################
    data_select.loc[:, "quarterlactation_id"] = data_select.loc[
        :, "quarterlactation_id"
    ].astype(object)
    data_select.loc[:, "lp"] = data_select.loc[:, "lp"].astype(object)

    if level == 1:
        data_select.loc[:, "qp"] = data_select.loc[:, "qp"].astype(object)

    data_select.loc[data_select.logdim < 0, "logdim"] = 0
    data_select.loc[data_select.dim < 0, "dim"] = 0

    lme_model = smf.mixedlm(
        formula, data_select, groups=data_select[formula_groups], re_formula=formula_re
    )
    lme_out = lme_model.fit()

    summary["LL"] = lme_out.llf
    summary["AIC"] = lme_out.aic

    data_select["my_fe"] = np.exp(lme_model.predict(lme_out.fe_params)) / 1000
    data_select["my_re"] = np.concatenate([np.dot(lme_model.exog_re_li[j], lme_out.random_effects[k]) for (j, k) in enumerate(lme_model.group_labels)])

    data_select["my_lmm"] = np.exp(lme_out.fittedvalues) / 1000
    data_select["my_res_lmm"] = data_select["my"] - data_select["my_lmm"]
    data_select["my_res_rel_lmm"] = data_select["my_res_lmm"] / data_select["my_lmm"] * 100

    summary["Rsq"] = r2_score(data_select["my"], data_select["my_lmm"])
    summary["RMSE"] = np.sqrt((data_select.my_res_lmm**2).mean())
    summary["MPE"] = data_select["my_res_rel_lmm"].mean()

    if level == 1:
        mixedlmresults_fe_ql = pd.DataFrame(
            data=[np.ravel(lme_out.fe_params)],
            columns=[
                "fe_1",
                "fe_2",
                "fe_3",
                "fe_4",
                "fe_5",
                "fe_6",
                "fe_7",
                "fe_8",
                "fe_9",
                "fe_10",
            ],
        )
        mixedlmresults_cov_ql = pd.DataFrame(
            data=[np.ravel(lme_out.cov_re)],
            columns=[
                "fe_cov_1",
                "fe_cov_2",
                "fe_cov_3",
                "fe_cov_4",
                "fe_cov_5",
                "fe_cov_6",
                "fe_cov_7",
                "fe_cov_8",
                "fe_cov_9",
                "fe_cov_10",
                "fe_cov_11",
                "fe_cov_12",
                "fe_cov_13",
                "fe_cov_14",
                "fe_cov_15",
                "fe_cov_16",
            ],
        )
    else:
        mixedlmresults_fe_ql = pd.DataFrame(
            data=[np.ravel(lme_out.fe_params)],
            columns=[
                "fe_1",
                "fe_2",
                "fe_3",
                "fe_4",
                "fe_5",
                "fe_6",
                "fe_7",
            ],
        )
        mixedlmresults_cov_ql = pd.DataFrame(
            data=[np.ravel(lme_out.cov_re)],
            columns=[
                "fe_cov_1",
                "fe_cov_2",
                "fe_cov_3",
                "fe_cov_4",
                "fe_cov_5",
                "fe_cov_6",
                "fe_cov_7",
                "fe_cov_8",
                "fe_cov_9",
                "fe_cov_10",
                "fe_cov_11",
                "fe_cov_12",
                "fe_cov_13",
                "fe_cov_14",
                "fe_cov_15",
                "fe_cov_16",
            ],
        )
    mixedlmresults_scale_ql = pd.DataFrame(
        data=[np.ravel(lme_out.scale)], columns=["fe_scale"]
    )

    df_lmm_fixed_effects = pd.DataFrame(
        {
            "lmm_fixed_effects_id": [
                datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            ],
            "farm_id": df_milking.farm_id.unique(),
            "fe_level": [level],
            "total_quarterlactations": [
                len(data.quarterlactation_id.unique())
            ],
            "created_on": [datetime.datetime.now()],
        }
    )
    df_lmm_fixed_effects = df_lmm_fixed_effects.join(mixedlmresults_fe_ql)
    df_lmm_fixed_effects = df_lmm_fixed_effects.join(mixedlmresults_cov_ql)
    df_lmm_fixed_effects = df_lmm_fixed_effects.join(mixedlmresults_scale_ql)

    return data_select, df_lmm_fixed_effects, summary

def p4_f1_return_to_cyclicity(p4_lactation):
    """
    Identify when a cow returns to cyclicity and ends her postpartum anestrus period.

    Parameters
    ----------
    p4_lactation : pd.DataFrame
        DataFrame of a single lactation of an individual cow with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'dim'
            - 'raw'
            - 'smooth'

    Returns
    -------
    pd.DataFrame
        DataFrame with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'return_to_cyclicity_dim'
    """
    # sort values based on dim
    data = p4_lactation.copy().sort_values(by=["dim"])

    # identify where the first time the smooth p4 concentration is >= 5 ng/mL
    data = data[data["smooth"] >= 5]
    return_to_cyclicity = (
        data[data["dim"] == data["dim"].min()][
            ["farm_id", "animal_id", "lactation_id", "parity", "dim"]
        ]
        .rename(columns={"dim": "return_to_cyclicity_dim"})
        .reset_index(drop=True)
    )

    return return_to_cyclicity


def p4_f2_estrus_detection(p4_lactation):
    """
    Identify when a cow is in estrus throughout her lactation.

    Parameters
    ----------
    p4_lactation : pd.DataFrame
        DataFrame of a single lactation of an individual cow with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'dim'
            - 'raw'
            - 'smooth'

    Returns
    -------
    pd.DataFrame
        DataFrame with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'estrus_number'
            - 'dim_at_estrus'
    """
    # sort values based on dim
    data = p4_lactation.copy().sort_values(by=["dim"])

    # identify where smooth p4 concentration is < 5 ng/mL after a period of luteal activity
    data["prev_smooth"] = data["smooth"].shift(1)  # get the previous smooth measurement
    estrus = data[(data["smooth"] < 5) & (data["prev_smooth"] >= 5)][
        ["farm_id", "animal_id", "lactation_id", "parity", "dim"]
    ].rename(columns={"dim": "dim_at_estrus"})
    # make an indication for estrus number
    estrus["indic"] = 1
    estrus["estrus_number"] = estrus["indic"].cumsum()
    estrus = estrus[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "estrus_number",
            "dim_at_estrus",
        ]
    ]

    return estrus


def p4_f3_interluteal_phase(p4_lactation, estrus):
    """
    Identify the length of the interluteal phase after every estrus throughout a cow's lactation.

    Parameters
    ----------
    p4_lactation : pd.DataFrame
        DataFrame of a single lactation of an individual cow with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'dim'
            - 'raw'
            - 'smooth'
    estrus : pd.DataFrame
        DataFrame with estrus detection information.

    Returns
    -------
    pd.DataFrame
        DataFrame with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'estrus_number'
            - 'dim_at_estrus'
            - 'end_interluteal'
            - 'start_interluteal'
            - 'interluteal_phase_length'
    """
    # sort values based on dim
    data = p4_lactation.copy().sort_values(by=["dim"])
    data_estrus = estrus.copy()

    data_estrus["next_estrus"] = data_estrus["dim_at_estrus"].shift(-1)
    # merge with data_estrus
    data = pd.merge(
        data_estrus,
        data,
        on=["farm_id", "animal_id", "lactation_id", "parity"],
        how="left",
    )
    # start interluteal = dim_at_estrus, end interluteal = the first time smooth >= 5 after an estrus
    data.loc[
        (data["smooth"] >= 5)
        & (data["dim"] > data["dim_at_estrus"])
        & ((data["dim"] < data["next_estrus"]) | (data["next_estrus"].isna())),
        "indic",
    ] = 1
    # now only keep where indic = 1 for every estrus number
    data = data[data["indic"] == 1]
    # now take the first dim of every dim_at_estrus group - this is your end interluteal
    end_interluteal = data.loc[data.groupby(["dim_at_estrus"])["dim"].idxmin()].rename(
        columns={"dim": "end_interluteal"}
    )

    interluteal_phase = end_interluteal[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "estrus_number",
            "dim_at_estrus",
            "end_interluteal",
        ]
    ].copy()
    interluteal_phase["start_interluteal"] = interluteal_phase["dim_at_estrus"].copy()
    interluteal_phase["interluteal_phase_length"] = (
        interluteal_phase["end_interluteal"] - interluteal_phase["start_interluteal"]
    )

    return interluteal_phase


def p4_f4_luteal_phase(p4_lactation, estrus):
    """
    Identify the length of the luteal phase after every estrus throughout a cow's lactation.

    Parameters
    ----------
    p4_lactation : pd.DataFrame
        DataFrame of a single lactation of an individual cow with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'dim'
            - 'raw'
            - 'smooth'
    estrus : pd.DataFrame
        DataFrame with estrus detection information.

    Returns
    -------
    pd.DataFrame
        DataFrame with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'estrus_number'
            - 'dim_at_estrus'
            - 'start_luteal'
            - 'end_luteal'
            - 'luteal_phase_length'
    """
    # sort values based on dim
    data = p4_lactation.copy().sort_values(by=["dim"])
    data_estrus = estrus.copy()
    data_estrus["next_estrus"] = data_estrus["dim_at_estrus"].shift(-1)
    # merge with data_estrus
    data = pd.merge(
        data_estrus,
        data,
        on=["farm_id", "animal_id", "lactation_id", "parity"],
        how="left",
    )
    # end_luteal = next_estrus, start_luteal = the first time smooth >= 5 after an estrus
    data.loc[
        (data["smooth"] >= 5)
        & (data["dim"] > data["dim_at_estrus"])
        & (data["dim"] < data["next_estrus"]),
        "indic",
    ] = 1
    # now only keep where indic = 1 for every estrus number
    data = data[data["indic"] == 1]
    # now take the first dim of every dim_at_estrus group - this is your start luteal
    start_luteal = data.loc[data.groupby(["dim_at_estrus"])["dim"].idxmin()].rename(
        columns={"dim": "start_luteal"}
    )

    luteal_phase = start_luteal[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "estrus_number",
            "dim_at_estrus",
            "next_estrus",
            "start_luteal",
        ]
    ]
    luteal_phase = luteal_phase.rename(columns={"next_estrus": "end_luteal"})
    luteal_phase["luteal_phase_length"] = (
        luteal_phase["end_luteal"] - luteal_phase["start_luteal"]
    )

    # also make sure that you get the first luteal phase after return to cyclicity
    data = p4_lactation.copy().sort_values(by=["dim"])
    # end_luteal = first estrus, start_luteal = the first time smooth >= 5 after return to cyclicity
    data = data[data["smooth"] >= 5]
    # now take the first dim because this is your first start_luteal
    first_luteal = data[data["dim"] == data["dim"].min()].rename(
        columns={"dim": "start_luteal"}
    )
    first_estrus = estrus[estrus["estrus_number"] == 1]
    first_luteal = pd.merge(
        first_luteal,
        first_estrus,
        on=["farm_id", "animal_id", "lactation_id", "parity"],
        how="outer",
    )
    first_luteal = first_luteal[
        [
            "farm_id",
            "animal_id",
            "lactation_id",
            "parity",
            "start_luteal",
            "dim_at_estrus",
        ]
    ].rename(columns={"dim_at_estrus": "end_luteal"})
    first_luteal["luteal_phase_length"] = (
        first_luteal["end_luteal"] - first_luteal["start_luteal"]
    )
    first_luteal["estrus_number"] = 0
    first_luteal["dim_at_estrus"] = np.nan

    luteal_phase = pd.concat([luteal_phase, first_luteal]).sort_values(
        by=["estrus_number"]
    )

    return luteal_phase


def p4_f5_visualisation_fertility_profile(
    p4_lactation, return_to_cyclicity, estrus, interluteal_phase, luteal_phase
):
    """
    Visualise the p4 profile of a single lactation of an individual cow.

    Parameters
    ----------
    p4_lactation : pd.DataFrame
        DataFrame of a single lactation of an individual cow with the columns:
            - 'farm_id'
            - 'animal_id'
            - 'lactation_id'
            - 'parity'
            - 'dim'
            - 'raw'
            - 'smooth'
    return_to_cyclicity : pd.DataFrame
        DataFrame with return to cyclicity information.
    estrus : pd.DataFrame
        DataFrame with estrus detection information.
    interluteal_phase : pd.DataFrame
        DataFrame with interluteal phase information.
    luteal_phase : pd.DataFrame
        DataFrame with luteal phase information.

    Returns
    -------
    None
    """

    # plot df for return_to_cyclicity
    plot_return_to_cyclicity = return_to_cyclicity.copy()
    plot_return_to_cyclicity["forplot"] = 0

    # plot df for estrus
    plot_estrus = estrus.copy()
    plot_estrus["forplot"] = 0

    # plot df for interluteal_phase
    plot_interluteal_phase = interluteal_phase.copy()
    # now create the plot df for luteal_phase
    plot_luteal_phase = luteal_phase.copy()

    # plot
    sns.set_style("whitegrid")
    # make the plot
    fig = plt.figure(figsize=(14.08, 7.08), dpi=600)
    ax = fig.add_subplot(111)
    # plot raw p4
    ax.plot(
        p4_lactation["dim"],
        p4_lactation["raw"],
        "D",
        color="#A9ACA9",
        ms=4,
        label="raw p4",
    )
    # plot smooth p4
    ax.plot(
        p4_lactation["dim"],
        p4_lactation["smooth"],
        "o-",
        color="#424B54",
        ms=6,
        label="smooth p4",
    )
    # plot return to cyclicity
    ax.plot(
        plot_return_to_cyclicity["return_to_cyclicity_dim"],
        plot_return_to_cyclicity["forplot"],
        "^",
        color="#5EB1BF",
        ms=10,
        label="return to cyclicity",
    )
    # plot estrus
    ax.plot(
        plot_estrus["dim_at_estrus"],
        plot_estrus["forplot"],
        "^",
        color="#EF7B45",
        ms=10,
        label="estrus",
    )

    # plot interluteal phases and luteal phases
    for i in plot_interluteal_phase["estrus_number"].unique():
        select_interluteal = plot_interluteal_phase[
            plot_interluteal_phase["estrus_number"] == i
        ]
        plt.axvline(
            x=select_interluteal["end_interluteal"].iloc[0], linestyle="--", color="lightgrey"
        )
        plt.axvline(
            x=select_interluteal["start_interluteal"].iloc[0], linestyle="--", color="lightgrey"
        )
        ax.text(
            (
                select_interluteal["start_interluteal"]
                + (select_interluteal["interluteal_phase_length"] / 2)
            ),
            (p4_lactation["raw"].max() + 2),
            "interluteal",
            fontsize=8,
            color="black",
            ha="center",
            va="bottom",
        )
    for i in plot_luteal_phase["estrus_number"].unique():
        select_luteal = plot_luteal_phase[plot_luteal_phase["estrus_number"] == i]
        ax.text(
            (
                select_luteal["start_luteal"]
                + (select_luteal["luteal_phase_length"] / 2)
            ),
            (p4_lactation["raw"].max() + 2),
            "luteal",
            fontsize=8,
            color="black",
            ha="center",
            va="bottom",
        )
        # also plot the very first luteal phase start
        if i == 0:
            plt.axvline(
                x=select_luteal["start_luteal"].iloc[0],
                linestyle="--",
                color="lightgrey",
            )

    ax.grid(axis="y", linewidth=1)
    ax.grid(axis="x", linewidth=0)
    ax.set_xlabel("dim")
    ax.set_ylabel("milk p4 (ng/mL)")
    plt.legend()
    plt.title(
        (
            "farm_id: "
            + str(p4_lactation["farm_id"].iloc[0])
            + ", lactation_id: "
            + str(p4_lactation["lactation_id"].iloc[0])
            + ", parity: "
            + str(p4_lactation["parity"].iloc[0])
        )
    )
    # Setting the values for all axes.
    plt.ylim(top=(p4_lactation["raw"].max() + 3))
    plt.tight_layout()
    plt.show()


def calc_thi(temperature, rel_humidity):
    """

    THI calculation:
    THI = 1.8*T+32-((0.55-0.0055*rel_hum)*(1.8*T-26))

    Parameters
    ----------
    temperature : Array (dtype = float)
        Temperature in Celsius
    rel_humidity : Array (dtype = float)
        Relative humidity in percentage

    Returns
    -------
    thi : Array (dtype = float)

    """

    # calculate per hour thi
    thi = (
        1.8 * temperature
        + 32
        - ((0.55 - 0.0055 * rel_humidity) * (1.8 * temperature - 26))
    )
    return thi


def add_thi(weather_dataframe):
    """
    Parameters
    ----------
    weather_dataframe : dataframe
        Dataframe containing temperature and humidityy data

    Returns
    -------
    weather_dataframe : dataframe
        Dataframe containing additionally a column with thi

    """

    weather_dataframe["thi"] = calc_thi(
        weather_dataframe.temperature, weather_dataframe.humidity
    )
    return weather_dataframe


def add_lat(weather_dataframe):
    """
    Calculates the relative time of the day where the temperature is
    1. >= 25 - high temperature
    2. <= 18 - low temperature
    (>18 & <25 is considered moderate temperature)

    A daily lagged accumulated temperature (lat) is then calculated as follows
    lat = (0.5 * (1-temp_hrs_low-temp_hrs_high) + 2 * temp_hrs_high)*24


    Parameters
    ----------
    weather_dataframe : dataframe
        dataframe containing temperature data and datetime

    Returns
    -------
    df_weather_daily : dataframe
        Dataframe containing the number of measurements per day, the min and max temperature,
        the relative time per day where the temperature is low, respectively high, and the lat

    """

    df_weather = weather_dataframe[["farm_id", "datetime", "temperature"]].copy()
    df_weather.datetime = pd.to_datetime(df_weather.datetime)
    df_weather["date"] = df_weather.datetime.dt.date
    df_weather["temp_ishigh"] = 0
    df_weather.loc[df_weather["temperature"] >= 25, "temp_ishigh"] = 1
    df_weather["temp_islow"] = 0
    df_weather.loc[df_weather["temperature"] <= 18, "temp_islow"] = 1

    df_weather_daily = (
        df_weather[["farm_id", "date", "temperature", "temp_ishigh", "temp_islow"]]
        .groupby(by=["farm_id", "date"])
        .agg(
            {
                "temperature": ["count", "min", "max"],
                "temp_ishigh": ["sum"],
                "temp_islow": ["sum"],
            }
        )
    ).reset_index()

    df_weather_daily.columns = df_weather_daily.columns.droplevel()
    df_weather_daily.columns = [
        "farm_id",
        "date",
        "no_meas",
        "temp_min",
        "temp_max",
        "temp_hrs_high",
        "temp_hrs_low",
    ]

    df_weather_daily.temp_hrs_high = (
        df_weather_daily.temp_hrs_high / df_weather_daily.no_meas
    )
    df_weather_daily.temp_hrs_low = (
        df_weather_daily.temp_hrs_low / df_weather_daily.no_meas
    )

    # calculate new weather feature lat = 0.5*hrs mod temp + 2* hrs high temp
    df_weather_daily["lat_single"] = (
        0.5 * (1 - df_weather_daily["temp_hrs_low"] - df_weather_daily["temp_hrs_high"])
        + 2 * df_weather_daily["temp_hrs_high"]
    ) * 24
    df_weather_daily = df_weather_daily.sort_values(by=["farm_id", "date"])
    df_weather_daily["lat"] = df_weather_daily.groupby("farm_id")["lat_single"].rolling(window=4, min_periods=1).sum().reset_index(level=0, drop=True)
    return df_weather_daily

