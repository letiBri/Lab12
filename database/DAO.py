from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNazioni():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select distinct(gr.Country)
                    from go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailers(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select *
                    from go_retailers gr 
                    where gr.Country = %s"""

        cursor.execute(query, (country, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesi(r1, r2, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select count(*) as peso
                    from (select gds1.Retailer_code as r1, gds2.Retailer_code as r2, gds1.Product_number as p
                            from go_daily_sales gds1, go_daily_sales gds2
                            where gds1.Product_number = gds2.Product_number 
                            and gds1.Retailer_code = %s and gds2.Retailer_code = %s
                            and year(gds1.Date) = year(gds2.Date) and year(gds1.Date) = %s
                            group by gds1.Product_number) t"""

        cursor.execute(query, (r1.Retailer_code, r2.Retailer_code, anno))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result
