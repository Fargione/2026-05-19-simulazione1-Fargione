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
        query = """select a.Name, a.ArtistId  , sum(i.Quantity) as popolarita
                from artist a , album a2 , track t , genre g, invoiceline i
                where a.ArtistId = a2.ArtistId and a2.AlbumId = t.AlbumId 
                and t.GenreId = g.GenreId and g.Name = %s and 
                i.TrackId = t.TrackId
                group by a.ArtistId  """

        cursor.execute(query, (genre,))

        for row in cursor:
            dizio[row["ArtistId"]] = row["popolarita"]

        cursor.close()
        conn.close()
        return dizio

    @staticmethod
    def getAllEdges(genre):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            select distinct inv.CustomerId, ar.ArtistId
            from invoiceline il, invoice inv, track t, album al, artist ar, genre g
            where il.InvoiceId = inv.InvoiceId and il.TrackId = t.TrackId and t.AlbumId = al.AlbumId
              and al.ArtistId = ar.ArtistId and t.GenreId = g.GenreId and g.Name = %s
        """
        cursor.execute(query, (genre,))
        res = []
        for row in cursor:
            res.append((row["CustomerId"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return res