from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():


    @staticmethod
    def getAllGen():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct g.Name 
                from genre g  """

        cursor.execute(query)
        res = []

        for row in cursor:
            res.append(row["Name"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllNodes(genre):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct a.*
from artist a , album a2 , track t , genre g 
where a.ArtistId = a2.ArtistId and a2.AlbumId = t.AlbumId 
and t.GenreId = g.GenreId and g.Name = %s """

        cursor.execute(query, (genre,))
        res = []

        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllPopol(genre):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        dizio = {}
        query = """select a.ArtistId, sum(i2.Quantity ) as peso
                    from invoiceline i2 , track t , album a , artist a2, genre g 
                    where i2.TrackId = t.TrackId and t.AlbumId = a.AlbumId and 
                    a2.ArtistId = a.ArtistId and t.GenreId = g.GenreId and g.Name = %s
                    group by a.ArtistId"""

        cursor.execute(query, (genre,))

        for row in cursor:
            dizio[row["ArtistId"]] = row["peso"]

        cursor.close()
        conn.close()
        return dizio

    @staticmethod
    def getAllEdges(genre):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """with tavola as (select distinct i.CustomerId , a.ArtistId 
                from invoice i , invoiceline i2 , track t , album a , artist a2, genre g 
                where i.InvoiceId = i2.InvoiceId and i2.TrackId = t.TrackId 
                and t.AlbumId = a.AlbumId and a2.ArtistId = a.ArtistId and 
                t.GenreId = g.GenreId and g.Name = %s)
                select t.artistid as primo, t2.artistid as secondo
                from tavola t ,tavola t2
                where t.customerid = t2.customerid and t.artistid > t2.artistid 
                group by t.artistid , t2.artistid """
        cursor.execute(query, (genre,))
        res = []
        for row in cursor:
            res.append((row["primo"], row["secondo"]))

        cursor.close()
        conn.close()
        return res