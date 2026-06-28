from database.DB_connect import DBConnect
from model.Artisti import Artista
from model.Generi import Genere


class DAO:

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select  *
                from genre g
                order by g.Name asc
                """

        cursor.execute(query)

        for row in cursor:
            results.append(Genere(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArtist(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct a.*
                from genre g, artist a, album al, track t
                where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.GenreId =g.GenreId 
                and g.Name = %s
                and t.TrackId is not Null
                Order by a.Name asc
                """

        cursor.execute(query, (genere.Name,))

        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopolarity(genere):  # 1 - poi aggiungere questo nel model

        conn = DBConnect.get_connection()



        cursor = conn.cursor(dictionary=True)
        query = """ 
                select a.ArtistId , a.Name, SUM(ic.Quantity ) as popularity
                from artist a , album al, genre g , track t, invoice i, invoiceline ic
                where a.ArtistId = al.ArtistId  and t.AlbumId =al.AlbumId 
                and t.GenreId =g.GenreId and i.InvoiceId = ic.InvoiceId  and ic.TrackId = t.TrackId 
                and g.Name = %s
                group by a.ArtistId , a.Name
                """

        cursor.execute(query, (genere.Name,))
        idMapPopolarity = {}

        for row in cursor:
            idMapPopolarity[row["ArtistId"]] = row["popularity"]


        cursor.close()
        conn.close()
        return idMapPopolarity

    @staticmethod
    def getClienteArtista(genere):  # 1 - poi aggiungere questo nel model

            conn = DBConnect.get_connection()
            results = []

            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT DISTINCT i.CustomerId, a.ArtistId
                FROM invoice i, invoiceline ic, track t, album al, artist a, genre g
                WHERE i.InvoiceId = ic.InvoiceId
                AND ic.TrackId = t.TrackId
                AND t.AlbumId = al.AlbumId
                AND al.ArtistId = a.ArtistId
                AND t.GenreId = g.GenreId
                AND g.Name = %s
            """

            cursor.execute(query, (genere.Name,))

            for row in cursor:
                results.append(row)

            cursor.close()
            conn.close()
            return results
