#!/usr/bin/env python3
import cmd, sqlite3, prettytable

CLI_VERSION = '2.0.1'

class goodsShell(cmd.Cmd):
	intro = 'Help Goods %s\nType \'help\' or \'?\' to show all commands.' % CLI_VERSION
	prompt = '(goods) '

	def __init__(self):
		super(goodsShell, self).__init__()
		self.conn = sqlite3.connect('goods.db')
		self.cur = self.conn.cursor()
		self.cur.execute('CREATE TABLE IF NOT EXISTS GOODS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, QUANTITY INT);')

	def do_add(self, arg):
		'Usage: add <item1> <quantity1> <item2> <quantity2> ...\nAdd items, seperated by space.'
		args = str(arg).split()
		item = ''
		added, updated = 0, 0
		for argi in args:
			if item:
				quantity = int(argi) if argi.isdigit() else 1
				self.cur.execute('SELECT * FROM GOODS WHERE NAME = "%s";' % item)
				if record := self.cur.fetchone():
					self.cur.execute('UPDATE GOODS SET QUANTITY = %d WHERE NAME = "%s"' % (record[2] + quantity, item))
					updated += 1
				else:
					self.cur.execute('INSERT INTO GOODS (NAME, QUANTITY) VALUES ("%s", %d);' % (item, quantity))
					added += 1
				item = '' if argi.isdigit() else argi
			else: item = argi
		if item:
			quantity = 1
			self.cur.execute('SELECT * FROM GOODS WHERE NAME = "%s";' % item)
			if record := self.cur.fetchone():
				self.cur.execute('UPDATE GOODS SET QUANTITY = %d WHERE NAME = "%s"' % (record[2] + quantity, item))
				updated += 1
			else:
				self.cur.execute('INSERT INTO GOODS (NAME, QUANTITY) VALUES ("%s", %d);' % (item, quantity))
				added += 1
		self.conn.commit()
		if added and updated: print('Added %d item(s), updated %d item(s)' % (added, updated))
		else:
			if added: print('Added %d item(s)' % added)
			if updated: print('Updated %d item(s)' % updated)

	def do_del(self, arg):
		'Usage: del <item1> <quantity1> <item2> <quantity2> ...\nDelete items, seperated by space.'
		args = str(arg).split()
		item = ''
		deleted, updated = 0, 0
		for argi in args:
			if item:
				quantity = int(argi) if argi.isdigit() else 1
				self.cur.execute('SELECT * FROM GOODS WHERE NAME = "%s";' % item)
				if record := self.cur.fetchone():
					if record[2] < quantity:
						print('Error: Attempt to delete %d of %s, but it only has %d.' % (quantity, record[1], record[2]))
						return
					if record[2] == quantity:
						self.cur.execute('DELETE FROM GOODS WHERE NAME = "%s"' % record[1])
						deleted += 1
					else:
						self.cur.execute('UPDATE GOODS SET QUANTITY = %d WHERE NAME = "%s"' % (record[2] - quantity, item))
						updated += 1
				else:
					print('Error: %s Not Found!' % item)
					return
				item = '' if argi.isdigit() else argi
			else: item = argi
		if item:
			quantity = 1
			self.cur.execute('SELECT * FROM GOODS WHERE NAME = "%s";' % item)
			if record := self.cur.fetchone():
				if record[2] < quantity:
					print('Error: Attempt to delete %d of %s, but it only has %d.' % (quantity, record[1], record[2]))
					return
				if record[2] == quantity:
					self.cur.execute('DELETE FROM GOODS WHERE NAME = "%s"' % record[1])
					deleted += 1
				else:
					self.cur.execute('UPDATE GOODS SET QUANTITY = %d WHERE NAME = "%s"' % (record[2] - quantity, item))
					updated += 1
			else:
				print('Error: %s Not Found!' % item)
				return
		self.conn.commit()
		if deleted and updated: print('Deleted %d item(s), updated %d item(s)' % (deleted, updated))
		else:
			if deleted: print('Deleted %d item(s)' % deleted)
			if updated: print('Updated %d item(s)' % updated)

	def do_list(self, arg):
		'List all items.'
		self.cur.execute('SELECT * FROM GOODS;')
		result = prettytable.PrettyTable()
		result.field_names = ('Name', 'Quantity')
		for record in self.cur.fetchall(): result.add_row(record[1:])
		print(result)

	def do_search(self, arg):
		'Usage: search <item1> <item2> ...\nSearch for item.'
		items = str(arg).split()
		for item in items:
			print('Search for %s:' % item)
			self.cur.execute('SELECT * FROM GOODS WHERE NAME LIKE "%%%s%%";' % item)
			if records := self.cur.fetchall():
				result = prettytable.PrettyTable()
				result.field_names = ('Name', 'Quantity')
				for record in records: result.add_row(record[1:])
				print(result)
			else: print('%s Not Found!' % item)

	def do_reset(self, arg):
		'Reset Database.'
		self.cur.execute('DROP TABLE GOODS')
		self.cur.execute('CREATE TABLE GOODS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, QUANTITY INT);')
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