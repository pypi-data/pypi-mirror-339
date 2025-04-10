from DE_Lib.DataBase import SQLite, Oracle, MsSql, MySql, Postgres, RedShift, Cache

# instanciando conexoes com banco de dados
cache = Cache.CACHE()
redshift = RedShift.REDSHIFT()
postgres = Postgres.POSTGRES()
mysql = MySql.MYSQL()
mssql = MsSql.MSSQL()
oracle = Oracle.ORACLE()
sqlite = SQLite.SQLITE()

class CONNECT:
    def __init__(self):
        self.__connection_valid = None
        self.__database_error = None
        self.__connection = None
        self.__nome_database = None
        self.__database_driver = None

    def setConectionDataBase(self, conn: dict):
        msg, result = None, True
        __valid, __error, __conn, __nomedatabase, __databasedriver = None, None, None, None, None
        try:
            if conn["database"].upper() == 'ORACLE':
                oracle.Connect(conn=conn)
                __valid = oracle.CONNECTION_VALID
                __error = oracle.DATABASE_ERROR
                __conn = oracle.CONNECTION
                __nomedatabase = oracle.NOME_DATABASE
                __databasedriver = oracle.DATABASE_DRIVER
            elif conn["database"].upper() == 'SQLITE':
                __connection = sqlite.Connect(conn=conn)
                __valid = sqlite.CONNECTION_VALID
                __error = sqlite.DATABASE_ERROR
                __conn = sqlite.CONNECTION
                __nomedatabase = sqlite.NOME_DATABASE
                __databasedriver = sqlite.DATABASE_DRIVER
            elif conn["database"].upper() == 'MSSQL':
                __connection = mssql.Connect(conn=conn)
                __valid = mssql.CONNECTION_VALID
                __error = mssql.DATABASE_ERROR
                __conn = mssql.CONNECTION
                __nomedatabase = mssql.NOME_DATABASE
                __databasedriver = mssql.DATABASE_DRIVER
            elif conn["database"].upper() == 'MYSQL':
                mysql.Connect(conn=conn)
                __valid = mysql.CONNECTION_VALID
                __error = mysql.DATABASE_ERROR
                __conn = mysql.CONNECTION
                __nomedatabase = mysql.NOME_DATABASE
                __databasedriver = mysql.DATABASE_DRIVER
            elif conn["database"].upper() == 'POSTGRES':
                __connection = postgres.Connect(conn=conn)
                __valid = postgres.CONNECTION_VALID
                __error = postgres.DATABASE_ERROR
                __conn = postgres.CONNECTION
                __nomedatabase = postgres.NOME_DATABASE
                __databasedriver = postgres.DATABASE_DRIVER
            elif conn["database"].upper() == 'CACHE':
                #__connection = db.CACHE(conn=conn)
                # __valid = oracle.CONNECTION_VALID
                # __error = oracle.DATABASE_ERROR
                # __conn = oracle.CONNECTION
                # __nomedatabase = oracle.NOME_DATABASE
                # __databasedriver = oracle.DATABASE_DRIVER
                #__connection = cache.
                ...
            elif conn["database"].upper() == 'REDSHIFT':
                #__connection = .REDSHIFT(conn=conn)
                # __valid = oracle.CONNECTION_VALID
                # __error = oracle.DATABASE_ERROR
                # __conn = oracle.CONNECTION
                # __nomedatabase = oracle.NOME_DATABASE
                # __databasedriver = oracle.DATABASE_DRIVER
                ...
            else:
                ...
        except Exception as error:
            msg = error
            result = msg
        finally:
            self.__connection_valid = __valid
            self.__database_error = __error
            self.__connection = __conn
            self.__nome_database = __nomedatabase
            self.__database_driver = __databasedriver
            return result

    # region Property´s
    @property
    def CONNECTION_VALID(self):
        return self.__connection_valid

    @property
    def CONNECTION(self):
        return self.__connection

    @property
    def DATABASE_ERROR(self):
        return self.__database_error

    @property
    def NOME_DATABASE(self):
        return self.__nome_database

    @property
    def DATABASE_DRIVER(self):
        return self.__database_driver

    @DATABASE_DRIVER.setter
    def DATABASE_DRIVER(self, value):
        self._DATABASE_DRIVER = value

    # endregion
