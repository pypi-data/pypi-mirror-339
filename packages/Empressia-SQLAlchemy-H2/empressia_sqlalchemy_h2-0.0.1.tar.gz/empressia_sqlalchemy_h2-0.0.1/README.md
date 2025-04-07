# Empressia SQLAlchemy H2

## 概要

Empressia製のSQLAlchemy用のDialectです。  
H2 DatabaseへのJayDeBeApiを使用したJDBC接続をサポートします。  
接続するための最低限の実装しかしていません。  

## 使い方

JayDeBeApiを使用しているため、  
環境変数JAVA_HOMEに、JDKへのパスを指定しておく必要があります。  
例えば、pythonで設定するには以下のようにします。  

```python
os.environ["JAVA_HOME"] = r"/path/to/JDK/";
```

H2のjarへのパスは、環境変数CLASSPATHに設定するか、  
sqlalchemy.create_engineにjars引数として文字列の配列で渡してください。  

```python
os.environ["CLASSPATH"] = r"/path/to/h2-<version>.jar";
```

```python
sqlalchemy.create_engine("<URL>", jars=[r"/path/to/h2-<version>.jar"]);
```

URLは、以下の形式をサポートしています。  

> h2:///<database>
> h2+jaydebeapi:///<database>

databaseには、JDBCのsubnameを指定します。  

例えば、次のようなJDBCの接続文字列について考えます。  

> jdbc:h2:mem:TestDB

この場合は、以下がsubnameとなります。  

> mem:TestDB

sqlalchemy.create_engineに渡すURLは、次のようになります。  

> h2:///mem:TestDB

sqlalchemy.create_engineを呼ぶ前に、empressia_sqlalchemy_h2をimportしておいてください。  
SQLAlchemyへDialectを登録します。  

```python
import empressia_sqlalchemy_h2;
```
