import os
import json
import random
import re

import numpy as np
import pandas as pd
import datetime as dt

from cowbase.cowbase_m5 import DB_connect
from pathlib import Path
from meteostat import Point, Hourly, Stations


def initiateDatabase(rootdir: str | Path, dbtype: str) -> None:
    """
    Creates a new database using CowBase's data scheme

    Parameters
    ----------
    rootdir : str or Path
        Filepath to CowBase root directory (e.g. linux: '/var/lib/'; windows: 'C:\\Users\\user\\Documents\\')
    dbtype : str
        postgres, mysql, sqlite - database management software needs to be downloaded and installed prior to this
    """

    rootdir = Path(rootdir)

    with open(rootdir / "config" / "serverSettings.json") as file:
        serverSettings = json.load(file)
    with open(rootdir / "config" / "M4_tableDict.json") as file:
        tableDict = json.load(file)

    db_connect = DB_connect(**serverSettings)
    db_connect.create_db()

    dbtype = serverSettings["dbtype"]

    for tables in tableDict:
        sql_statement = f"CREATE TABLE IF NOT EXISTS {tables} ("
        for columnnames in tableDict[tables][dbtype]:
            sql_statement += f"{columnnames} {tableDict[tables][dbtype][columnnames]}, "
        for pkeys in tableDict[tables]["p_key"]:
            sql_statement += f"PRIMARY KEY ({pkeys}), "
        for fkeys in tableDict[tables]["f_keys"]:
            sql_statement += f"FOREIGN KEY ({fkeys}) REFERENCES {tableDict[tables]['f_keys'][fkeys]}, "
        if len(tableDict[tables]["unique"]) > 0:
            sql_statement += f"UNIQUE({', '.join(tableDict[tables]['unique'])}), "
        sql_statement = sql_statement[0:-2] + ");"
        db_connect.execute(query=sql_statement)

    if dbtype == "postgres":
        sql_statement = """
        do
        $$
        begin
            if not exists (select * from pg_user where usename = 'dbview') then
                create role dbview password 'view';
            end if;
        end
        $$
        ;
        do
        $$
        begin
            if not exists (select * from pg_user where usename = 'dbwrite') then
                create role dbwrite password 'write';
            end if;
        end
        $$
        ;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO dbview;
        GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO dbwrite;
        """
        db_connect.execute(query=sql_statement)


def create_sql_insert_update(db_update: dict) -> str:
    """
    Creates an upsert sql statement from a dictionary containing necessary parameters (table, insert, conflict, update)

    Parameters
    ----------
    db_update : dict
        dictionary containing information to generate a sql statement

    Return
    ------
    update_sql : str
        sql statement
    """
    update_sql = f'INSERT INTO {db_update["table"]}'

    if db_update["insert"]:
        update_sql += f" ("
        for elem in db_update["insert"]:
            update_sql += f"{elem}, "
        update_sql = update_sql[:-2] + f") VALUES ("
        for elem in db_update["insert"]:
            update_sql += f":{elem}, "
        update_sql = update_sql[:-2] + f") "

    if db_update["conflict"]:
        update_sql += f"ON CONFLICT ("
        for elem in db_update["conflict"]:
            update_sql += f"{elem}, "
        update_sql = update_sql[:-2] + f") "

    if db_update["update"]:
        update_sql += f"DO UPDATE SET "
        for elem in db_update["update"]:
            update_sql += f"{elem} = EXCLUDED.{elem}, "
        update_sql = update_sql[:-2]

    update_sql += ";"
    return update_sql


def create_sql_update(db_update: dict) -> str:
    """
    Creates an update sql statement from a dictionary containing necessary parameters (table, update, where)

    Parameters
    ----------
    db_update : dict
        dictionary containing information to generate a sql statement

    Return
    ------
    update_sql : str
        sql statement
    """
    update_sql = f'UPDATE {db_update["table"]}'

    if db_update["update"]:
        update_sql += f" SET "
        for elem in db_update["update"]:
            update_sql += f"{elem} = :{elem}, "
        update_sql = update_sql[:-2]

    if db_update["where"]:
        update_sql += f" WHERE "
        for elem in db_update["where"]:
            update_sql += f"{elem} = :{elem} AND "
        update_sql = update_sql[:-4]

    update_sql += ";"
    return update_sql


def readData(
    filepath: str | Path, tablename: str, tableDict: dict, farmtype: str
) -> pd.DataFrame:
    """
    Read data from file (pandas)

    Parameters
    ----------
    filepath : str
        path to datafile (.csv)
    tablename : str
        name of the table/file
    tableDict : dict
        dictionary containing information about the table schema of the target database
    farmtype : str
        milking system identifier (d- delaval, l- lely)

    Return
    ------
    df_data : pandas dataframe

    """
    df_data = pd.read_csv(filepath, delimiter=";", header=0, engine="python")

    notnull_columns = tableDict[tablename][f"not_null_read"]

    if len(notnull_columns) > 0:
        for column in list(notnull_columns):
            df_data = df_data.loc[~pd.isnull(df_data[column])]

    datetime_columns = tableDict[tablename][f"{farmtype}_datetime"]

    if len(datetime_columns) > 0:
        for datetime_column in datetime_columns:
            df_data[datetime_column] = df_data[datetime_column].apply(pd.to_datetime)
            df_data[datetime_column] = df_data[datetime_column].dt.floor("s")
    return df_data


def updateFarm(
    df_data: pd.DataFrame,
    db_connect: DB_connect,
    farmname: str,
    milkingSystem: str,
    sqlupdateDict: dict,
    new_backup_date: dt.datetime,
) -> tuple[pd.DataFrame, int]:
    """
    Update farm information

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    farmname : str
        name of farm for which data is processed
    milkingSystem : str
        milking system identifier (d- delaval, l- lely)
    sqlupdateDict : dict
        dictionary containing information to generate a sql statement
    new_backup_date : dt.datetime
        max datetime for the new data that is being added to the database

    Return
    ------
    df_data : pandas dataframe
    farm_id : int
    update_ani_lac : Boolean

    """

    farm_sql = """
    SELECT farm_id, farmname, created_on, last_data
    FROM farm
    ;
    """
    farm_db = db_connect.query(query=farm_sql)

    if not farm_db.empty:
        if not pd.isnull(pd.to_datetime(farm_db.last_data).iloc[0]):
            last_data = pd.to_datetime(farm_db.last_data).iloc[0]
        else:
            last_data = dt.datetime(2000, 1, 1)
    else:
        last_data = dt.datetime(2000, 1, 1)

    if farmname in farm_db.loc[:, "farmname"].tolist():
        farm_update = pd.DataFrame(
            {
                "farmname": [str(farmname)],
                "created_on": [
                    farm_db.loc[farm_db["farmname"] == farmname, "created_on"].iloc[0]
                ],
                "updated_on": [dt.date.today()],
                "milking_system_type": [milkingSystem],
                "last_data": [max(new_backup_date, last_data).date()],
            }
        )

        # Update database table 'farm' with data from .txt file - insert if no data entry exist yet, update else

        farm_update_sql = create_sql_update(sqlupdateDict["sql_update"]["farm_upd"])
        db_connect.insert(query=farm_update_sql, data=farm_update.to_dict("records"))

    else:
        farm_update = pd.DataFrame(
            {
                "farmname": [str(farmname)],
                "created_on": [dt.date.today()],
                "updated_on": [dt.date.today()],
                "milking_system_type": [milkingSystem],
                "last_data": [new_backup_date.date()],
            }
        )

        # Insert into database table 'farm' with data from .txt file - insert if no data entry exist yet, update else

        farm_update_sql = create_sql_insert_update(sqlupdateDict["sql_update"]["farm"])
        db_connect.insert(query=farm_update_sql, data=farm_update.to_dict("records"))

    farm_id = db_connect.query(
        query=f"""SELECT farm_id FROM farm WHERE farmname = '{farmname}';"""
    ).squeeze()

    df_data["farm_id"] = farm_id

    if new_backup_date >= last_data:
        update_ani_lac = True
    else:
        update_ani_lac = False

    return df_data, farm_id, update_ani_lac


def updateAnimal(
    df_data: pd.DataFrame, db_connect: DB_connect, farm_id: int, sqlupdateDict: dict
) -> pd.DataFrame:
    """
    Update animal table

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    farm_id : integer
        id of farm for which data is processed
    sqlupdateDict : dict
        dictionary containing information to generate a sql statement
    """

    # animal update
    animal_sql = f"""
    SELECT farm_id, animal_oid
    FROM animal
    WHERE farm_id = {farm_id}
    ;
    """
    animal_db = db_connect.query(query=animal_sql)

    df_check_animal = df_data.copy(deep=True)
    df_check_animal = df_check_animal[["farm_id", "animal_oid"]].drop_duplicates()

    df_check_animal = df_check_animal.loc[~pd.isnull(df_check_animal.animal_oid)]
    df_check_animal.animal_oid = df_check_animal.animal_oid.astype(int)

    df_animal_update = df_check_animal.merge(
        animal_db[["farm_id", "animal_oid"]],
        how="left",
        on=["farm_id", "animal_oid"],
        indicator=True,
    )

    df_animal_update = df_animal_update.loc[
        df_animal_update["_merge"] == "left_only"
    ].drop(columns=["_merge"])

    df_animal_update = df_animal_update.loc[~pd.isnull(df_animal_update.animal_oid)]

    df_animal_update.animal_oid = df_animal_update.animal_oid.astype(int)

    df_animal_update["updated_on"] = dt.date.today()

    if len(df_animal_update) >= 1:
        # Update database table 'animal' with data from lactation data - insert if no data entry exist yet, update else

        df_animal_update = df_animal_update.drop(columns=["animal_id"])
        animal_update_sql = create_sql_insert_update(
            sqlupdateDict["sql_update"]["animal_table"]
        )
        db_connect.insert(
            query=animal_update_sql, data=df_animal_update.to_dict("records")
        )

    animal_ids = db_connect.query(
        query=f"""SELECT animal_id, animal_oid FROM animal WHERE farm_id = {farm_id};"""
    )

    dict_animal_ids = pd.Series(
        animal_ids.animal_id.values, index=animal_ids.animal_oid
    ).to_dict()

    df_data["animal_id"] = df_data["animal_oid"].map(dict_animal_ids)

    df_data = df_data.drop(columns=["animal_oid"])

    return df_data


def checkDatabase(
    df_data: pd.DataFrame,
    db_connect: DB_connect,
    table: str,
    farm_id: int,
    tableDict: dict,
) -> pd.DataFrame:
    """
    Check database for already present data

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    table : str
        name of the table/file
    farm_id : integer
        id of farm for which data is processed
    tableDict : dict
        dictionary containing information about the table schema of the target database

    Return
    ------
    data_update_new : pandas dataframe

    """
    data_sql = f"""
    SELECT {', '.join(tableDict[table]['unique'])}
    FROM {table}
    WHERE farm_id = {farm_id}
    ;
    """
    data_db = db_connect.query(query=data_sql)

    df_data = df_data.drop_duplicates(subset=tableDict[table]["unique"])

    data_update = df_data.merge(
        data_db,
        how="left",
        on=tableDict[table]["unique"],
        indicator=True,
    )

    data_update_new = data_update.loc[data_update["_merge"] == "left_only"].drop(
        columns=["_merge"]
    )

    data_update_update = (
        data_update.loc[data_update["_merge"] == "both"].copy().drop(columns=["_merge"])
    )

    return data_update_new, data_update_update


def writeData(
    df_data: pd.DataFrame, db_connect, table: str, tableDict: dict, farmtype: str
) -> None:
    """
    Write new data to 'table'

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    table : str
        name of the table/file
    tableDict : dict
        dictionary containing information about the table schema of the target database
    farmtype : str
        milking system identifier (d- delaval, l- lely)
    """
    df_data["updated_on"] = dt.date.today()
    datetime_columns = tableDict[table][f"{farmtype}_datetime"]
    if len(datetime_columns) > 0:
        for column in datetime_columns:
            df_data[column] = df_data[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    notnull_columns = tableDict[table][f"not_null_write"]

    if len(notnull_columns) > 0:
        for column in list(notnull_columns):
            df_data_remove = df_data.loc[pd.isnull(df_data[column])]
            df_data = df_data.loc[~pd.isnull(df_data[column])]
            if len(df_data_remove) > 0:
                print("NOT NULL constraint failed; Data has been removed!")
                print(df_data_remove)

    df_data.to_sql(
        f"{table}", con=db_connect.ret_con(), if_exists="append", index=False
    )


def updateData(
    df_data: pd.DataFrame,
    db_connect,
    table: str,
    tableDict: dict,
    sqlupdateDict: dict,
    farmtype: str,
    farm_id: int,
    update_ani_lac: bool,
) -> None:
    """
    Update data in 'table'

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    table : str
        name of the table/file
    tableDict : dict
        dictionary containing information about the table schema of the target database
    farmtype : str
        milking system identifier (d- delaval, l- lely)
    farm_id : int
        Id of the farm
    update_ani_lac : bool
        True if the current update is newer that the last update for the particular farm
    """
    df_data["updated_on"] = dt.date.today()

    datetime_columns = tableDict[table][f"{farmtype}_datetime"]
    if len(datetime_columns) > 0:
        for column in datetime_columns:
            df_data[column] = df_data[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    df_data = df_data.where(pd.notnull(df_data), None)

    notnull_columns = tableDict[table][f"not_null_write"]

    if len(notnull_columns) > 0:
        for column in list(notnull_columns):
            df_data_remove = df_data.loc[pd.isnull(df_data[column])]
            df_data = df_data.loc[~pd.isnull(df_data[column])]
            if len(df_data_remove) > 0:
                print("NOT NULL constraint failed; Data has been removed!")
                print(df_data_remove)

    if update_ani_lac == True:
        data_sql = f"""
        SELECT *
        FROM {table}
        WHERE farm_id = {farm_id}
        AND {tableDict[table]['unique'][1]} in ({', '.join(list(df_data[f"{tableDict[table]['unique'][1]}"].astype(str)))})
        ;
        """
        data_db = db_connect.query(query=data_sql)

        datetime_columns = tableDict[table][f"{farmtype}_datetime"]
        if len(datetime_columns) > 0:
            for column in datetime_columns:
                data_db[column] = pd.to_datetime(data_db[column])
                data_db[column] = data_db[column].dt.strftime("%Y-%m-%d %H:%M:%S")

        dict_animal_ids = pd.Series(
            data_db[tableDict[table]["p_key"][0]].values,
            index=data_db[tableDict[table]["unique"][1]],
        ).to_dict()
        df_data[tableDict[table]["p_key"][0]] = df_data[
            tableDict[table]["unique"][1]
        ].map(dict_animal_ids)

        data_db = data_db[df_data.columns]

        data_db = data_db.sort_values(
            by=["farm_id", f"{tableDict[table]['unique'][1]}"]
        ).reset_index(drop=True)
        df_data = df_data.sort_values(
            by=["farm_id", f"{tableDict[table]['unique'][1]}"]
        ).reset_index(drop=True)

        # Compare the two dataframes
        df_diff = data_db.compare(df_data)

        # Get first level columns
        first_level_columns = df_diff.columns.get_level_values(0).unique()

        changelog = pd.DataFrame()

        # Iterate over the first level columns
        for column in first_level_columns:
            # Select rows where 'self' is not equal to 'other'
            diff_pair = df_diff.loc[
                df_diff[column]["self"].ne(df_diff[column]["other"]), column
            ]
            # Remove rows where both 'self' and 'other' are NaN
            diff_pair = diff_pair.dropna(subset=["self", "other"], how="all")
            diff_pair["columnname"] = column
            diff_pair = diff_pair.merge(
                data_db[tableDict[table]["p_key"][0]],
                how="left",
                left_index=True,
                right_index=True,
            )
            changelog = pd.concat([changelog, diff_pair])
        changelog.rename(
            columns={
                tableDict[table]["p_key"][0]: "table_id",
                "self": "prev_value",
                "other": "new_value",
            },
            inplace=True,
        )
        changelog["tablename"] = table
        changelog["updated_on"] = dt.date.today()
        changelog = changelog.loc[changelog.columnname != "updated_on"]

        if not changelog.empty:
            changelog.to_sql(
                "changelog", con=db_connect.ret_con(), if_exists="append", index=False
            )

    if farmtype == "l" and table == "lactation":
        df_data.breed = df_data.breed.astype("Int64")

    # Update database table 'table' if data has changed in new backup/data import
    table_update_sql = create_sql_update(
        sqlupdateDict["sql_update"][f"{table}_upd_{farmtype}"]
    )
    db_connect.insert(query=table_update_sql, data=df_data.to_dict("records"))


def updateMilking(
    df_milking: pd.DataFrame,
    db_connect,
    farm_id: int,
    farmname: str,
    farmtype: str,
    sqlupdateDict: dict,
    tableDict: dict,
) -> None:
    """
    Update milking table

    Parameters
    ----------
    df_milking : pandas dataframe
        dataframe for the milking table
    db_connect : sql engine
        engine to connect ot database
    farm_id : integer
        id of farm for which data is processed
    farmname : str
        name of farm for which data is processed
    farmtype : str
        milking system identifier (d- delaval, l- lely)
    sqlupdateDict : dict
        dictionary containing information to generate a sql statement
    tableDict : dict
        dictionary containing information about the table schema of the target database
    """
    print("Total milking entries in backup:", len(df_milking))
    milking_sql = f"""
    SELECT farm_id, animal_id, milking_oid, started_at, ended_at, tmy
    FROM milking
    WHERE farm_id = {farm_id}
    ;
    """
    milking_db = db_connect.query(query=milking_sql)

    milking_db.started_at = milking_db.started_at.apply(pd.to_datetime)
    milking_db.ended_at = milking_db.ended_at.apply(pd.to_datetime)

    df_milking["farm_id"] = farm_id

    df_milking = df_milking.drop_duplicates(
        subset=["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"]
    )

    milking_update_new = df_milking.merge(
        milking_db[["farm_id", "animal_id", "milking_oid"]],
        how="left",
        on=["farm_id", "animal_id", "milking_oid"],
        indicator=True,
    )
    milking_update_new = milking_update_new[milking_update_new["_merge"] == "left_only"]
    milking_update_new = milking_update_new.drop(columns=["_merge"])

    milking_update_new.started_at = milking_update_new.started_at.apply(pd.to_datetime)
    milking_update_new.ended_at = milking_update_new.ended_at.apply(pd.to_datetime)

    print("Total new milking entries:", len(milking_update_new))

    ################################################################################################################
    # apply lactation_ids, parities and calving dates to milking_update_new

    lactation_sql = f"""
    SELECT farm_id, animal_id, lactation_oid, calving, dry_off, parity
    FROM lactation
    WHERE farm_id = {farm_id}
    ;
    """
    lactation_db = db_connect.query(query=lactation_sql)

    animal_sql = f"""
    SELECT farm_id, animal_id, animal_oid, birth_date
    FROM animal
    WHERE farm_id = {farm_id}
    ;
    """
    animal_db = db_connect.query(query=animal_sql)

    if len(milking_update_new) > 0:
        ################################################################################################################
        # Lactation correction (farm level)
        ################################################################################################################
        # Step 1: Identify gaps in data at farm level

        if len(milking_db) > 0:
            df_farmgap_det = pd.concat(
                [
                    milking_db[["animal_id", "started_at"]],
                    milking_update_new[["animal_id", "started_at"]],
                ]
            )
        else:
            df_farmgap_det = milking_update_new[["animal_id", "started_at"]].copy()
        df_farmgap_det["started_at"] = pd.to_datetime(
            df_farmgap_det.loc[:, "started_at"]
        )
        df_farmgap_det = df_farmgap_det.loc[
            (df_farmgap_det.started_at > dt.datetime(2000, 1, 1))
            & (df_farmgap_det.started_at <= dt.datetime.today())
        ]

        start_date_farm = df_farmgap_det.started_at.min()
        # Calculate the minimum started_at for each animal_id
        start_date_animals = df_farmgap_det.groupby('animal_id')['started_at'].min()

        # Convert started_at to date, drop duplicates
        df_farmgap_det.started_at = df_farmgap_det.started_at.dt.date
        df_farmgap_det = df_farmgap_det.drop_duplicates()
        df_farmgap_det = df_farmgap_det.groupby(by="started_at").count().reset_index()

        # sort milk data and calculate gaps
        df_farmgap_det = df_farmgap_det.sort_values(by=["started_at"]).reset_index(
            drop=True
        )
        df_farmgap_det["gap"] = (
            df_farmgap_det.started_at.diff().dt.total_seconds() / 86400
        )

        df_farmgap_det.loc[pd.isnull(df_farmgap_det.gap), "gap"] = 0
        df_farmgap_det.loc[df_farmgap_det.gap < 2, "gap"] = 0
        df_farmgap_det.loc[df_farmgap_det.gap > 0, "gap"] = 1

        # define periods restricted by gaps of at least 2 days
        df_farmgap_det["periods"] = df_farmgap_det.gap.cumsum()

        farm_gaps = pd.DataFrame(columns=["gap", "gap_start", "gap_end", "gap_length"])
        if df_farmgap_det.periods.max() > 0:
            for i in range(int(df_farmgap_det.periods.max())):
                gap = int(i + 1)
                gap_start = df_farmgap_det.loc[
                    df_farmgap_det.periods == i, "started_at"
                ].max()
                gap_end = df_farmgap_det.loc[
                    df_farmgap_det.periods == i + 1, "started_at"
                ].min()
                gap_length = gap_end - gap_start
                farm_gaps.loc[len(farm_gaps.index)] = [
                    gap,
                    gap_start,
                    gap_end,
                    gap_length,
                ]

        ################################################################################################################
        # Step 2: Remove too short lactation lengths indicated by the farmer
        # (remove both the lactations that are indicated as too close together)
        df_lac_farm_corr = lactation_db.copy()
        df_lac_farm_corr["calving"] = pd.to_datetime(df_lac_farm_corr.loc[:, "calving"])
        df_lac_farm_corr["dry_off"] = pd.to_datetime(df_lac_farm_corr.loc[:, "dry_off"])
        df_lac_farm_corr = df_lac_farm_corr.loc[
            (df_lac_farm_corr.calving > dt.datetime(2000, 1, 1))
            & (df_lac_farm_corr.calving <= dt.datetime.today())
        ].sort_values(by=["animal_id", "calving"])
        df_lac_farm_corr["prev_lactation_length"] = df_lac_farm_corr.groupby(
            by="animal_id"
        ).calving.diff()
        # Convert Timedelta to float (total seconds) and handle NaN values
        df_lac_farm_corr["prev_lactation_length"] = df_lac_farm_corr[
            "prev_lactation_length"
        ].apply(lambda x: x.total_seconds() / 86400 if pd.notnull(x) else None)
        # Shift the lactation_length column one row back within each animal_id group
        df_lac_farm_corr["lactation_length"] = df_lac_farm_corr.groupby("animal_id")[
            "prev_lactation_length"
        ].shift(-1)
        df_lac_farm_corr = df_lac_farm_corr.loc[
            (
                pd.isnull(df_lac_farm_corr.prev_lactation_length)
                & (df_lac_farm_corr.lactation_length >= 270)
            )
            | (
                pd.isnull(df_lac_farm_corr.lactation_length)
                & (df_lac_farm_corr.prev_lactation_length >= 270)
            )
            | (
                pd.isnull(df_lac_farm_corr.prev_lactation_length)
                & pd.isnull(df_lac_farm_corr.lactation_length)
            )
            | (
                (df_lac_farm_corr.prev_lactation_length >= 270)
                & (df_lac_farm_corr.lactation_length >= 270)
            )
        ]
        df_lac_farm_corr.loc[df_lac_farm_corr.parity >= 20, "parity"] = None

        ################################################################################################################
        # Step 3: Identify gaps in milking data

        if len(milking_db) > 0:
            df_milkgap_det = pd.concat(
                [
                    milking_db[["animal_id", "started_at", "tmy"]],
                    milking_update_new[["animal_id", "started_at", "tmy"]],
                ]
            )
        else:
            df_milkgap_det = milking_update_new[
                ["animal_id", "started_at", "tmy"]
            ].copy()
        df_milkgap_det = df_milkgap_det.loc[~pd.isnull(df_milkgap_det.tmy)]
        df_milkgap_det = df_milkgap_det[["animal_id", "started_at"]]
        df_milkgap_det["started_at"] = pd.to_datetime(df_milkgap_det["started_at"])
        df_milkgap_det = df_milkgap_det.loc[
            (df_milkgap_det.started_at > dt.datetime(2000, 1, 1))
            & (df_milkgap_det.started_at <= dt.datetime.today())
        ]

        # sort milk data and calculate gaps
        df_milkgap_det = df_milkgap_det.sort_values(
            by=["animal_id", "started_at"]
        ).reset_index(drop=True)
        df_milkgap_det["gap"] = (
            df_milkgap_det.groupby(by="animal_id").started_at.diff().dt.total_seconds()
            / 86400
        )

        df_milkgap_det.loc[pd.isnull(df_milkgap_det.gap), "gap"] = 0
        df_milkgap_det.loc[df_milkgap_det.gap < 14, "gap"] = 0
        df_milkgap_det.loc[df_milkgap_det.gap > 0, "gap"] = 1

        # define periods restricted by gaps of at least 10 days
        df_milkgap_det["periods"] = df_milkgap_det.groupby(by="animal_id").gap.cumsum()

        # define the calculated calving date as the date of the first milking in each period
        df_milkgap_det["calving"] = df_milkgap_det.groupby(
            by=["animal_id", "periods"]
        ).started_at.transform("min")
        df_milkgap_det["calving"] = df_milkgap_det["calving"]

        # define the calculated dry off date as the date of the last milking in each period
        df_milkgap_det["dry_off"] = df_milkgap_det.groupby(
            by=["animal_id", "periods"]
        ).started_at.transform("max")
        df_milkgap_det["dry_off"] = df_milkgap_det["dry_off"]

        # # Remove each first calving as it is likely to be the first available data not the true calving date
        # df_milkgap_det = df_milkgap_det.loc[df_milkgap_det.periods > 0]

        df_lac_corrected_2 = (
            df_milkgap_det[["animal_id", "calving", "dry_off"]].copy().drop_duplicates()
        )

        # Set each last available dry off for each cow to None, as we can not be sure if this is due to the data period ending or a true dry off
        # Sort by animal_id and calving in descending order
        df_lac_corrected_2.sort_values(
            ["animal_id", "calving"], ascending=[True, False], inplace=True
        )

        # Set the 'dry_off' of the first entry of each 'animal_id' group to None
        df_lac_corrected_2.loc[
            df_lac_corrected_2.dry_off
            >= (df_lac_corrected_2.dry_off.max() - dt.timedelta(days=30)),
            "dry_off",
        ] = None

        # df_lac_corrected_2.sort_values(by=["animal_id", "calving"], inplace=True)

        ################################################################################################################
        # Step 4: Remove gaps that coincide with missing data on farm level
        df_lac_corrected_1 = df_lac_farm_corr[
            ["animal_id", "parity", "calving", "dry_off"]
        ].copy()
        df_lac_corrected_1.loc[:, "reported"] = "farmer"
        df_lac_corrected_2.loc[:, "reported"] = "gap_detection"
        df_lac_corrected = pd.concat([df_lac_corrected_1, df_lac_corrected_2])

        # Remove gaps detected that coincide with missing data on farm level

        if farm_gaps.empty == False:
            for i in list(farm_gaps.gap):
                farmgap_start = pd.to_datetime(
                    farm_gaps.loc[farm_gaps.gap == i, "gap_start"]
                ).values[0]
                farmgap_end = pd.to_datetime(
                    farm_gaps.loc[farm_gaps.gap == i, "gap_end"]
                ).values[0]
                df_lac_corrected = df_lac_corrected.loc[
                    (
                        (df_lac_corrected.reported == "gap_detection")
                        & (
                            (df_lac_corrected.calving < farmgap_start)
                            | (df_lac_corrected.calving > farmgap_end)
                        )
                    )
                    | (df_lac_corrected.reported == "farmer")
                ]

        # Calculate period between (potential) calvings

        df_lac_corrected = df_lac_corrected.sort_values(by=["animal_id", "calving"])
        df_lac_corrected["gap_prev"] = (
            df_lac_corrected.groupby(by="animal_id")
            .calving.diff()
            .apply(lambda x: x.total_seconds() / 86400 if pd.notnull(x) else None)
        )
        df_lac_corrected["gap_next"] = (
            df_lac_corrected.groupby(by="animal_id")
            .calving.diff(periods=-1)
            .apply(lambda x: x.total_seconds() / 86400 if pd.notnull(x) else None)
        )

        ################################################################################################################
        # Step 5: Check which calvings are present in both the farmer reported dataset and the on gaps-detection based dataset
        df_lac_corrected2 = df_lac_corrected.copy().reset_index()

        # Convert to datetime if not already
        df_lac_corrected2["calving"] = pd.to_datetime(df_lac_corrected2["calving"])
        df_lac_corrected2["dry_off"] = pd.to_datetime(df_lac_corrected2["dry_off"])

        # Sort by animal_id and calving
        df_lac_corrected2.sort_values(["animal_id", "calving"], inplace=True)

        # Create calving_period column
        df_lac_corrected2["calving_prev"] = df_lac_corrected2.groupby(
            by="animal_id"
        ).calving.shift(1)
        df_lac_corrected2["reported_prev"] = df_lac_corrected2.groupby(
            by="animal_id"
        ).reported.shift(1)

        df_lac_corrected2["pres_calving"] = df_lac_corrected2["calving"]
        df_lac_corrected2.loc[
            (df_lac_corrected2.gap_prev < 20)
            & (df_lac_corrected2.reported != df_lac_corrected2.reported_prev),
            "pres_calving",
        ] = df_lac_corrected2["calving_prev"]

        # Create separate dataframes for farmer and gap_detection
        df_farmer = df_lac_corrected2[df_lac_corrected2["reported"] == "farmer"].copy()
        df_gap_detection = df_lac_corrected2[
            df_lac_corrected2["reported"] == "gap_detection"
        ].copy()

        # Merge the dataframes
        df_merged = pd.merge(
            df_farmer,
            df_gap_detection,
            on=["animal_id", "pres_calving"],
            how="outer",
            suffixes=("_farmer", "_gap_detection"),
        )

        # Combine the data
        df_merged["calving"] = df_merged[
            ["calving_farmer", "calving_gap_detection"]
        ].min(axis=1)
        df_merged["dry_off"] = df_merged["dry_off_gap_detection"].fillna(
            df_merged["dry_off_farmer"]
        )
        df_merged["parity"] = df_merged["parity_gap_detection"].combine_first(
            df_merged["parity_farmer"]
        )
        df_merged["reported"] = df_merged.apply(
            lambda row: (
                "both"
                if pd.notnull(row["reported_farmer"])
                and pd.notnull(row["reported_gap_detection"])
                else (
                    row["reported_farmer"]
                    if pd.notnull(row["reported_farmer"])
                    else row["reported_gap_detection"]
                )
            ),
            axis=1,
        )

        # Keep only the necessary columns
        df_merged = df_merged[
            ["animal_id", "calving", "dry_off", "parity", "reported"]
        ].sort_values(by=["animal_id", "calving"])

        df_merged["gap_prev"] = (
            df_merged.groupby(by="animal_id").calving.diff().dt.total_seconds() / 86400
        )
        df_merged["gap_next"] = (
            df_merged.groupby(by="animal_id")
            .calving.diff(periods=-1)
            .dt.total_seconds()
            / 86400
        )
        df_merged["dry_off_prev"] = df_merged.groupby(by="animal_id").dry_off.shift(1)

        ################################################################################################################
        # Step 6: Remove potential calvings detected by gap-detection if they are too close to a prior/next lactation (i.e. do not make sense with the given pregnancy length)

        df_merged = df_merged.loc[
            (df_merged.reported == "both")
            | (df_merged.reported == "farmer")
            | (
                (df_merged.reported == "gap_detection")
                & (
                    (df_merged.calving >= df_merged.dry_off_prev)
                    | pd.isnull(df_merged.dry_off_prev)
                )
                & (df_merged.gap_prev >= 270)
                & ((df_merged.gap_next <= -270) | pd.isnull(df_merged.gap_next))
                & (df_merged.calving >= start_date_farm + dt.timedelta(days=365))
                & (df_merged.apply(lambda row: row.calving >= (start_date_animals[row.animal_id] if row.animal_id in start_date_animals else start_date_farm) + dt.timedelta(days=365), axis=1))
            )
        ]

        ################################################################################################################
        # Step 7: Add the birth date and correct for first recorded lactaitons where no parity number is available
        # (guess based on median distribution of age at calving for the farm)

        df_animal_info = animal_db[["animal_id", "birth_date"]].copy()
        df_animal_info["birth_date"] = pd.to_datetime(df_animal_info["birth_date"])

        df_lac_final = df_merged.merge(df_animal_info, on="animal_id")
        df_lac_final = df_lac_final.loc[df_lac_final.calving != df_lac_final.birth_date]
        df_lac_final["birth_to_parity"] = (
            df_lac_final.calving - df_lac_final.birth_date
        ).dt.total_seconds() / 86400

        # Calculate a dictionary defining thresholds to apply to lactations without parity information
        parity_dict = (
            df_lac_final.groupby(by="parity")
            .birth_to_parity.median()
            .reset_index()
            .sort_values("parity")
            .reset_index(drop=True)
        )
        parity_dict = (
            parity_dict.loc[parity_dict.parity > 0]
            .sort_values("parity")
            .reset_index(drop=True)
        )
        parity_dict = parity_dict.loc[parity_dict.parity == parity_dict.index + 1]
        parity_dict["parity_lowerlimit"] = parity_dict.rolling(2).birth_to_parity.mean()
        parity_dict["parity_upperlimit"] = parity_dict["parity_lowerlimit"].shift(-1)
        parity_dict.loc[parity_dict.parity == 1, "parity_lowerlimit"] = 0
        parity_dict.loc[
            parity_dict.parity == parity_dict.parity.max(), "parity_upperlimit"
        ] = df_lac_final.birth_to_parity.max()

        # Apply parity information to final lactation table
        for i in parity_dict.parity:
            par_ll = parity_dict.loc[parity_dict.parity == i, "parity_lowerlimit"].iloc[
                0
            ]
            par_ul = parity_dict.loc[parity_dict.parity == i, "parity_upperlimit"].iloc[
                0
            ]
            df_lac_final.loc[
                pd.isnull(df_lac_final.parity)
                & (
                    (df_lac_final.calving - df_lac_final.birth_date).dt.total_seconds()
                    / 86400
                    > par_ll
                )
                & (
                    (df_lac_final.calving - df_lac_final.birth_date).dt.total_seconds()
                    / 86400
                    <= par_ul
                ),
                "parity",
            ] = i

        df_lac_final.reset_index(inplace=True, drop=True)

        ################################################################################################################
        # Step 8: Check if consecutive lactations have consecutive parity numbers

        # Check if consecutive entries have consecutive lactation numbers, correct otherwise
        for index, row in df_lac_final.iterrows():
            if index == 0:
                continue
            if (
                (
                    df_lac_final.loc[index, "animal_id"]
                    == df_lac_final.loc[index - 1, "animal_id"]
                )
                and (
                    df_lac_final.loc[index, "parity"]
                    != df_lac_final.loc[index - 1, "parity"] + 1
                )
                and (
                    (
                        (
                            df_lac_final.loc[index, "calving"]
                            - df_lac_final.loc[index - 1, "calving"]
                        ).total_seconds()
                        / 86400
                    )
                    < 700
                )
            ):
                df_lac_final.loc[index, "parity"] = (
                    df_lac_final.loc[index - 1, "parity"] + 1
                )

        ################################################################################################################
        # Step 9: Create final set of corrected lactation parameters

        df_lac_final = df_lac_final[
            ["animal_id", "birth_date", "calving", "dry_off", "parity", "reported"]
        ]

        df_lac_final["lactation_length"] = np.round(
            (df_lac_final.dry_off - df_lac_final.calving).dt.total_seconds() / 86400,
            decimals=2,
        )
        df_lac_final.loc[df_lac_final.lactation_length <= 250, "dry_off"] = None
        df_lac_final["lactation_length"] = np.round(
            (df_lac_final.dry_off - df_lac_final.calving).dt.total_seconds() / 86400,
            decimals=2,
        )
        df_lac_final["calving_prev"] = df_lac_final.groupby(
            by="animal_id"
        ).calving.shift(1)
        df_lac_final["dry_off_prev"] = df_lac_final.groupby(
            by="animal_id"
        ).dry_off.shift(1)
        df_lac_final["dry_period_prev"] = np.round(
            (df_lac_final.calving - df_lac_final.dry_off_prev).dt.total_seconds()
            / 86400,
            decimals=2,
        )
        df_lac_final["lactation_length_prev"] = np.round(
            (df_lac_final.dry_off_prev - df_lac_final.calving_prev).dt.total_seconds()
            / 86400,
            decimals=2,
        )
        df_lac_final["farm_id"] = farm_id
        df_lac_final.loc[df_lac_final.parity == 1, "age_at_first_calving"] = np.round(
            (
                df_lac_final.loc[df_lac_final.parity == 1, "calving"]
                - df_lac_final.loc[df_lac_final.parity == 1, "birth_date"]
            ).dt.total_seconds()
            / 86400,
            decimals=2,
        )
        df_lac_final["age_at_first_calving"] = df_lac_final.groupby("animal_id")[
            "age_at_first_calving"
        ].transform(lambda x: x.min(skipna=True))

        ################################################################################################################
        # Step 10: Update corrected lactation information to database

        # update lactation table
        df_lac_final.loc[pd.isnull(df_lac_final.parity)] = 0
        df_lac_final.parity = df_lac_final.parity.astype(int)
        df_lac_final["updated_on"] = dt.date.today()

        df_lac_final["birth_date"] = pd.to_datetime(df_lac_final.loc[:, "birth_date"])
        df_lac_final["calving"] = pd.to_datetime(df_lac_final.loc[:, "calving"])
        df_lac_final["dry_off"] = pd.to_datetime(df_lac_final.loc[:, "dry_off"])
        df_lac_final["calving_prev"] = pd.to_datetime(
            df_lac_final.loc[:, "calving_prev"]
        )
        df_lac_final["dry_off_prev"] = pd.to_datetime(
            df_lac_final.loc[:, "dry_off_prev"]
        )
        datetime_columns = tableDict["lactation_corrected"][f"{farmtype}_datetime"]
        for column in datetime_columns:
            df_lac_final[column] = df_lac_final[column].dt.strftime("%Y-%m-%d %H:%M:%S")
        df_lac_final = df_lac_final.where(pd.notnull(df_lac_final), None)
        df_lac_final = df_lac_final.loc[df_lac_final.farm_id == farm_id]

        # Fetch data from lactation_corrected table
        lac_corr_sql = f"SELECT * FROM lactation_corrected WHERE farm_id={farm_id}"
        lactation_corrected = db_connect.query(query=lac_corr_sql)

        # Merge to find differences based on farm_id, animal_id, and parity
        merged_diff = lactation_corrected.merge(
            df_lac_final,
            on=["farm_id", "animal_id", "parity"],
            how="outer",
            indicator=True,
        )

        # Rows in lactation_corrected but not in df_lac_final
        rows_to_delete = merged_diff[merged_diff["_merge"] == "left_only"]

        # Update parity to 99 in lactation_corrected for rows not in df_lac_final
        # Track the current parity for each (farm_id, animal_id) combination
        current_parity = {}

        for index, row in rows_to_delete.iterrows():
            key = (row["farm_id"], row["animal_id"])

            # Initialize the parity if the key is not in the dictionary
            if key not in current_parity:
                if row["animal_id"] not in lactation_corrected["animal_id"].values:
                    current_parity[key] = 99
                else:
                    current_parity[key] = int(lactation_corrected.loc[
                        (lactation_corrected["farm_id"] == row["farm_id"]) &
                        (lactation_corrected["animal_id"] == row["animal_id"]),
                        "parity"
                    ].max() + 1)
            else:
                # Increment the parity for subsequent entries
                current_parity[key] += 1

            update_sql = f"""
            UPDATE lactation_corrected 
            SET parity = {current_parity[key]}
            WHERE farm_id = '{row['farm_id']}' 
            AND animal_id = '{row['animal_id']}' 
            AND parity = {row['parity']}
            """
            db_connect.execute(update_sql)

        lactation_sql = create_sql_insert_update(
            sqlupdateDict["sql_update"]["corrected_lactation_update"]
        )
        db_connect.insert(query=lactation_sql, data=df_lac_final.to_dict("records"))

        ################################################################################################################
        # Step 11: Apply corrected lactation information to milking data

        # add the lactation_ids back to the milking dataframe
        lactation_db = db_connect.query(
            query=f"""SELECT lactation_id, animal_id, parity, calving FROM lactation_corrected WHERE farm_id = {farm_id} AND parity < 99;"""
        )

        milking_sql = f"""
        SELECT farm_id, animal_id, lactation_id, milking_oid, parity, dim, started_at, ended_at
        FROM milking
        WHERE farm_id = {farm_id}
        ;
        """
        milking_db = db_connect.query(query=milking_sql)

        milking_db.started_at = milking_db.started_at.apply(pd.to_datetime)
        milking_db.ended_at = milking_db.ended_at.apply(pd.to_datetime)

        df_apply_lac_corr = pd.concat(
            [
                milking_db[
                    ["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"]
                ],
                milking_update_new[
                    ["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"]
                ],
            ]
        )
        df_apply_lac_corr.started_at = df_apply_lac_corr.started_at.apply(
            pd.to_datetime
        )
        df_apply_lac_corr.ended_at = df_apply_lac_corr.ended_at.apply(pd.to_datetime)

        for lacids in lactation_db.sort_values(
            by=["animal_id", "parity"]
        ).lactation_id.unique():
            aniid = lactation_db.loc[
                lactation_db.lactation_id == lacids, "animal_id"
            ].values[0]
            calvingdate = (
                lactation_db.loc[lactation_db.lactation_id == lacids, "calving"]
                .apply(pd.to_datetime)
                .values[0]
            )
            if calvingdate == None:  # fixing error when calvingdate == None
                calvingdate = df_apply_lac_corr.loc[
                    (df_apply_lac_corr.animal_id == aniid), "started_at"
                ].min()

            lacno = lactation_db.loc[
                lactation_db.lactation_id == lacids, "parity"
            ].values[0]
            df_apply_lac_corr.loc[
                (df_apply_lac_corr.animal_id == aniid)
                & (df_apply_lac_corr.started_at >= calvingdate),
                "lactation_id",
            ] = lacids
            df_apply_lac_corr.loc[
                (df_apply_lac_corr.animal_id == aniid)
                & (df_apply_lac_corr.started_at >= calvingdate),
                "parity",
            ] = lacno
            df_apply_lac_corr.loc[
                (df_apply_lac_corr.animal_id == aniid)
                & (df_apply_lac_corr.started_at >= calvingdate),
                "calving",
            ] = calvingdate

        # Calculate new DIM
        df_apply_lac_corr.loc[
            ~pd.isnull(df_apply_lac_corr.ended_at)
            & ~pd.isnull(df_apply_lac_corr.calving),
            "dim",
        ] = (
            (
                df_apply_lac_corr.loc[
                    ~pd.isnull(df_apply_lac_corr.ended_at)
                    & ~pd.isnull(df_apply_lac_corr.calving),
                    "ended_at",
                ].apply(pd.to_datetime)
                - df_apply_lac_corr.loc[
                    ~pd.isnull(df_apply_lac_corr.ended_at)
                    & ~pd.isnull(df_apply_lac_corr.calving),
                    "calving",
                ].apply(pd.to_datetime)
            ).dt.total_seconds()
            / 86400
        ).round(
            decimals=2
        )

        # drop the data that was already available in the database
        df_apply_lac_corr["updated_on"] = dt.date.today()

        # Merge the DataFrames on animal_id and milking_oid
        merged_df = pd.merge(
            milking_db,
            df_apply_lac_corr,
            on=["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"],
            suffixes=("_milking", "_apply"),
        )

        # Filter rows where lactation_id, parity, or dim differ
        rows_to_update = merged_df[
            (merged_df["lactation_id_milking"] != merged_df["lactation_id_apply"])
            | (merged_df["parity_milking"] != merged_df["parity_apply"])
            | (merged_df["dim_milking"] != merged_df["dim_apply"])
        ]

        # Create a new DataFrame that only keeps the rows in df_apply_lac_corr that need to be updated
        milking_update_db_data = df_apply_lac_corr[
            df_apply_lac_corr["animal_id"].isin(rows_to_update["animal_id"])
            & df_apply_lac_corr["milking_oid"].isin(rows_to_update["milking_oid"])
        ].copy()

        milking_update_db_data.drop(columns=["calving"], inplace=True)

        df_apply_lac_corr.started_at = df_apply_lac_corr.started_at.apply(
            pd.to_datetime
        )
        df_apply_lac_corr.ended_at = df_apply_lac_corr.ended_at.apply(pd.to_datetime)

        milking_update_new.started_at = milking_update_new.started_at.apply(
            pd.to_datetime
        )
        milking_update_new.ended_at = milking_update_new.ended_at.apply(pd.to_datetime)

        # Add the lactation_id, parity, and dim columns from df_apply_lac_corr to milking_update_new
        milking_update_new_data = milking_update_new.merge(
            df_apply_lac_corr[
                [
                    "farm_id",
                    "animal_id",
                    "milking_oid",
                    "started_at",
                    "ended_at",
                    "lactation_id",
                    "parity",
                    "dim",
                ]
            ],
            on=["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"],
        )

        milking_update_new_data = milking_update_new_data.loc[
            ~pd.isnull(milking_update_new_data.milking_oid)
        ]
        milking_update_new_data = milking_update_new_data.loc[
            ~pd.isnull(milking_update_new_data.animal_id)
        ]
        milking_update_new_data = milking_update_new_data.loc[
            ~pd.isnull(milking_update_new_data.lactation_id)
        ]

        milking_update_new_data["updated_on"] = dt.date.today()

        ################################################################################################################

        if len(milking_update_db_data) > 0:
            milking_update_db_data = milking_update_db_data[
                ~pd.isnull(milking_update_db_data.animal_id)
            ]
            milking_update_db_data = milking_update_db_data[
                ~pd.isnull(milking_update_db_data.lactation_id)
            ]
            milking_update_db_data.lactation_id = (
                milking_update_db_data.lactation_id.astype(int)
            )
            milking_update_db_data.loc[
                pd.isnull(milking_update_db_data.parity), "parity"
            ] = 0
            milking_update_db_data.parity = milking_update_db_data.parity.astype(int)
            # update milking table
            milking_sql = create_sql_update(
                sqlupdateDict["sql_update"]["milking_milking_table"]
            )

            db_connect.insert(
                query=milking_sql, data=milking_update_db_data.to_dict("records")
            )

        if len(milking_update_new_data) > 0:
            ################################################################################################################
            # if the milkings system oid is missing in the original backup data, create a new id, to indicate this and add the data regardsless to our database
            milking_update_new_data.loc[
                pd.isnull(milking_update_new_data.milking_system_oid),
                "milking_system_oid",
            ] = int(farm_id * 1000 + 999)

            ################################################################################################################
            # update milking system table
            milking_system_update = (
                milking_update_new_data[["farm_id", "milking_system_oid", "updated_on"]]
                .copy()
                .drop_duplicates(subset=["farm_id", "milking_system_oid"])
            )
            ms_update_sql = create_sql_insert_update(
                sqlupdateDict["sql_update"]["milking_system_milking_table"]
            )
            db_connect.insert(
                query=ms_update_sql, data=milking_system_update.to_dict("records")
            )

            ################################################################################################################
            # map milking system ids to milking system oids
            milking_system_ids = db_connect.query(
                query=f"""SELECT milking_system_id, milking_system_oid FROM milking_system WHERE farm_id = {farm_id};"""
            )

            dict_ms_ids = pd.Series(
                milking_system_ids.milking_system_id.values,
                index=milking_system_ids.milking_system_oid,
            ).to_dict()

            milking_update_new_data["milking_system_id"] = milking_update_new_data[
                "milking_system_oid"
            ].map(dict_ms_ids)

            milking_update_new_data = milking_update_new_data.drop(
                columns=["milking_system_oid"]
            )

            ################################################################################################################

            # insert new milkings into milking table
            datetime_columns = tableDict["milking"][f"{farmtype}_datetime"]
            for column in datetime_columns:
                milking_update_new_data[column] = pd.to_datetime(
                    milking_update_new_data[column]
                )
                milking_update_new_data[column] = milking_update_new_data[
                    column
                ].dt.strftime("%Y-%m-%d %H:%M:%S")
            milking_update_new_data.to_sql(
                "milking", con=db_connect.ret_con(), if_exists="append", index=False
            )

        ################################################################################################################
        # Step 12: Update corrected lactation information for other dataframes

        for table in ["bcs", "activity", "milkbiomarkers", "insemination"]:

            add_table_sql = f"""
            SELECT farm_id, animal_id, lactation_id, {table}_id, parity, dim, measured_on
            FROM {table}
            WHERE farm_id = {farm_id}
            ;
            """
            add_table_db = db_connect.query(query=add_table_sql)
            add_table_new = add_table_db.copy()

            if not add_table_db.empty:
                for lacids in list(
                    lactation_db.sort_values(by=["animal_id", "calving"]).lactation_id
                ):
                    aniid = lactation_db.loc[
                        lactation_db.lactation_id == lacids, "animal_id"
                    ].values[0]
                    calvingdate = (
                        lactation_db.loc[lactation_db.lactation_id == lacids, "calving"]
                        .apply(pd.to_datetime)
                        .values[0]
                    )
                    lacno = lactation_db.loc[
                        lactation_db.lactation_id == lacids, "parity"
                    ].values[0]
                    add_table_new.loc[
                        (add_table_new.animal_id == aniid)
                        & (add_table_new.measured_on >= calvingdate),
                        "lactation_id",
                    ] = lacids
                    add_table_new.loc[
                        (add_table_new.animal_id == aniid)
                        & (add_table_new.measured_on >= calvingdate),
                        "calvingdate",
                    ] = calvingdate
                    add_table_new.loc[
                        (add_table_new.animal_id == aniid)
                        & (add_table_new.measured_on >= calvingdate),
                        "parity",
                    ] = lacno
                # calculate the dim
                add_table_new["dim"] = (
                    add_table_new.measured_on
                    - pd.to_datetime(add_table_new.calvingdate, format="%Y-%m-%d")
                ) / np.timedelta64(1, "D")
                if table in ["bcs", "activity"]:
                    add_table_new = add_table_new.drop(columns=["calvingdate"])

                # Merge the DataFrames on animal_id and milking_oid
                merged_df = pd.merge(
                    add_table_db,
                    add_table_new,
                    on=["farm_id", "animal_id", f"{table}_id", "measured_on"],
                    suffixes=("_database", "_new"),
                )

                # Filter rows where lactation_id, parity, or dim differ
                rows_to_update = merged_df[
                    (
                        merged_df["lactation_id_database"]
                        != merged_df["lactation_id_new"]
                    )
                    | (merged_df["parity_database"] != merged_df["parity_new"])
                    | (merged_df["dim_database"] != merged_df["dim_new"])
                ]

                # Create a new DataFrame that only keeps the rows in add_table_new that need to be updated
                add_table_new = add_table_new[
                    add_table_new["animal_id"].isin(rows_to_update["animal_id"])
                    & add_table_new[f"{table}_id"].isin(rows_to_update[f"{table}_id"])
                ].copy()

                add_table_new = add_table_new[~pd.isnull(add_table_new.animal_id)]
                add_table_new = add_table_new[~pd.isnull(add_table_new.lactation_id)]
                add_table_new.lactation_id = add_table_new.lactation_id.astype(int)
                add_table_new.loc[pd.isnull(add_table_new.parity), "parity"] = 0
                add_table_new.parity = add_table_new.parity.astype(int)

                if not add_table_new.empty:
                    # update milking table
                    update_sql = create_sql_update(
                        sqlupdateDict["sql_update"][f"milking_{table}_table"]
                    )

                    db_connect.insert(
                        query=update_sql, data=add_table_new.to_dict("records")
                    )


def lactationCorrection(
    db_connect,
    farm_id: int,
    farmtype: str,
    sqlupdateDict: dict,
    tableDict: dict,
) -> None:
    """
    Update milking table

    Parameters
    ----------
    db_connect : sql engine
        engine to connect ot database
    farm_id : integer
        id of farm for which data is processed
    farmname : str
        name of farm for which data is processed
    farmtype : str
        milking system identifier (d- delaval, l- lely)
    sqlupdateDict : dict
        dictionary containing information to generate a sql statement
    tableDict : dict
        dictionary containing information about the table schema of the target database
    """

    milking_sql = f"""
    SELECT farm_id, animal_id, milking_oid, started_at, ended_at, tmy
    FROM milking
    WHERE farm_id = {farm_id}
    ;
    """
    milking_db = db_connect.query(query=milking_sql)

    milking_db.started_at = milking_db.started_at.apply(pd.to_datetime)
    milking_db.ended_at = milking_db.ended_at.apply(pd.to_datetime)

    ################################################################################################################
    # apply lactation_ids, parities and calving dates to milking_update_new

    lactation_sql = f"""
    SELECT farm_id, animal_id, lactation_oid, calving, dry_off, parity
    FROM lactation
    WHERE farm_id = {farm_id}
    ;
    """
    lactation_db = db_connect.query(query=lactation_sql)

    animal_sql = f"""
    SELECT farm_id, animal_id, animal_oid, birth_date
    FROM animal
    WHERE farm_id = {farm_id}
    ;
    """
    animal_db = db_connect.query(query=animal_sql)

    ################################################################################################################
    # Lactation correction (farm level)
    ################################################################################################################
    # Step 1: Identify gaps in data at farm level

    if len(milking_db) > 0:
        df_farmgap_det = milking_db[["animal_id", "started_at"]].copy()
    else:
        return
    df_farmgap_det["started_at"] = pd.to_datetime(df_farmgap_det.loc[:, "started_at"])
    df_farmgap_det = df_farmgap_det.loc[
        (df_farmgap_det.started_at > dt.datetime(2000, 1, 1))
        & (df_farmgap_det.started_at <= dt.datetime.today())
    ]

    start_date_farm = df_farmgap_det.started_at.min()
    # Calculate the minimum started_at for each animal_id
    start_date_animals = df_farmgap_det.groupby('animal_id')['started_at'].min()

    # Convert started_at to date, drop duplicates
    df_farmgap_det.started_at = df_farmgap_det.started_at.dt.date
    df_farmgap_det = df_farmgap_det.drop_duplicates()
    df_farmgap_det = df_farmgap_det.groupby(by="started_at").count().reset_index()

    # sort milk data and calculate gaps
    df_farmgap_det = df_farmgap_det.sort_values(by=["started_at"]).reset_index(
        drop=True
    )
    df_farmgap_det["gap"] = df_farmgap_det.started_at.diff().dt.total_seconds() / 86400

    df_farmgap_det.loc[pd.isnull(df_farmgap_det.gap), "gap"] = 0
    df_farmgap_det.loc[df_farmgap_det.gap < 2, "gap"] = 0
    df_farmgap_det.loc[df_farmgap_det.gap > 0, "gap"] = 1

    # define periods restricted by gaps of at least 2 days
    df_farmgap_det["periods"] = df_farmgap_det.gap.cumsum()

    farm_gaps = pd.DataFrame(columns=["gap", "gap_start", "gap_end", "gap_length"])
    if df_farmgap_det.periods.max() > 0:
        for i in range(int(df_farmgap_det.periods.max())):
            gap = int(i + 1)
            gap_start = df_farmgap_det.loc[
                df_farmgap_det.periods == i, "started_at"
            ].max()
            gap_end = df_farmgap_det.loc[
                df_farmgap_det.periods == i + 1, "started_at"
            ].min()
            gap_length = gap_end - gap_start
            farm_gaps.loc[len(farm_gaps.index)] = [
                gap,
                gap_start,
                gap_end,
                gap_length,
            ]

    ################################################################################################################
    # Step 2: Remove too short lactation lengths indicated by the farmer
    # (remove both the lactations that are indicated as too close together)
    df_lac_farm_corr = lactation_db.copy()
    df_lac_farm_corr["calving"] = pd.to_datetime(df_lac_farm_corr.loc[:, "calving"])
    df_lac_farm_corr["dry_off"] = pd.to_datetime(df_lac_farm_corr.loc[:, "dry_off"])
    df_lac_farm_corr = df_lac_farm_corr.loc[
        (df_lac_farm_corr.calving > dt.datetime(2000, 1, 1))
        & (df_lac_farm_corr.calving <= dt.datetime.today())
    ].sort_values(by=["animal_id", "calving"])
    df_lac_farm_corr["prev_lactation_length"] = df_lac_farm_corr.groupby(
        by="animal_id"
    ).calving.diff()
    # Convert Timedelta to float (total seconds) and handle NaN values
    df_lac_farm_corr["prev_lactation_length"] = df_lac_farm_corr[
        "prev_lactation_length"
    ].apply(lambda x: x.total_seconds() / 86400 if pd.notnull(x) else None)
    # Shift the lactation_length column one row back within each animal_id group
    df_lac_farm_corr["lactation_length"] = df_lac_farm_corr.groupby("animal_id")[
        "prev_lactation_length"
    ].shift(-1)
    df_lac_farm_corr = df_lac_farm_corr.loc[
        (
            pd.isnull(df_lac_farm_corr.prev_lactation_length)
            & (df_lac_farm_corr.lactation_length >= 150)
        )
        | (
            pd.isnull(df_lac_farm_corr.lactation_length)
            & (df_lac_farm_corr.prev_lactation_length >= 150)
        )
        | (
            pd.isnull(df_lac_farm_corr.prev_lactation_length)
            & pd.isnull(df_lac_farm_corr.lactation_length)
        )
        | (
            (df_lac_farm_corr.prev_lactation_length >= 150)
            & (df_lac_farm_corr.lactation_length >= 150)
        )
    ]
    df_lac_farm_corr.loc[df_lac_farm_corr.parity >= 20, "parity"] = None

    ################################################################################################################
    # Step 3: Identify gaps in milking data

    if len(milking_db) > 0:
        df_milkgap_det = milking_db[["animal_id", "started_at", "tmy"]].copy()
    else:
        return
    df_milkgap_det = df_milkgap_det.loc[~pd.isnull(df_milkgap_det.tmy)]
    df_milkgap_det = df_milkgap_det[["animal_id", "started_at"]]
    df_milkgap_det["started_at"] = pd.to_datetime(df_milkgap_det["started_at"])
    df_milkgap_det = df_milkgap_det.loc[
        (df_milkgap_det.started_at > dt.datetime(2000, 1, 1))
        & (df_milkgap_det.started_at <= dt.datetime.today())
    ]

    # sort milk data and calculate gaps
    df_milkgap_det = df_milkgap_det.sort_values(
        by=["animal_id", "started_at"]
    ).reset_index(drop=True)
    df_milkgap_det["gap"] = (
        df_milkgap_det.groupby(by="animal_id").started_at.diff().dt.total_seconds()
        / 86400
    )

    df_milkgap_det.loc[pd.isnull(df_milkgap_det.gap), "gap"] = 0
    df_milkgap_det.loc[df_milkgap_det.gap < 14, "gap"] = 0
    df_milkgap_det.loc[df_milkgap_det.gap > 0, "gap"] = 1

    # define periods restricted by gaps of at least 10 days
    df_milkgap_det["periods"] = df_milkgap_det.groupby(by="animal_id").gap.cumsum()

    # define the calculated calving date as the date of the first milking in each period
    df_milkgap_det["calving"] = df_milkgap_det.groupby(
        by=["animal_id", "periods"]
    ).started_at.transform("min")
    df_milkgap_det["calving"] = df_milkgap_det["calving"]

    # define the calculated dry off date as the date of the last milking in each period
    df_milkgap_det["dry_off"] = df_milkgap_det.groupby(
        by=["animal_id", "periods"]
    ).started_at.transform("max")
    df_milkgap_det["dry_off"] = df_milkgap_det["dry_off"]

    # # Remove each first calving as it is likely to be the first available data not the true calving date
    # df_milkgap_det = df_milkgap_det.loc[df_milkgap_det.periods > 0]

    df_lac_corrected_2 = (
        df_milkgap_det[["animal_id", "calving", "dry_off"]].copy().drop_duplicates()
    )

    # Set each last available dry off for each cow to None, as we can not be sure if this is due to the data period ending or a true dry off
    # Sort by animal_id and calving in descending order
    df_lac_corrected_2.sort_values(
        ["animal_id", "calving"], ascending=[True, False], inplace=True
    )

    # Set the 'dry_off' of the first entry of each 'animal_id' group to None
    df_lac_corrected_2.loc[
        df_lac_corrected_2.dry_off
        >= (df_lac_corrected_2.dry_off.max() - dt.timedelta(days=30)),
        "dry_off",
    ] = None

    # df_lac_corrected_2.sort_values(by=["animal_id", "calving"], inplace=True)

    ################################################################################################################
    # Step 4: Remove gaps that coincide with missing data on farm level
    df_lac_corrected_1 = df_lac_farm_corr[
        ["animal_id", "parity", "calving", "dry_off"]
    ].copy()
    df_lac_corrected_1.loc[:, "reported"] = "farmer"
    df_lac_corrected_2.loc[:, "reported"] = "gap_detection"
    df_lac_corrected = pd.concat([df_lac_corrected_1, df_lac_corrected_2])

    # Remove gaps detected that coincide with missing data on farm level

    if farm_gaps.empty == False:
        for i in list(farm_gaps.gap):
            farmgap_start = pd.to_datetime(
                farm_gaps.loc[farm_gaps.gap == i, "gap_start"]
            ).values[0]
            farmgap_end = pd.to_datetime(
                farm_gaps.loc[farm_gaps.gap == i, "gap_end"]
            ).values[0]
            df_lac_corrected = df_lac_corrected.loc[
                (
                    (df_lac_corrected.reported == "gap_detection")
                    & (
                        (df_lac_corrected.calving < farmgap_start)
                        | (df_lac_corrected.calving > farmgap_end)
                    )
                )
                | (df_lac_corrected.reported == "farmer")
            ]

    # Calculate period between (potential) calvings

    df_lac_corrected = df_lac_corrected.sort_values(by=["animal_id", "calving"])
    df_lac_corrected["gap_prev"] = (
        df_lac_corrected.groupby(by="animal_id")
        .calving.diff()
        .apply(lambda x: x.total_seconds() / 86400 if pd.notnull(x) else None)
    )
    df_lac_corrected["gap_next"] = (
        df_lac_corrected.groupby(by="animal_id")
        .calving.diff(periods=-1)
        .apply(lambda x: x.total_seconds() / 86400 if pd.notnull(x) else None)
    )

    ################################################################################################################
    # Step 5: Check which calvings are present in both the farmer reported dataset and the on gaps-detection based dataset
    df_lac_corrected2 = df_lac_corrected.copy().reset_index()

    # Convert to datetime if not already
    df_lac_corrected2["calving"] = pd.to_datetime(df_lac_corrected2["calving"])
    df_lac_corrected2["dry_off"] = pd.to_datetime(df_lac_corrected2["dry_off"])

    # Sort by animal_id and calving
    df_lac_corrected2.sort_values(["animal_id", "calving"], inplace=True)

    # Create calving_period column
    df_lac_corrected2["calving_prev"] = df_lac_corrected2.groupby(
        by="animal_id"
    ).calving.shift(1)
    df_lac_corrected2["reported_prev"] = df_lac_corrected2.groupby(
        by="animal_id"
    ).reported.shift(1)

    df_lac_corrected2["pres_calving"] = df_lac_corrected2["calving"]
    df_lac_corrected2.loc[
        (df_lac_corrected2.gap_prev < 10)
        & (df_lac_corrected2.reported != df_lac_corrected2.reported_prev),
        "pres_calving",
    ] = df_lac_corrected2["calving_prev"]

    # Create separate dataframes for farmer and gap_detection
    df_farmer = df_lac_corrected2[df_lac_corrected2["reported"] == "farmer"].copy()
    df_gap_detection = df_lac_corrected2[
        df_lac_corrected2["reported"] == "gap_detection"
    ].copy()

    # Merge the dataframes
    df_merged = pd.merge(
        df_farmer,
        df_gap_detection,
        on=["animal_id", "pres_calving"],
        how="outer",
        suffixes=("_farmer", "_gap_detection"),
    )

    # Combine the data
    df_merged["calving"] = df_merged[["calving_farmer", "calving_gap_detection"]].min(
        axis=1
    )
    df_merged["dry_off"] = df_merged["dry_off_gap_detection"].fillna(
        df_merged["dry_off_farmer"]
    )
    df_merged["parity"] = df_merged["parity_gap_detection"].combine_first(
        df_merged["parity_farmer"]
    )
    df_merged["reported"] = df_merged.apply(
        lambda row: (
            "both"
            if pd.notnull(row["reported_farmer"])
            and pd.notnull(row["reported_gap_detection"])
            else (
                row["reported_farmer"]
                if pd.notnull(row["reported_farmer"])
                else row["reported_gap_detection"]
            )
        ),
        axis=1,
    )

    # Keep only the necessary columns
    df_merged = df_merged[
        ["animal_id", "calving", "dry_off", "parity", "reported"]
    ].sort_values(by=["animal_id", "calving"])

    df_merged["gap_prev"] = (
        df_merged.groupby(by="animal_id").calving.diff().dt.total_seconds() / 86400
    )
    df_merged["gap_next"] = (
        df_merged.groupby(by="animal_id").calving.diff(periods=-1).dt.total_seconds()
        / 86400
    )
    df_merged["dry_off_prev"] = df_merged.groupby(by="animal_id").dry_off.shift(1)

    ################################################################################################################
    # Step 6: Remove potential calvings detected by gap-detection if they are too close to a prior/next lactation (i.e. do not make sense with the given pregnancy length)

    df_merged = df_merged.loc[
        (df_merged.reported == "both")
        | (df_merged.reported == "farmer")
        | (
            (df_merged.reported == "gap_detection")
            & (
                (df_merged.calving >= df_merged.dry_off_prev)
                | pd.isnull(df_merged.dry_off_prev)
            )
            & (df_merged.gap_prev >= 270)
            & ((df_merged.gap_next <= -270) | pd.isnull(df_merged.gap_next))
            & (df_merged.calving >= start_date_farm + dt.timedelta(days=365))
            & (df_merged.apply(lambda row: row.calving >= (start_date_animals[row.animal_id] if row.animal_id in start_date_animals else start_date_farm) + dt.timedelta(days=365), axis=1))
        )
    ]

    ################################################################################################################
    # Step 7: Add the birth date and correct for first recorded lactaitons where no parity number is available
    # (guess based on median distribution of age at calving for the farm)

    df_animal_info = animal_db[["animal_id", "birth_date"]].copy()
    df_animal_info["birth_date"] = pd.to_datetime(df_animal_info["birth_date"])

    df_lac_final = df_merged.merge(df_animal_info, on="animal_id")
    df_lac_final = df_lac_final.loc[df_lac_final.calving != df_lac_final.birth_date]
    df_lac_final["birth_to_parity"] = (
        df_lac_final.calving - df_lac_final.birth_date
    ).dt.total_seconds() / 86400

    # Calculate a dictionary defining thresholds to apply to lactations without parity information
    parity_dict = (
        df_lac_final.groupby(by="parity")
        .birth_to_parity.median()
        .reset_index()
        .sort_values("parity")
        .reset_index(drop=True)
    )
    parity_dict = (
        parity_dict.loc[parity_dict.parity > 0]
        .sort_values("parity")
        .reset_index(drop=True)
    )
    parity_dict = parity_dict.loc[parity_dict.parity == parity_dict.index + 1]
    parity_dict["parity_lowerlimit"] = parity_dict.rolling(2).birth_to_parity.mean()
    parity_dict["parity_upperlimit"] = parity_dict["parity_lowerlimit"].shift(-1)
    parity_dict.loc[parity_dict.parity == 1, "parity_lowerlimit"] = 0
    parity_dict.loc[
        parity_dict.parity == parity_dict.parity.max(), "parity_upperlimit"
    ] = df_lac_final.birth_to_parity.max()

    # Apply parity information to final lactation table
    for i in parity_dict.parity:
        par_ll = parity_dict.loc[parity_dict.parity == i, "parity_lowerlimit"].iloc[0]
        par_ul = parity_dict.loc[parity_dict.parity == i, "parity_upperlimit"].iloc[0]
        df_lac_final.loc[
            pd.isnull(df_lac_final.parity)
            & (
                (df_lac_final.calving - df_lac_final.birth_date).dt.total_seconds()
                / 86400
                > par_ll
            )
            & (
                (df_lac_final.calving - df_lac_final.birth_date).dt.total_seconds()
                / 86400
                <= par_ul
            ),
            "parity",
        ] = i

    df_lac_final.reset_index(inplace=True, drop=True)

    ################################################################################################################
    # Step 8: Check if consecutive lactations have consecutive parity numbers

    # Check if consecutive entries have consecutive lactation numbers, correct otherwise
    for index, row in df_lac_final.iterrows():
        if index == 0:
            continue
        if (
            (
                df_lac_final.loc[index, "animal_id"]
                == df_lac_final.loc[index - 1, "animal_id"]
            )
            and (
                df_lac_final.loc[index, "parity"]
                != df_lac_final.loc[index - 1, "parity"] + 1
            )
            and (
                (
                    (
                        df_lac_final.loc[index, "calving"]
                        - df_lac_final.loc[index - 1, "calving"]
                    ).total_seconds()
                    / 86400
                )
                < 700
            )
        ):
            df_lac_final.loc[index, "parity"] = (
                df_lac_final.loc[index - 1, "parity"] + 1
            )

    ################################################################################################################
    # Step 9: Create final set of corrected lactation parameters

    df_lac_final = df_lac_final[
        ["animal_id", "birth_date", "calving", "dry_off", "parity", "reported"]
    ]

    df_lac_final["lactation_length"] = np.round(
        (df_lac_final.dry_off - df_lac_final.calving).dt.total_seconds() / 86400,
        decimals=2,
    )
    df_lac_final.loc[df_lac_final.lactation_length <= 250, "dry_off"] = None
    df_lac_final["lactation_length"] = np.round(
        (df_lac_final.dry_off - df_lac_final.calving).dt.total_seconds() / 86400,
        decimals=2,
    )
    df_lac_final["calving_prev"] = df_lac_final.groupby(by="animal_id").calving.shift(1)
    df_lac_final["dry_off_prev"] = df_lac_final.groupby(by="animal_id").dry_off.shift(1)
    df_lac_final["dry_period_prev"] = np.round(
        (df_lac_final.calving - df_lac_final.dry_off_prev).dt.total_seconds() / 86400,
        decimals=2,
    )
    df_lac_final["lactation_length_prev"] = np.round(
        (df_lac_final.dry_off_prev - df_lac_final.calving_prev).dt.total_seconds()
        / 86400,
        decimals=2,
    )
    df_lac_final["farm_id"] = farm_id
    df_lac_final.loc[df_lac_final.parity == 1, "age_at_first_calving"] = np.round(
        (
            df_lac_final.loc[df_lac_final.parity == 1, "calving"]
            - df_lac_final.loc[df_lac_final.parity == 1, "birth_date"]
        ).dt.total_seconds()
        / 86400,
        decimals=2,
    )
    df_lac_final["age_at_first_calving"] = df_lac_final.groupby("animal_id")[
        "age_at_first_calving"
    ].transform(lambda x: x.min(skipna=True))

    ################################################################################################################
    # Step 10: Update corrected lactation information to database

    # update lactation table
    df_lac_final.loc[pd.isnull(df_lac_final.parity)] = 0
    df_lac_final.parity = df_lac_final.parity.astype(int)
    df_lac_final["updated_on"] = dt.date.today()

    df_lac_final["birth_date"] = pd.to_datetime(df_lac_final.loc[:, "birth_date"])
    df_lac_final["calving"] = pd.to_datetime(df_lac_final.loc[:, "calving"])
    df_lac_final["dry_off"] = pd.to_datetime(df_lac_final.loc[:, "dry_off"])
    df_lac_final["calving_prev"] = pd.to_datetime(df_lac_final.loc[:, "calving_prev"])
    df_lac_final["dry_off_prev"] = pd.to_datetime(df_lac_final.loc[:, "dry_off_prev"])
    datetime_columns = tableDict["lactation_corrected"][f"{farmtype}_datetime"]
    for column in datetime_columns:
        df_lac_final[column] = df_lac_final[column].dt.strftime("%Y-%m-%d %H:%M:%S")
    df_lac_final = df_lac_final.where(pd.notnull(df_lac_final), None)
    df_lac_final = df_lac_final.loc[df_lac_final.farm_id == farm_id]

    # Fetch data from lactation_corrected table
    lac_corr_sql = f"SELECT * FROM lactation_corrected WHERE farm_id={farm_id}"
    lactation_corrected = db_connect.query(query=lac_corr_sql)

    # Merge to find differences based on farm_id, animal_id, and parity
    merged_diff = lactation_corrected.merge(
        df_lac_final, on=["farm_id", "animal_id", "parity"], how="outer", indicator=True
    )

    # Rows in lactation_corrected but not in df_lac_final
    rows_to_delete = merged_diff[merged_diff["_merge"] == "left_only"]

    # Update parity to 99 in lactation_corrected for rows not in df_lac_final
    # Track the current parity for each (farm_id, animal_id) combination
    current_parity = {}

    for index, row in rows_to_delete.iterrows():
        key = (row["farm_id"], row["animal_id"])

        # Initialize the parity if the key is not in the dictionary
        if key not in current_parity:
            if row["animal_id"] not in lactation_corrected["animal_id"].values:
                current_parity[key] = 99
            else:
                current_parity[key] = int(lactation_corrected.loc[
                    (lactation_corrected["farm_id"] == row["farm_id"]) &
                    (lactation_corrected["animal_id"] == row["animal_id"]),
                    "parity"
                ].max() + 1)
        else:
            # Increment the parity for subsequent entries
            current_parity[key] += 1

        update_sql = f"""
        UPDATE lactation_corrected 
        SET parity = {current_parity[key]}
        WHERE farm_id = '{row['farm_id']}' 
        AND animal_id = '{row['animal_id']}' 
        AND parity = {row['parity']}
        """
        db_connect.execute(update_sql)

    lactation_sql = create_sql_insert_update(
        sqlupdateDict["sql_update"]["corrected_lactation_update"]
    )
    db_connect.insert(query=lactation_sql, data=df_lac_final.to_dict("records"))

    ################################################################################################################
    # Step 11: Apply corrected lactation information to milking data

    # add the lactation_ids back to the milking dataframe
    lactation_db = db_connect.query(
        query=f"""SELECT lactation_id, animal_id, parity, calving FROM lactation_corrected WHERE farm_id = {farm_id} AND parity < 99;"""
    )

    milking_sql = f"""
    SELECT farm_id, animal_id, lactation_id, milking_oid, parity, dim, started_at, ended_at
    FROM milking
    WHERE farm_id = {farm_id}
    ;
    """
    milking_db = db_connect.query(query=milking_sql)

    milking_db.started_at = milking_db.started_at.apply(pd.to_datetime)
    milking_db.ended_at = milking_db.ended_at.apply(pd.to_datetime)

    df_apply_lac_corr = milking_db[
        ["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"]
    ].copy()
    df_apply_lac_corr.started_at = df_apply_lac_corr.started_at.apply(pd.to_datetime)
    df_apply_lac_corr.ended_at = df_apply_lac_corr.ended_at.apply(pd.to_datetime)

    for lacids in lactation_db.sort_values(
        by=["animal_id", "parity"]
    ).lactation_id.unique():
        aniid = lactation_db.loc[
            lactation_db.lactation_id == lacids, "animal_id"
        ].values[0]
        calvingdate = (
            lactation_db.loc[lactation_db.lactation_id == lacids, "calving"]
            .apply(pd.to_datetime)
            .values[0]
        )
        if calvingdate == None:  # fixing error when calvingdate == None
            calvingdate = df_apply_lac_corr.loc[
                (df_apply_lac_corr.animal_id == aniid), "started_at"
            ].min()

        lacno = lactation_db.loc[lactation_db.lactation_id == lacids, "parity"].values[
            0
        ]
        df_apply_lac_corr.loc[
            (df_apply_lac_corr.animal_id == aniid)
            & (df_apply_lac_corr.started_at >= calvingdate),
            "lactation_id",
        ] = lacids
        df_apply_lac_corr.loc[
            (df_apply_lac_corr.animal_id == aniid)
            & (df_apply_lac_corr.started_at >= calvingdate),
            "parity",
        ] = lacno
        df_apply_lac_corr.loc[
            (df_apply_lac_corr.animal_id == aniid)
            & (df_apply_lac_corr.started_at >= calvingdate),
            "calving",
        ] = calvingdate

    # Calculate new DIM
    df_apply_lac_corr.loc[
        ~pd.isnull(df_apply_lac_corr.ended_at) & ~pd.isnull(df_apply_lac_corr.calving),
        "dim",
    ] = (
        (
            df_apply_lac_corr.loc[
                ~pd.isnull(df_apply_lac_corr.ended_at)
                & ~pd.isnull(df_apply_lac_corr.calving),
                "ended_at",
            ].apply(pd.to_datetime)
            - df_apply_lac_corr.loc[
                ~pd.isnull(df_apply_lac_corr.ended_at)
                & ~pd.isnull(df_apply_lac_corr.calving),
                "calving",
            ].apply(pd.to_datetime)
        ).dt.total_seconds()
        / 86400
    ).round(
        decimals=2
    )

    # drop the data that was already available in the database
    df_apply_lac_corr["updated_on"] = dt.date.today()

    # Merge the DataFrames on animal_id and milking_oid
    merged_df = pd.merge(
        milking_db,
        df_apply_lac_corr,
        on=["farm_id", "animal_id", "milking_oid", "started_at", "ended_at"],
        suffixes=("_milking", "_apply"),
    )

    # Filter rows where lactation_id, parity, or dim differ
    rows_to_update = merged_df[
        (merged_df["lactation_id_milking"] != merged_df["lactation_id_apply"])
        | (merged_df["parity_milking"] != merged_df["parity_apply"])
        | (merged_df["dim_milking"] != merged_df["dim_apply"])
    ]

    # Create a new DataFrame that only keeps the rows in df_apply_lac_corr that need to be updated
    milking_update_db_data = df_apply_lac_corr[
        df_apply_lac_corr["animal_id"].isin(rows_to_update["animal_id"])
        & df_apply_lac_corr["milking_oid"].isin(rows_to_update["milking_oid"])
    ].copy()

    milking_update_db_data.drop(columns=["calving"], inplace=True)

    df_apply_lac_corr.started_at = df_apply_lac_corr.started_at.apply(pd.to_datetime)
    df_apply_lac_corr.ended_at = df_apply_lac_corr.ended_at.apply(pd.to_datetime)

    ################################################################################################################

    if len(milking_update_db_data) > 0:
        milking_update_db_data = milking_update_db_data[
            ~pd.isnull(milking_update_db_data.animal_id)
        ]
        milking_update_db_data = milking_update_db_data[
            ~pd.isnull(milking_update_db_data.lactation_id)
        ]
        milking_update_db_data.lactation_id = (
            milking_update_db_data.lactation_id.astype(int)
        )
        milking_update_db_data.loc[
            pd.isnull(milking_update_db_data.parity), "parity"
        ] = 0
        milking_update_db_data.parity = milking_update_db_data.parity.astype(int)
        # update milking table
        milking_sql = create_sql_update(
            sqlupdateDict["sql_update"]["milking_milking_table"]
        )
        if len(milking_update_db_data) > 0:
            db_connect.insert(
                query=milking_sql, data=milking_update_db_data.to_dict("records")
            )

    ################################################################################################################
    # Step 12: Update corrected lactation information for other dataframes

    for table in ["bcs", "activity", "milkbiomarkers", "insemination"]:

        add_table_sql = f"""
        SELECT farm_id, animal_id, lactation_id, {table}_id, parity, dim, measured_on
        FROM {table}
        WHERE farm_id = {farm_id}
        ;
        """
        add_table_db = db_connect.query(query=add_table_sql)
        add_table_new = add_table_db.copy()

        if not add_table_db.empty:
            for lacids in list(
                lactation_db.sort_values(by=["animal_id", "calving"]).lactation_id
            ):
                aniid = lactation_db.loc[
                    lactation_db.lactation_id == lacids, "animal_id"
                ].values[0]
                calvingdate = (
                    lactation_db.loc[lactation_db.lactation_id == lacids, "calving"]
                    .apply(pd.to_datetime)
                    .values[0]
                )
                lacno = lactation_db.loc[
                    lactation_db.lactation_id == lacids, "parity"
                ].values[0]
                add_table_new.loc[
                    (add_table_new.animal_id == aniid)
                    & (add_table_new.measured_on >= calvingdate),
                    "lactation_id",
                ] = lacids
                add_table_new.loc[
                    (add_table_new.animal_id == aniid)
                    & (add_table_new.measured_on >= calvingdate),
                    "calvingdate",
                ] = calvingdate
                add_table_new.loc[
                    (add_table_new.animal_id == aniid)
                    & (add_table_new.measured_on >= calvingdate),
                    "parity",
                ] = lacno
            # calculate the dim
            add_table_new["dim"] = (
                add_table_new.measured_on
                - pd.to_datetime(add_table_new.calvingdate, format="%Y-%m-%d")
            ) / np.timedelta64(1, "D")
            if table in ["bcs", "activity"]:
                add_table_new = add_table_new.drop(columns=["calvingdate"])

            # Merge the DataFrames on animal_id and milking_oid
            merged_df = pd.merge(
                add_table_db,
                add_table_new,
                on=["farm_id", "animal_id", f"{table}_id", "measured_on"],
                suffixes=("_database", "_new"),
            )

            # Filter rows where lactation_id, parity, or dim differ
            rows_to_update = merged_df[
                (merged_df["lactation_id_database"] != merged_df["lactation_id_new"])
                | (merged_df["parity_database"] != merged_df["parity_new"])
                | (merged_df["dim_database"] != merged_df["dim_new"])
            ]

            # Create a new DataFrame that only keeps the rows in add_table_new that need to be updated
            add_table_new = add_table_new[
                add_table_new["animal_id"].isin(rows_to_update["animal_id"])
                & add_table_new[f"{table}_id"].isin(rows_to_update[f"{table}_id"])
            ].copy()

            add_table_new = add_table_new[~pd.isnull(add_table_new.animal_id)]
            add_table_new = add_table_new[~pd.isnull(add_table_new.lactation_id)]
            add_table_new = add_table_new[~pd.isnull(add_table_new.dim)]
            add_table_new.lactation_id = add_table_new.lactation_id.astype(int)
            add_table_new.loc[pd.isnull(add_table_new.parity), "parity"] = 0
            add_table_new.parity = add_table_new.parity.astype(int)

            if not add_table_new.empty:
                # update milking table
                update_sql = create_sql_update(
                    sqlupdateDict["sql_update"][f"milking_{table}_table"]
                )

                db_connect.insert(
                    query=update_sql, data=add_table_new.to_dict("records")
                )


def mapMilkingSystem(df_data: pd.DataFrame, db_connect, farm_id: int) -> pd.DataFrame:
    """
    Update milking system table

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    farm_id : integer
        id of farm for which data is processed

    Return
    ------
    df_data : pandas dataframe
        dataframe with new milking_system_ids
    """
    milking_system_ids = db_connect.query(
        query=f"""SELECT milking_system_id, milking_system_oid FROM milking_system WHERE farm_id = {farm_id};"""
    )

    dict_ms_ids = pd.Series(
        milking_system_ids.milking_system_id.values,
        index=milking_system_ids.milking_system_oid,
    ).to_dict()

    ################################################################################################################
    # if the milkings system oid is missing in the original backup data, create a new id, to indicate this and add the data regardsless to our database
    df_data.loc[pd.isnull(df_data.milking_system_oid), "milking_system_oid"] = int(
        farm_id * 1000 + 999
    )

    df_data["milking_system_id"] = df_data["milking_system_oid"].map(dict_ms_ids)
    df_data.milking_system_id = df_data.milking_system_id.astype(float).astype("Int64")

    df_data = df_data.drop(columns=["milking_system_oid"])
    return df_data


def mapAnimalid(df_data: pd.DataFrame, db_connect, farm_id: int) -> pd.DataFrame:
    """
    Map new animal_ids to the animal_id used on the farm

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    farm_id : int
        id of farm for which data is processed

    Return
    ------
    df_data : pandas dataframe
        dataframe with new animal_ids
    """
    animal_ids = db_connect.query(
        query=f"""SELECT animal_id, animal_oid FROM animal WHERE farm_id = {farm_id};"""
    )

    dict_animal_ids = pd.Series(
        animal_ids.animal_id.values, index=animal_ids.animal_oid
    ).to_dict()

    df_data["animal_id"] = df_data["animal_oid"].map(dict_animal_ids)

    df_data = df_data.drop(columns=["animal_oid"])
    return df_data


def mapLactationid(
    df_data: pd.DataFrame, db_connect, farm_id: int, tablename: str
) -> pd.DataFrame:
    """
    Map new lactation_ids to the lactation_id used on the farm

    Parameters
    ----------
    df_data : pandas dataframe
        dataframe for a single table
    db_connect : sql engine
        engine to connect ot database
    farm_id : integer
        id of farm for which data is processed
    tablename : str
        name of the table/file

    Return
    ------
    df_data : pandas dataframe
        dataframe with new lactation_ids
    """
    lactation_sql = f"""
    SELECT farm_id, animal_id, lactation_id, calving, parity
    FROM lactation_corrected
    WHERE farm_id = {farm_id}
    ;
    """
    lactation_db = db_connect.query(query=lactation_sql)

    for lacids in list(
        lactation_db.sort_values(by=["animal_id", "calving"]).lactation_id
    ):
        aniid = lactation_db.loc[
            lactation_db.lactation_id == lacids, "animal_id"
        ].values[0]
        calvingdate = (
            lactation_db.loc[lactation_db.lactation_id == lacids, "calving"]
            .apply(pd.to_datetime)
            .values[0]
        )
        lacno = lactation_db.loc[lactation_db.lactation_id == lacids, "parity"].values[
            0
        ]
        df_data.loc[
            (df_data.animal_id == aniid) & (df_data.measured_on >= calvingdate),
            "lactation_id",
        ] = lacids
        df_data.loc[
            (df_data.animal_id == aniid) & (df_data.measured_on >= calvingdate),
            "calvingdate",
        ] = calvingdate
        df_data.loc[
            (df_data.animal_id == aniid) & (df_data.measured_on >= calvingdate),
            "parity",
        ] = lacno
    # calculate the dim
    df_data["dim"] = (
        df_data.measured_on - pd.to_datetime(df_data.calvingdate, format="%Y-%m-%d")
    ) / np.timedelta64(1, "D")
    if tablename in ["bcs", "activity"]:
        df_data = df_data.drop(columns=["calvingdate"])
    return df_data


def updateFarmLocation(db_connect, sqlupdateDict: dict, anonymized: bool) -> None:
    """
    Update farm location

    Parameters
    ----------
    db_connect : sql engine
        engine to connect ot database
    sqlupdateDict : dict
        dictionary containing information to generate a sql statement
    anonymized : bool
        anonlymize farm location (in a radius of 5 km around original location)
    """
    farm_sql = """
            SELECT *
            FROM farm
            ;
            """
    farm_db = db_connect.query(query=farm_sql)

    dict_farmlocation = sqlupdateDict["farminfo"]["farm_location"]

    dict_farm_lat = dict(
        zip(
            dict_farmlocation.keys(),
            list(list(zip(*list(dict_farmlocation.values())))[0]),
        )
    )
    dict_farm_long = dict(
        zip(
            dict_farmlocation.keys(),
            list(list(zip(*list(dict_farmlocation.values())))[1]),
        )
    )
    dict_farm_alt = dict(
        zip(
            dict_farmlocation.keys(),
            list(list(zip(*list(dict_farmlocation.values())))[2]),
        )
    )

    farm_db["longitude"] = farm_db["farmname"].map(dict_farm_long)
    farm_db["latitude"] = farm_db["farmname"].map(dict_farm_lat)
    farm_db["altitude"] = farm_db["farmname"].map(dict_farm_alt)

    if anonymized == True:
        for index, row in farm_db.iterrows():
            rand_dist = random.randint(0, 2 * np.pi)
            rand_long = np.sin(rand_dist) * 0.1
            rand_lat = np.cos(rand_dist) * 0.1
            farm_db.loc[farm_db.index == index, "longitude"] += rand_long
            farm_db.loc[farm_db.index == index, "latitude"] += rand_lat

    #########################################################################################################################
    # Update database table 'aws' with weather data

    farm_db["updated_on"] = dt.date.today()

    farm_update_sql = create_sql_update(sqlupdateDict["sql_update"]["farm_location"])
    db_connect.insert(query=farm_update_sql, data=farm_db.to_dict("records"))


def updateDatabaseTable(
    db_connect,
    filepath: str | Path,
    tablename: str,
    farmname: str,
    farmtype: str,
    new_backup_date: dt.datetime,
    tableDict: dict,
    sqlupdateDict: dict,
) -> None:
    """
    Update farm information

    Parameters
    ----------
    db_connect : sql engine
        engine to connect ot database
    filepath : str or Path
        path to datafile (.csv)
    tablename : str
        name of the table/file
    farmname : str
        name of farm for which data is processed
    farmtype : str
        milking system identifier (d- delaval, l- lely)
    tableDict : dict
        dictionary containing information about the table schema of the target database
    sqlupdateDict : dict
        dictionary containing information to generate a sql statement
    """

    if farmtype == "d":
        milkingSystem = "AMS delaval"
    elif farmtype == "l":
        milkingSystem = "AMS lely"

    df_data = readData(filepath, tablename, tableDict, farmtype)
    df_data, farm_id, update_ani_lac = updateFarm(
        df_data, db_connect, farmname, milkingSystem, sqlupdateDict, new_backup_date
    )

    if tablename == "animal":
        df_data_new, df_data_update = checkDatabase(
            df_data, db_connect, tablename, farm_id, tableDict
        )
        if not df_data_update.empty:
            updateData(
                df_data_update,
                db_connect,
                tablename,
                tableDict,
                sqlupdateDict,
                farmtype,
                farm_id,
                update_ani_lac,
            )
        if not df_data_new.empty:
            writeData(df_data_new, db_connect, tablename, tableDict, farmtype)
    elif tablename == "lactation":
        df_data = updateAnimal(df_data, db_connect, farm_id, sqlupdateDict)
        df_data = df_data.loc[~pd.isnull(df_data.animal_id)]
        df_data_new, df_data_update = checkDatabase(
            df_data, db_connect, tablename, farm_id, tableDict
        )
        if not df_data_update.empty:
            updateData(
                df_data_update,
                db_connect,
                tablename,
                tableDict,
                sqlupdateDict,
                farmtype,
                farm_id,
                update_ani_lac,
            )
        if not df_data_new.empty:
            writeData(df_data_new, db_connect, tablename, tableDict, farmtype)
    elif tablename == "milking":
        df_data = updateAnimal(df_data, db_connect, farm_id, sqlupdateDict)
        updateMilking(
            df_data, db_connect, farm_id, farmname, farmtype, sqlupdateDict, tableDict
        )
    elif tablename == "cleaning":
        df_data = mapMilkingSystem(df_data, db_connect, farm_id)
        df_data_new, df_data_update = checkDatabase(
            df_data, db_connect, tablename, farm_id, tableDict
        )
        if not df_data_new.empty:
            writeData(df_data_new, db_connect, tablename, tableDict, farmtype)
    elif tablename in ["activity", "milkbiomarkers", "insemination", "bcs"]:
        df_data = mapAnimalid(df_data, db_connect, farm_id)
        df_data_new, df_data_update = checkDatabase(
            df_data, db_connect, tablename, farm_id, tableDict
        )
        if not df_data_new.empty:
            df_data_new = mapLactationid(df_data_new, db_connect, farm_id, tablename)
            writeData(df_data_new, db_connect, tablename, tableDict, farmtype)


def updateDatabaseFull(
    rootdir: str | Path, farm_to_update: str, anonymizeFarmlocation: bool
) -> None:
    """
    Update farm information

    Parameters
    ----------
    rootdir : str or Path
        path to cowbase rootdir
    farm_to_update : str
        name of farm for which data is processed
    anonymizeFarmlocation : bool
        anonymize farm location (in a radius of 5 km around original location)
    """

    rootdir = Path(rootdir)

    with open(rootdir / "config" / "serverSettings.json") as file:
        serverSettings = json.load(file)
    with open(rootdir / "config" / "M4_tableDict.json") as file:
        tableDict = json.load(file)
    with open(rootdir / "config" / "M4_sqlupdate.json") as file:
        sqlupdateDict = json.load(file)

    db_connect = DB_connect(**serverSettings)

    filepath = rootdir / "OUTPUT"
    farmfound = False
    for farms in os.listdir(filepath):
        farmtype = re.split("_", farms)[0]
        farmname = re.split("_", farms)[1]
        if not farms == farm_to_update:
            continue
        farmfound = True
        for tables in tableDict:
            for files in os.listdir(filepath / farms / "02_merged_table"):
                tablename = re.split("_", files[:-4])[-1]
                try:
                    new_backup_date = dt.datetime.strptime(
                        re.split("_", files)[3], "%Y%m%d"
                    )
                except RuntimeError:
                    new_backup_date = dt.datetime.strptime(
                        re.split("_", files)[3], "%Y%m%d%H%M"
                    )
                if tablename == tables:
                    print(f"Writing data in table {tablename}!")
                    datapath = filepath / farms / "02_merged_table" / files
                    updateDatabaseTable(
                        db_connect,
                        datapath,
                        tablename,
                        farmname,
                        farmtype,
                        new_backup_date,
                        tableDict,
                        sqlupdateDict,
                    )
                    print("Done!")
        updateFarmLocation(db_connect, sqlupdateDict, anonymizeFarmlocation)
    if farmfound == False:
        print("Could not find data for the farm that should be analyzed!")


def writeWeather(rootdir):
    rootdir = Path(rootdir)
    rootdir_INPUT_weather = rootdir / "INPUT" / "weather"
    with open(rootdir / "config" / "serverSettings.json") as file:
        serverSettings = json.load(file)
    with open(rootdir / "config" / "M4_sqlupdate.json") as file:
        sqlupdateDict = json.load(file)
    db_connect = DB_connect(**serverSettings)

    df_weather = pd.read_csv(rootdir_INPUT_weather / "weather.csv", header=0)
    df_weather_stations = pd.read_csv(rootdir_INPUT_weather / "aws.csv", header=0)
    df_weather_stations_weights = pd.read_csv(
        rootdir_INPUT_weather / "aws_weights.csv", header=0
    )
    df_weather_stations[
        [
            "hourly_start",
            "hourly_end",
            "daily_start",
            "daily_end",
            "monthly_start",
            "monthly_end",
        ]
    ] = df_weather_stations[
        [
            "hourly_start",
            "hourly_end",
            "daily_start",
            "daily_end",
            "monthly_start",
            "monthly_end",
        ]
    ].apply(
        pd.to_datetime
    )

    for column in [
        "hourly_start",
        "hourly_end",
        "daily_start",
        "daily_end",
        "monthly_start",
        "monthly_end",
    ]:
        df_weather_stations[column] = df_weather_stations[column].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    df_weather_stations[
        [
            "hourly_start",
            "hourly_end",
            "daily_start",
            "daily_end",
            "monthly_start",
            "monthly_end",
        ]
    ] = df_weather_stations[
        [
            "hourly_start",
            "hourly_end",
            "daily_start",
            "daily_end",
            "monthly_start",
            "monthly_end",
        ]
    ].replace(
        {np.nan: None}
    )

    farm_sql = """
    SELECT farm_id, farmname
    FROM farm
    ;
    """
    farm_db = db_connect.query(query=farm_sql)

    dict_farm_ids = pd.Series(farm_db.farm_id.values, index=farm_db.farmname).to_dict()

    df_weather = df_weather.loc[df_weather.farmname.isin(list(farm_db.farmname))]
    df_weather_stations = df_weather_stations.loc[
        df_weather_stations.farmname.isin(list(farm_db.farmname))
    ]
    df_weather_stations_weights = df_weather_stations_weights.loc[
        df_weather_stations_weights.farmname.isin(list(farm_db.farmname))
    ]

    df_weather["farm_id"] = df_weather["farmname"].map(dict_farm_ids)
    df_weather = df_weather.drop(columns=["farmname"])
    df_weather["updated_on"] = dt.date.today()

    df_weather_stations = df_weather_stations.drop(columns=["farmname"])
    df_weather_stations["updated_on"] = dt.date.today()

    df_weather_stations_weights["farm_id"] = df_weather_stations_weights[
        "farmname"
    ].map(dict_farm_ids)
    df_weather_stations_weights = df_weather_stations_weights.drop(columns=["farmname"])
    df_weather_stations_weights["updated_on"] = dt.date.today()

    df_weather_stations_weights.aws_id_1 = np.floor(
        pd.to_numeric(df_weather_stations_weights.aws_id_1, errors="coerce")
    ).astype("Int64")
    df_weather_stations_weights.aws_id_2 = np.floor(
        pd.to_numeric(df_weather_stations_weights.aws_id_2, errors="coerce")
    ).astype("Int64")
    df_weather_stations_weights.aws_id_3 = np.floor(
        pd.to_numeric(df_weather_stations_weights.aws_id_3, errors="coerce")
    ).astype("Int64")
    df_weather_stations_weights.aws_id_4 = np.floor(
        pd.to_numeric(df_weather_stations_weights.aws_id_4, errors="coerce")
    ).astype("Int64")

    # ####################################################################################################################
    # drop data that was already in the database
    weather_sql = f"""
    SELECT farm_id, datetime
    FROM weather
    ;
    """
    weather_db = db_connect.query(query=weather_sql)

    df_weather["datetime"] = pd.to_datetime(df_weather["datetime"])
    weather_db["datetime"] = pd.to_datetime(weather_db["datetime"])

    df_weather = df_weather.drop_duplicates(
        subset=["farm_id", "datetime"], keep="first"
    )

    weather_update_new = df_weather.merge(
        weather_db[["farm_id", "datetime"]],
        how="left",
        on=["farm_id", "datetime"],
        indicator=True,
    ).copy()

    weather_update_new = weather_update_new.loc[
        weather_update_new["_merge"] == "left_only"
    ].drop(columns=["_merge"])

    weather_update_new["datetime"] = weather_update_new["datetime"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    weather_update_new.to_sql(
        "weather", con=db_connect.ret_con(), if_exists="append", index=False
    )

    ####################################################################################################################

    aws_update_sql = create_sql_insert_update(sqlupdateDict["sql_update"]["aws"])
    db_connect.insert(query=aws_update_sql, data=df_weather_stations.to_dict("records"))

    aws_weights_update_sql = create_sql_insert_update(
        sqlupdateDict["sql_update"]["aws_weights"]
    )
    db_connect.insert(
        query=aws_weights_update_sql,
        data=df_weather_stations_weights.to_dict("records"),
    )


def meteostatExtract(rootdir, startdate="2010-01-01", enddate="2023-01-01"):
    start = dt.datetime.strptime(startdate, "%Y-%m-%d")
    end = dt.datetime.strptime(enddate, "%Y-%m-%d")

    with open(os.path.join(rootdir, "config", "M4_sqlupdate.json")) as file:
        sqlupdateDict = json.load(file)

    dict_farmlocation = sqlupdateDict["farminfo"]["farm_location"]

    weather = pd.DataFrame()
    weather_stations = pd.DataFrame()
    weather_stations_weights = pd.DataFrame()
    for farms in dict_farmlocation.keys():
        print(farms)
        farmlocation = Point(
            dict_farmlocation[farms][0],
            dict_farmlocation[farms][1],
            dict_farmlocation[farms][2],
        )
        farmlocation.method = "weighted"
        weather_add = Hourly(farmlocation, start, end)
        weather_add = weather_add.fetch()
        weather_add = weather_add.reset_index()
        weather_add = weather_add.rename(
            columns={
                "time": "datetime",
                "temp": "temperature",
                "dwpt": "dew_point",
                "rhum": "humidity",
                "prcp": "precipitation",
                "snow": "snow",
                "wdir": "wind_direction",
                "wspd": "windspeed",
                "wpgt": "peak_wind_gust",
                "pres": "air_pressure",
                "tsun": "total_sunshine_duration",
                "coco": "weather_condition_code",
            }
        )
        weather_stations_add = Stations()
        weather_stations_add = weather_stations_add.nearby(
            dict_farmlocation[farms][0], dict_farmlocation[farms][1]
        ).fetch(4)
        weather_stations_add = weather_stations_add.reset_index()
        weather_stations_add = weather_stations_add.rename(columns={"id": "aws_id"})
        weather_stations_add = weather_stations_add.loc[
            ~pd.isnull(weather_stations_add.wmo)
        ]
        weather_stations_add = weather_stations_add.reset_index(drop=True)
        weather_stations_add.aws_id = weather_stations_add.aws_id.astype(int)
        if len(weather_stations_add) == 4:
            weather_stations_weighted_add = pd.DataFrame(
                {
                    "farmname": [farms],
                    "aws_id_1": list(weather_stations_add.aws_id.astype(int))[0],
                    "distance_1": list(weather_stations_add.distance.astype(float))[0],
                    "aws_id_2": list(weather_stations_add.aws_id.astype(int))[1],
                    "distance_2": list(weather_stations_add.distance.astype(float))[1],
                    "aws_id_3": list(weather_stations_add.aws_id.astype(int))[2],
                    "distance_3": list(weather_stations_add.distance.astype(float))[2],
                    "aws_id_4": list(weather_stations_add.aws_id.astype(int))[3],
                    "distance_4": list(weather_stations_add.distance.astype(float))[3],
                }
            )
        elif len(weather_stations_add) == 3:
            print(
                "Warning: 1 of the closest weather stations were not registered with WMO and hence removed!"
            )
            weather_stations_weighted_add = pd.DataFrame(
                {
                    "farmname": [farms],
                    "aws_id_1": list(weather_stations_add.aws_id.astype(int))[0],
                    "distance_1": list(weather_stations_add.distance.astype(float))[0],
                    "aws_id_2": list(weather_stations_add.aws_id.astype(int))[1],
                    "distance_2": list(weather_stations_add.distance.astype(float))[1],
                    "aws_id_3": list(weather_stations_add.aws_id.astype(int))[2],
                    "distance_3": list(weather_stations_add.distance.astype(float))[2],
                }
            )
        elif len(weather_stations_add) == 2:
            print(
                "Warning: 2 of the closest weather stations were not registered with WMO and hence removed!"
            )
            weather_stations_weighted_add = pd.DataFrame(
                {
                    "farmname": [farms],
                    "aws_id_1": list(weather_stations_add.aws_id.astype(int))[0],
                    "distance_1": list(weather_stations_add.distance.astype(float))[0],
                    "aws_id_2": list(weather_stations_add.aws_id.astype(int))[1],
                    "distance_2": list(weather_stations_add.distance.astype(float))[1],
                }
            )
        else:
            print(
                "Warning: More than 2 of the closest weather stations were not registered with WMO and hence removed!"
            )
            weather_stations_weighted_add = pd.DataFrame()

        weather_stations_add = weather_stations_add.drop(columns=["distance"])
        weather_stations_add["farmname"] = farms
        weather_add["farmname"] = farms
        weather = pd.concat([weather, weather_add])
        weather = weather.reset_index(drop=True)
        weather_stations = pd.concat([weather_stations, weather_stations_add])
        weather_stations = weather_stations.drop_duplicates(subset=["aws_id"])
        weather_stations = weather_stations.reset_index(drop=True).sort_values(
            by="aws_id"
        )
        weather_stations_weights = pd.concat(
            [weather_stations_weights, weather_stations_weighted_add]
        )
        weather_stations_weights = weather_stations_weights.reset_index(drop=True)

    rootdir = Path(rootdir)
    rootdir_INPUT_weather = rootdir / "INPUT" / "weather"
    rootdir_INPUT_weather.mkdir(exist_ok=True, parents=True)
    weather.to_csv(rootdir_INPUT_weather / "weather.csv", index=False)
    weather_stations.to_csv(rootdir_INPUT_weather / "aws.csv", index=False)
    weather_stations_weights.to_csv(
        rootdir_INPUT_weather / "aws_weights.csv", index=False
    )
