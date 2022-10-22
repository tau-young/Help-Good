import cmd, sqlite3

CLI_VERSION = '1.0'

class goodsShell(cmd.Cmd):
	intro = 'Help Goods %s\n键入\'help\'或者\'?\'查看所有命令。' % CLI_VERSION
	prompt = '(goods) '

	def __init__(self):
		super(goodsShell, self).__init__()
		self.conn = sqlite3.connect('goods.db')
		self.cur = self.conn.cursor()
		self.cur.execute('CREATE TABLE IF NOT EXISTS GOODS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL);')

	def do_add(self, arg):
		'add <item>\n添加一个物品。'
		self.cur.execute('INSERT INTO GOODS (NAME) VALUES ("%s");' % arg)
		self.conn.commit()
	def do_del(self, arg):
		'del <item>\n删除一个物品。'
		self.cur.execute('DELETE FROM GOODS WHERE ROWID IN (SELECT ID FROM GOODS WHERE NAME = "%s" LIMIT 1);' % arg)
		self.conn.commit()
	def do_list(self, arg):
		'列出所有物品。'
		self.cur.execute('SELECT * FROM GOODS;')
		for record in self.cur.fetchall(): print(record[1])
	def do_search(self, arg):
		'search <item>\n查找物品。'
		self.cur.execute('SELECT * FROM GOODS WHERE NAME LIKE "%%%s%%";' % arg)
		for record in self.cur.fetchall(): print(record[1])
	def do_reset(self, arg):
		'重置数据库。'
		self.cur.execute('DROP TABLE GOODS')
		self.cur.execute('CREATE TABLE GOODS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL);')
		self.conn.commit()
	def do_exit(self, arg):
		'退出交互式环境。'
		self.cur.close()
		self.conn.close()
		return True

if __name__ == '__main__':
	goodsShell().cmdloop()