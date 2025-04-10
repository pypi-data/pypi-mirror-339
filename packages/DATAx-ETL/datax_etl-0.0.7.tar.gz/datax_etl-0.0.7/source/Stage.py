"""
se basear no numero do ultimo lote processado (RESUMO)
montar nome do arquivo a ser lido baseado no nome do processo
e numero do lote
"""

import datetime as dt
import os
import json
import re
import pandas as pd
from dotenv import load_dotenv

from DE_Lib.Utils.Cipher import Fernet
from DE_Lib.DataBase import Oracle, MySql, SQLite, OracleDDL
from DE_Lib.Utils import Sql, Generic, DateUtils, System
from DE_Lib.Utils.Cipher import Fernet
from DE_Lib.Files import Csv, JSon, Txt, Parquet, Zip
from DE_Lib.Log import Log, Level

from source.Lib import Parameter, Connect, Etl

sql = Sql.SQL()
gen = Generic.GENERIC()
fernet = Fernet.FERNET()
con = Connect.CONNECT()
so = System.SO()
dtu = DateUtils.DATEUTILS()
log = Log.LOG()
lvl = Level.LEVEL()
ddl = OracleDDL.OracleDDL()

csv = Csv.CSV()
txt = Txt.TXT()
jsn = JSon.JSON()
#parquet = Parquet.PARQUET()
zip = Zip.ZIP()

par = Parameter.PARAMETER()
conn = Connect.CONNECT()
etl = Etl.ETL()


class STAGE:
    def __init__(self):
        msg, result = None, None
        try:
            if not etl.getEnviroment():
                raise Exception(self.ERROR)
            fernet.setToken(os.environ.get("token"))
        except Exception as error:
            msg = error
            result = msg
        finally:
            print(result)

    def execute(self, process_name: str):
        msg, result, truncate = None, None, True
        try:

            #region Iniciando o processo
            self.NameProcess = process_name
            self.Start_Date = dt.datetime.now()
            #endregion

            #region Obtendo os parametros do processo
            par.setInit()
            __parListDict = par.getParameter(cols=["*"], cols_where=["NOM_PROJETO"],
                                             cols_value=[[self.NameProcess, "Paths"]])
            __hashes = sql.fromListDictToList(listDict=__parListDict, keyValue="HASH")
            self.Parameters = par.setParametersListToDict(__parListDict)
            # --------------------------------------------------------------
            #endregion

            #region Start LOG
            __fileLog = os.path.join(self.Parameters['Paths']['path_base'], self.Parameters['Paths']['log_files'],
                                     f"{self.NameProcess}-{self.Start_Date.strftime(dtu.DATETIME_FILENAME)}.log")
            __procDict = {"processo": self.NameProcess,
                          "descricao": "Teste de rotina de LOG",
                          "file": __fileLog,
                          "conexao": par.CONNECTION,
                          "table": "BI_DAX.LOG",
                          "event": "BI_DAX.LOG_EVENT"
                          }
            log.setInit(__procDict)
            log.setLogEvent(content=f"""Inicializando os parametros!""", level=lvl.INFO)
            #endregion

            for self.TableName in self.Parameters["Objetos_Candidatos"]:

                # region HASH
                """
                  ------------------------------------------------------------------------------------
                  o elemento HASH foi colocado intensionalmente pela funcao setParamtersListToDict
                  como ele foje da estrutura dos objetos candidatos, foi colocada a instrucao abaixo
                  Se este tipo de objeto for localizado sera dado um bypass e pula para o proximo
                  do looping
                  ------ Ver possibilidade de poipular o hash de outra forma ------
                  ------------------------------------------------------------------------------------
                """
                if self.TableName == "HASH":
                    continue
                # endregion

                # region Identifica se o objeto candidato esta ativo
                if self.TableId["ativo"] != "S":
                    # Objeto selecionado não se encontra ativo, pule para o proximo
                    continue
                # endregion

                #region Lendo arquivos candidatos
                __rootDir = os.path.join(self.Parameters["Paths"]["path_base"], self.Parameters["Paths"][self.Destino["local_destino"]])
                __regexinclude = f"""{self.NameProcess}-{self.TableName}.*{self.Resumo["identificacao"]["ultimo_lote"]}.*.(csv|json|xlsx|xls|parquet|avro|txt)"""
                __regexexclude = ""
                __files = os.listdir(__rootDir)
                regex = re.compile(__regexinclude, re.IGNORECASE)
                for __file in __files:
                    if regex.match(__file):
                        x = os.path.join(__rootDir, __file)
                        df = pd.read_csv(x, sep=";").astype(str)
                        df = df.replace({pd.NA: None, pd.NaT: None, float("nan"): None, str("nan"): None})
                        __tkStg = par.getParameter(cols=["VAL_PARAMETRO"], cols_where=['NOM_PARAMETRO'], cols_value=["token_bi_stg"])[0]["VAL_PARAMETRO"]
                        value = fernet.decrypt(__tkStg)
                        value = json.loads(value)
                        value["password"] = fernet.decrypt(value["password"])
                        con.setConectionDataBase(value)
                        if not con.CONNECTION_VALID:
                            raise Exception(con.DATABASE_ERROR)
                        else:
                            self.CONNECTION = con.CONNECTION
                            self.CONNECTION_IS_VALID = con.CONNECTION_VALID
                            self.DATABASE_ERROR = con.DATABASE_ERROR
                            self.DATABASE_DRIVER = con.DATABASE_DRIVER
                            self.NOME_DATABASE = con.NOME_DATABASE

                        ddl.create_table_and_insert_data(df=df, conn=self.CONNECTION, table_name=f"STG_{self.TableName[0:26]}", truncate=truncate)
                        truncate = False # Tabela ja foi truncada (apenas uma vez)
                #endregion

        except Exception as error:
            msg = error
            result = msg
        finally:
            log.setEnd()
            return result

        # region NOVAS PROPRIEDADES GETTER´s e SETTER´s

    @property
    def Start_Date(self):
        return self._Start_Date

    @Start_Date.setter
    def Start_Date(self, value):
        self._Start_Date = value

    @property
    def End_Date(self):
        return self._End_Date

    @End_Date.setter
    def End_Date(self, value):
        self._End_Date = value

    @property
    def NameProcess(self: str):
        return self._NameProcess

    @NameProcess.setter
    def NameProcess(self, value) -> str:
        self._NameProcess = value

    @property
    def Parameters(self) -> dict:
        return self._Parameters

    @Parameters.setter
    def Parameters(self, value: dict):
        self._Parameters = value

    @property
    def Paths(self) -> dict:
        return self.Parameters["Paths"]

    @Paths.setter
    def Paths(self, value: dict):
        self.Parameters["Paths"] = value

    @property
    def Schedule(self) -> dict:
        return self.Parameters["Schedule"]

    @Schedule.setter
    def Schedule(self, value: dict):
        self.Parameters["Schedule"] = value

    @property
    def Resumo(self) -> dict:
        return self.Parameters["Resumo"]

    @Resumo.setter
    def Resumo(self, value: dict):
        self._Resumo = value

    @property
    def Obj(self) -> dict:
        return self.Parameters["Objetos_Candidatos"]

    @Obj.setter
    def Obj(self, value: dict):
        self.Parameters["Objetos_Candidatos"] = value
        # self._Obj = value

    @property
    def TableName(self) -> str:
        return self._TableName

    @TableName.setter
    def TableName(self, value: str):
        self._TableName = value

    @property
    def TableId(self) -> dict:
        return self.Obj[self.TableName]["identificacao"]

    @TableId.setter
    def TableId(self, value: dict):
        self.Obj[self.TableName]["identificacao"] = value

    @property
    def Webhook(self) -> dict:
        return self.Obj[self.TableName]["webhook"]

    @Webhook.setter
    def Webhook(self, value: dict):
        self.Obj[self.TableName]["webhook"] = value

    @property
    def Origem(self) -> dict:
        return self.Obj[self.TableName]["origem"]

    @Origem.setter
    def Origem(self, value: dict):
        self.Obj[self.TableName]["origem"] = value

    @property
    def Estrategia(self) -> dict:
        return self.Obj[self.TableName]["estrategia"]

    @Estrategia.setter
    def Estrategia(self, value: dict):
        self.Obj[self.TableName]["estrategia"] = value

    @property
    def Filters(self) -> dict:
        return self.Obj[self.TableName]["filters"]

    @Filters.setter
    def Filters(self, value: dict):
        self.Obj[self.TableName]["filters"] = value

    @property
    def Destino(self) -> dict:
        return self.Obj[self.TableName]["destino"]

    @Destino.setter
    def Destino(self, value: dict):
        self.Obj[self.TableName]["destino"] = value

    @property
    def Delta(self) -> dict:
        return self.Estrategia["delta"]

    @Delta.setter
    def Delta(self, value: dict):
        self.Estrategia["delta"] = value

    @property
    def Slice(self) -> dict:
        return self.Estrategia["slice"]

    @Slice.setter
    def Slice(self, value: dict):
        self.Estrategia["slice"] = value

    @property
    def Iterator(self):
        # o Iterator pode retornar tanto um INT como um STR
        # por isso não foi tipado o retorno
        return self._Iterator

    @Iterator.setter
    def Iterator(self, value):
        # o Iterator pode popular tanto um INT como um STR
        # por isso não foi tipado a entrada
        self._Iterator = value

    @property
    def TokenName(self) -> str:
        # Nome do token de conexao
        return self.Origem["token"]

    @TokenName.setter
    def TokenName(self, value: str):
        # Nome do token de conexao
        self.Origem["token"] = value

    @property
    def TokenDataBase(self) -> str:
        # Token de conexao criptografado
        value = par.getParameter(cols=["VAL_PARAMETRO"], cols_where=["NOM_PARAMETRO"], cols_value=[self.TokenName])[0][
            "VAL_PARAMETRO"]
        if not isinstance(value, str):
            # consistindo se a coluna não é um STR (tipo BLOB oracle)
            value = str(value)
        return value

    @property
    def DataBaseConnection(self) -> dict:
        # string de conexao descriptografada
        value = fernet.decrypt(self.TokenDataBase)
        value = json.loads(value)
        value["password"] = fernet.decrypt(value["password"])
        return value

    @property
    def TipoCarga(self) -> str:
        return self.Estrategia["tipo_carga"]
        # return self._TipoCarga

    @TipoCarga.setter
    def TipoCarga(self, value: str):
        self.Estrategia["tipo_carga"] = value
    # endregion


if __name__ == "__main__":
    x = STAGE()
    process_name = "INTEGRADOR_HOSP_INDICADORES"
    rst = x.execute(process_name)
    print(rst)