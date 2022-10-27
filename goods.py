import cmd, sqlite3

CLI_VERSION = '1.1'

class goodsShell(cmd.Cmd):
	intro = 'Help Goods %s\nType \'help\' or \'?\' to show all commands.' % CLI_VERSION
	prompt = '(goods) '

	def __init__(self):
		super(goodsShell, self).__init__()
		self.conn = sqlite3.connect('goods.db')
		self.cur = self.conn.cursor()
		self.cur.execute('CREATE TABLE IF NOT EXISTS GOODS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL);')

	def do_add(self, arg):
		'add <item1> <item2> ...\nAdd items, seperated by space.'
		items = str(arg).split()
		for item in items:
			self.cur.execute('INSERT INTO GOODS (NAME) VALUES ("%s");' % item)
		self.conn.commit()
		print('Added %d item(s)' % len(items))
	def do_del(self, arg):
		'del <item1> <item2> ...\nDelete items, seperated by space.'
		items = str(arg).split()
		for item in items:
			self.cur.execute('SELECT * FROM GOODS WHERE NAME = "%s";' % item)
			if not self.cur.fetchone():
				print('Error: %s Not Found' % item)
				return
		for item in items:
			self.cur.execute('DELETE FROM GOODS WHERE ROWID IN (SELECT ID FROM GOODS WHERE NAME = "%s" LIMIT 1);' % item)
		self.conn.commit()
		print('Deleted %d item(s)' % len(items))
	def do_list(self, arg):
		'List all items.'
		self.cur.execute('SELECT * FROM GOODS;')
		for record in self.cur.fetchall(): print(record[1])
	def do_search(self, arg):
		'search <item>\nSearch for item.'
		self.cur.execute('SELECT * FROM GOODS WHERE NAME LIKE "%%%s%%";' % arg)
		records = self.cur.fetchall()
		if not records:
			print('%s Not Found' % arg)
		for record in records: print(record[1])
	def do_reset(self, arg):
		'Reset Database.'
		self.cur.execute('DROP TABLE GOODS')
		self.cur.execute('CREATE TABLE GOODS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL);')
		self.conn.commit()
		print('Reset Database')
	def do_exit(self, arg):
		'Exit Goods CLI.'
		self.cur.close()
		self.conn.close()
		print('See you~')
		return True

if __name__ == '__main__':
	goodsShell().cmdloop()