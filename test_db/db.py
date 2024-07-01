import sqlite3

connect = sqlite3.connect("exemple.db")
cursor = connect.cursor()
cursor.execute("INSERT INTO 게시물 VALUES ('안녕하세요.', '첫 번째 포스팅이네요!', '만나서 반갑습니다.', '2007-01-01 10:00:00', '2007-01-01 10:00:00')")
connect.commit()
connect.close()