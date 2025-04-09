from luca.connectors import LucaConnector, KeycloakConnector
from luca.querys import query
from luca.charts import get_charts, get_chart
from luca.datasources import get_datasources, get_datasource
from luca.systems import get_systems, get_system
from luca.users import get_users, get_user
import pytest
import pandas as pd

keycloak_env = {
    'server_url': 'https://dev.luca-bds.com/auth',
    'realm_name': 'luca-bds',
    'client_id': 'luca-bds-web'
}

luca_env = {
    'server_url': 'https://dev.luca-bds.com/luca-api',
    'username': 'luca',
    'password': '1234'
}

# ----------------------------------------
# Test KeycloakConnector and LucaConnector
# ----------------------------------------
@pytest.fixture
def test_KeycloakConnector():
    return KeycloakConnector(**keycloak_env)

@pytest.fixture
def test_KeycloakLucaConnector(test_KeycloakConnector):
    return LucaConnector(keycloak_connection=test_KeycloakConnector, **luca_env)

@pytest.fixture
def test_LucaConnector():
    return LucaConnector(**luca_env)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_info_kc(test_KeycloakLucaConnector, return_pd, expected_type):
    result = test_KeycloakLucaConnector.info(return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_info(test_LucaConnector, return_pd, expected_type):
    result = test_LucaConnector.info(return_pd=return_pd)
    assert isinstance(result, expected_type)

# ----------------------------------------
# Test Querys
# ----------------------------------------
@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_query_id(test_LucaConnector, return_pd, expected_type):
    result, pag, state = query(conn=test_LucaConnector, id=364, environment='DES', input_variables=[{'Usuario': 'luca', 'Sistema': 'LUCA'}], return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_query(test_LucaConnector, return_pd, expected_type):
    result, pag, state = query(conn=test_LucaConnector, name='Prueba', environment='DES', return_pd=return_pd)
    assert isinstance(result, expected_type)

# ----------------------------------------
# Test Charts
# ----------------------------------------
@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_charts(test_LucaConnector, return_pd, expected_type):
    result = get_charts(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_chart(test_LucaConnector, return_pd, expected_type):
    result = get_chart(conn=test_LucaConnector, id=27133, return_pd=return_pd)
    assert isinstance(result, expected_type)

# ----------------------------------------
# Test Datasources
# ----------------------------------------
@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_datasources(test_LucaConnector, return_pd, expected_type):
    result = get_datasources(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_datasource(test_LucaConnector, return_pd, expected_type):
    result = get_datasource(conn=test_LucaConnector, id=211488, return_pd=return_pd)
    assert isinstance(result, expected_type)

# ----------------------------------------
# Test Systems
# ----------------------------------------
@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_systems(test_LucaConnector, return_pd, expected_type):
    result = get_systems(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_ystem(test_LucaConnector, return_pd, expected_type):
    result = get_system(conn=test_LucaConnector, id=17002, return_pd=return_pd)
    assert isinstance(result, expected_type)

# ----------------------------------------
# Test Users
# ----------------------------------------
@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_users(test_LucaConnector, return_pd, expected_type):
    result = get_users(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_user(test_LucaConnector, return_pd, expected_type):
    result = get_user(conn=test_LucaConnector, id=295054, return_pd=return_pd)
    assert isinstance(result, expected_type)
