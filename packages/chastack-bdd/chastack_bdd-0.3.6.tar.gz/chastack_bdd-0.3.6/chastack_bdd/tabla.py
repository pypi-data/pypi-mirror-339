from chastack_bdd.tipos import *
from chastack_bdd.utiles import *
from chastack_bdd.bdd import ProtocoloBaseDeDatos
from chastack_bdd.registro import Registro

class Tabla(type):
    def __new__(mcs, nombre, bases, atributos):
        if Registro not in bases and nombre != 'Registro':
            bases = (Registro,) + bases
        
        cls = super().__new__(mcs, nombre, bases, atributos)
        
        cls.__tabla = nombre
        setattr(cls, "tabla", property(lambda cls : cls.__tabla))

        
        if not hasattr(cls, '__annotations__'):
            cls.__annotations__ = {}
        
        return cls

    def __init__(cls, nombre, ancestros, diccionario):
        cls.__INICIALIZADA = False
        cls.__DEBUG = False


    def __call__(cls, bdd: ProtocoloBaseDeDatos, *posicionales, **nominales): 
        if nominales and nominales.get("debug", False):
            cls.__DEBUG = True
        debug = lambda msj: print(f"[DEBUG] {msj}") if cls.__DEBUG else lambda msj: None
        debug(f"{posicionales}, {nominales}")
        debug(f"Se llamó a la clase {cls}. Instanciando objeto.")
        debug(f"{cls} {'ya' if cls.__INICIALIZADA else 'no'} estaba inicializada.")
        if not cls.__INICIALIZADA: 
            slots :list[str] = []        
            anotaciones : dict[str,type] = {}
            with bdd as bdd:
                resultados = bdd.DESCRIBE(cls.__tabla).ejecutar().devolverResultados()
                
                debug(f"Inicializando modelo para: {cls.__tabla}.")
                for columna in resultados:
                    nombre_campo = columna.get('Field')
                    es_clave = columna.get('Key') == "PRI"
                    es_auto = "auto_increment" in columna.get("Extra", "").lower() or "default_generated" in columna.get("Extra", "").lower() or "auto_generated" in columna.get("Extra", "").lower()
                    
                    nombre_attr = f"__{nombre_campo}" if es_clave or es_auto else nombre_campo
                    
                    tipo = cls.__resolverTipo(columna.get('Type'), nombre_campo)
                    debug(f"| {str(nombre_campo):<40} | {str(columna.get('Type','')):<40} | {str(tipo):<40}")
                    
                    if nombre_attr not in cls.__slots__:
                        slots.append(nombre_attr)
                    anotaciones.update({
                        nombre_attr : tipo
                    })
                    
                    
                    if es_clave:
                        setattr(cls, nombre_campo, property(lambda self, name=nombre_campo: getattr(self, atributoPrivado(self,name))))
        
            cls.__slots__ = cls.__slots__ + tuple(slots)
            cls.__annotations__.update(anotaciones)
            cls.__INICIALIZADA = True
        
        instancia = super().__call__(bdd, *posicionales, **nominales)
        setattr(instancia, atributoPrivado(instancia,"__bdd"),bdd)
        return instancia
    
    @classmethod
    def __resolverTipo(cls, tipo_sql: str, nombre_columna: Optional[str]) -> type:
        """
        Deduce y devuelve un tipo de Python en base al tipo declarado en MySQL para la columna.
        Si encuentra un ENUM, crea un enum de Python y lo guarda como una constante de la clase.
        
        Parámetros:
            :arg tipo_sql str: El tipo definido en MySQL
            :arg nombre_columna Optional[str]: El nombre de la columna (útil para enums)
        
        Devuelve:
            :arg tipo `type`: el tipo python correspondiente (o `Any`)
        """
        tipo_declarado: Optional[Match[AnyStr]] = match(r'([a-z]+)(\(.*\))?', tipo_sql.lower())
        if not tipo_declarado:
            return Any

        tipo_base: str = tipo_declarado.group(1)
        parametros: str = tipo_declarado.group(2) if tipo_declarado.group(2) else ""
        tipo_completo: str = tipo_base + parametros

        tipos: dict[str, type] = {
            'tinyint': int,
            'smallint': int,
            'mediumint': int,
            'int': int,
            'bigint': int,
            'float': float,
            'double': float,
            'decimal': Decimal,
            'datetime': datetime,
            'timestamp': datetime,
            'date': date,
            'time': time,
            'char': str,
            'varchar': str,
            'text': str,
            'mediumtext': str,
            'longtext': str,
            'tinytext': str,
            'boolean': bool,
            'bool': bool,
            'tinyint(1)': bool,
            'blob': bytearray,
            'mediumblob': bytearray,
            'longblob': bytearray,
            'tinyblob': bytearray,
            'binary': bytearray,
            'varbinary': bytearray,
            'json': dict,
        }

        
        if tipo_base == 'enum':
            valores_enum: list[Any] = findall(r"'([^']*)'", tipo_sql)
            dicc_enum: dict[str, int] = {'_invalido': 0}
            for i, val in enumerate(valores_enum, 1):   
                dicc_enum[val] = i
            
            nombre_enum: str = f"Tipo{nombre_columna.capitalize()}" if nombre_columna else f"__ENUM_{token_urlsafe(4)}"
            clase_enum: type = type(
                nombre_enum,
                (EnumSQL, Enum),
                dicc_enum
            )
            
            setattr(cls,nombre_enum,clase_enum)
            return clase_enum

        
        if tipo_completo in tipos:
            return tipos[tipo_completo]
        return tipos.get(tipo_base, Any)