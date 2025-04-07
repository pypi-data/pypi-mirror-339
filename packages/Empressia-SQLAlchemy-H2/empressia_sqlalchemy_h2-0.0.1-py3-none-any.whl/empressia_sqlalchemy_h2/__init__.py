import sqlalchemy;
import empressia_sqlalchemy_h2;
from empressia_sqlalchemy_h2.CompatibilityMode import *;
from empressia_sqlalchemy_h2.H2Dialect import *;

sqlalchemy.dialects.registry.register("h2", empressia_sqlalchemy_h2.__name__, "H2Dialect");
