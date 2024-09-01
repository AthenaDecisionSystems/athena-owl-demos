import unittest
import psycopg2
import sys,os
sys.path.append('./src')

from ibu.app_settings import get_config

class TestCustomQuery(unittest.TestCase):
    
    def test_get_client(self):
        conn = psycopg2.connect(
            host="localhost",
            database="insurancedb",
            user="postgres",
            password="p0stgrespwd"
        )
        cur = conn.cursor()

        # Execute a SQL query
        cur.execute("select c.id, c.firstName, c.lastName from public.client as c where c.lastName = 'Smith' and c.firstName = 'Sonya';")
        results = cur.fetchall()

        assert results
        assert len(results) > 0
        # Print the results
        for row in results:
            print(f"\n@@@@> client id= {row[0]} with a last name as: {row[1]} : {row[2]}")
        # Close the cursor and connection
        cur.close()
        conn.close()

        
    def test_join_policy_claim(self):
        conn = psycopg2.connect(
                    host="localhost",
                    database="insurancedb",
                    user="postgres",
                    password="p0stgrespwd"
                )
        cur = conn.cursor()

        # Execute a SQL query
        cur.execute("select c.id, c.status from public.claim as c join public.insurancepolicy as i on c.policy_id = i.id where i.client_id = 2;")
        results = cur.fetchall()
        assert results
        assert len(results) > 0
        # Print the results
        for row in results:
            print(f"\n@@@@>claim_id= {row[0]} with a status as: {row[1]}")

        # Close the cursor and connection
        cur.close()
        conn.close()
   
        
if __name__ == '__main__':
    unittest.main() 
