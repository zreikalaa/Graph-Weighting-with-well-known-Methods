import psycopg2 as psycopg2


class dataAdapter:  # A class to interact with the database that contains the trajectories
    tableName = None
    UCs = None

    def __init__(self, table_name):
        self.tableName = table_name

    def load_data(self, hors_dusage_percentage):

        data = []
        conn = psycopg2.connect(
            "dbname=BNF port=5432 user=postgres password=Postalaa1")
        cursor = conn.cursor()
        query = "SELECT * from " + self.tableName + " where class=1"
        cursor.execute(query)
        field_names = [i[0] for i in cursor.description][1:-3]
        records = cursor.fetchall()
        for row in records:
            id_uc = row[0]
            concepts = []
            for index, value in enumerate(row[1:-3]):
                if value != 0:
                    concepts.append(field_names[index])
            data.append((id_uc, concepts))
        communicable = cursor.rowcount
        hors_dusage = int((communicable*hors_dusage_percentage)/(100-hors_dusage_percentage))
        query = "SELECT * from " + self.tableName + " where class=0 limit "+str(hors_dusage)
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            id_uc = row[0]
            concepts = []
            for index, value in enumerate(row[1:-3]):
                if value != 0:
                    concepts.append(field_names[index])
            data.append((id_uc, concepts))
        hors_dusage = cursor.rowcount
        return field_names, data