import cmd

class goodsShell(cmd.Cmd):
	intro = '欢迎使用 Goods 交互式环境。键入 help 或者 ? 查看所有命令。\n'
	prompt = '(goods) '

	def do_add(self, arg):
		pass
	def do_del(self, arg):
		pass
	def do_list(self, arg):
		pass
	def do_search(self, arg):
		pass
	def do_exit(self, arg):
		return True

if __name__ == '__main__':
	goodsShell().cmdloop()