from jinja2 import Environment, FileSystemLoader

persons = [{'name': 'Алексей', 'old': 18, 'weight': 78.5},
           {'name': 'Николай', 'old': 28, 'weight': 82.3},
           {'name': 'Иван', 'old': 38, 'weight': 94.5}]

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

#tm = env.get_template('html/main.html')
# msg = tm.render(users=persons)
tm = env.get_template('html/page.html')
msg = tm.render(domain='www.google.com', titile="Про Jinja2")

print(msg)