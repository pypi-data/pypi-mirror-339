import sqlalchemy;
import jaydebeapi;
from empressia_sqlalchemy_h2.CompatibilityMode import *;

class H2Dialect(sqlalchemy.engine.default.DefaultDialect):
	"""
	Empressia製のSQLAlchemy用のDialectです。
	H2 DatabaseへのJayDeBeApiを使用したJDBC接続をサポートします。
	接続するための最低限の実装しかしていません。

	JayDeBeApiを使用しているため、
	環境変数JAVA_HOMEに、JDKへのパスを指定しておく必要があります。
	例えば、pythonで設定するには以下のようにします。
	os.environ["JAVA_HOME"] = r"/path/to/JDK/";

	H2のjarへのパスは、環境変数CLASSPATHに設定するか、
	sqlalchemy.create_engineにjars引数として文字列の配列で渡してください。
	os.environ["CLASSPATH"] = r"/path/to/h2-<version>.jar";
	sqlalchemy.create_engine("<URL>", jars=[r"/path/to/h2-<version>.jar"]);

	URLは、以下の形式をサポートしています。
	h2:///<database>
	h2+jaydebeapi:///<database>
	databaseには、JDBCのsubnameを指定します。

	例えば、次のようなJDBCの接続文字列について考えます。
	jdbc:h2:mem:TestDB
	この場合は、以下がsubnameとなります。
	mem:TestDB
	sqlalchemy.create_engineに渡すURLは、次のようになります。
	h2:///mem:TestDB

	sqlalchemy.create_engineを呼ぶ前に、empressia_sqlalchemy_h2をimportしておいてください。
	SQLAlchemyへDialectを登録します。
	import empressia_sqlalchemy_h2;
	"""

	name = "h2";

	driver = jaydebeapi.__name__;

	dialect_description = """
	Empressia製のSQLAlchemy用のDialectです。
	H2 DatabaseへのJayDeBeApiを使用したJDBC接続をサポートします。
	接続するための最低限の実装しかしていません。
	""";

	supports_statement_cache = True;
	""" 標準のキャッシュに従います。 """

	_jars: list[str] = [];
	""" H2のjarを指定するために用意しています。 """

	_CompatibilityMode: CompatibilityMode|None = None;

	def __init__(self, jars: list[str] = [], **kwargs):
		super().__init__(**kwargs);
		self._jars = jars;

	def create_connect_args(self, url):
		# SQLAlchemyでの定義は以下の感じです。
		# dialect+driver://username:password@host:port/database
		# このDialectでは以下をサポートします。
		# h2+jaydebeapi:///database
		# databaseはJDBCのsubnameに相当すると解釈します。
		# h2+jaydebeapi:///subname
		# h2ではsubnameをurl;setting=value[;setting=value]のような形式としています。
		START_WITHOUT_DRIVER = "h2://";
		START_WITH_DRIVER = "h2+jaydebeapi://";
		URL_WITHOUT_DATABASE_WITHOUT_DRIVER = START_WITHOUT_DRIVER + "/";
		URL_WITHOUT_DATABASE_WITH_DRIVER = START_WITH_DRIVER + "/";
		s: str = str(url);
		if((s.startswith(START_WITHOUT_DRIVER) or s.startswith(START_WITH_DRIVER)) == False):
			raise f"このDialectでは、url[{s}]は『dialect+driver://』として、『{START_WITHOUT_DRIVER}』、または、『{START_WITH_DRIVER}』で始まっている必要があります。";
		if((s.startswith(URL_WITHOUT_DATABASE_WITHOUT_DRIVER) or s.startswith(URL_WITHOUT_DATABASE_WITH_DRIVER)) == False):
			raise f"このDialectでは、username:password@host:portは省略する必要があります。必要であれば、database部分に指定するJDBCのsubname総統の箇所に指定してください。";
		if(s.startswith(URL_WITHOUT_DATABASE_WITHOUT_DRIVER)):
			subname = s[len(URL_WITHOUT_DATABASE_WITHOUT_DRIVER):];
		elif(s.startswith(URL_WITHOUT_DATABASE_WITH_DRIVER)):
			subname = s[len(URL_WITHOUT_DATABASE_WITH_DRIVER):];
		subname.split(";");
		JDBCURL = "jdbc:h2:" + subname;
		(url, *settings) = JDBCURL.split(";");
		d = dict(s.split("=") for s in settings);
		self._CompatibilityMode = d.get("MODE", CompatibilityMode.REGULAR);

		kwargs = {
			"jclassname": "org.h2.Driver",
			"url": JDBCURL,
			"driver_args": [],
			"jars": self._jars,
			"libs": []
		};
		return ((), kwargs);

	@classmethod
	def import_dbapi(cls):
		return jaydebeapi;

	def has_table(self, connection: sqlalchemy.engine.base.Connection, table_name: str, schema: str|None = None, **kw):
		if(schema != None):
			query = sqlalchemy.text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = :table_name").bindparams(
				schema=schema, table_name=table_name
			);
		else:
			query = sqlalchemy.text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :schema AND TABLE_NAME = :table_name").bindparams(
				schema=schema, table_name=table_name
			);
		count: int = connection.execute(query).scalar();
		has_table = (count > 0);
		return has_table;

# 検出されるようにモジュールに宣言しておく。
dialect=H2Dialect;
