import unittest
import psycopg2
import parameterized
import sys
sys.path.append('../src/')
import cell

class TestLogin(unittest.TestCase):

    # def setUp(self):
    #     #     global conn
    #     #     global cursor
    #     #     conn = psycopg2.connect("dbname='user_data' user='postgres' host='127.0.0.1' password='185111'")
    #     #     cursor = conn.cursor()
    #     #     #已存数据："wang""abc123ABC""Beijing Branch""Dr.Cai""2021-05-23""13935207223""lz_francis@163.com"
    #     #
    #     # def tearDown(self):
    #     #     conn.close()

    # @parameterized.parameterized.expand(login_data)
    def test_loginJudge_Username(self , username , password , expect):
        wrong_type = toolclass.loginJudge_Username(username , password , cursor)
        self.assertEqual(wrong_type , expect)

if __name__ == '__main__':
    unittest.main()
