# @Coding: UTF-8
# @Time: 2024/9/11 0:15
# @Author: xieyang_ls
# @Filename: mysql_handler.py
import json

import datetime

from abc import ABC, abstractmethod

from logging import info, error, INFO, basicConfig

from pyutils_spirit.annotation import singleton

from pymysql import Connect, OperationalError, cursors

from pyutils_spirit.exception import ArgumentException

basicConfig(level=INFO)


class Handler(ABC):

    @abstractmethod
    def select(self, sql: str) -> tuple:
        pass

    @abstractmethod
    def insert(self, sql: str) -> bool:
        pass

    @abstractmethod
    def update(self, sql: str) -> bool:
        pass

    @abstractmethod
    def delete(self, sql: str) -> bool:
        pass

    @abstractmethod
    def manageExecute(self, sql: str) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def getConnection(self) -> [Connect]:
        pass


@singleton(signature="MysqlHandler")
class MySQLHandler(Handler):
    __cursor = None

    __connection = None

    def __init__(self, args: dict[str, str | int]) -> None:
        try:
            connection: Connect = Connect(
                host=args["host"],
                port=args["port"],
                user=args["user"],
                password=args["password"],
                cursorclass=cursors.DictCursor
            )
            connection.select_db(args["database"])
            info(f"Connected to database {args['database']} successfully!!!")
            info(f"MySQL version: {connection.get_server_info()}")
            cursor = connection.cursor()
            self.__connection = connection
            self.__cursor = cursor
        except (ArgumentException, OperationalError):
            error(f"Connected to database {args['database']} failure")
            raise ArgumentException("please check connected the database arguments")

    def __json_format_list(self, results: list[dict] | tuple[dict]) -> list:
        if isinstance(results, list | tuple):
            for result in results:
                if result is None:
                    continue
                self.__json_format_dict(result)
        return results

    def __json_format_dict(self, result: dict) -> dict:
        for key in result.keys():
            attribute = result[key]
            if attribute is None:
                continue
            if isinstance(attribute, str):
                try:
                    attribute = json.loads(attribute)
                except json.decoder.JSONDecodeError:
                    continue
            if isinstance(attribute, dict):
                result[key] = self.__json_format_dict(attribute)
            elif isinstance(attribute, list):
                result[key] = self.__json_format_list(attribute)
            else:
                if isinstance(attribute, datetime.datetime):
                    result[key] = attribute.isoformat()
        return result

    def select(self, sql: str) -> list | tuple | dict:
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            return self.__json_format_list(results)
        except OperationalError as e:
            if e.args[0] == 1054:
                return []
            else:
                raise e

    def insert(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def update(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def delete(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def manageExecute(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def getConnection(self) -> [Connect]:
        return self.__connection, self.__cursor

    def disconnect(self) -> None:
        self.__connection.close()
