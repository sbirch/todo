import subprocess, sys, linecache, re
from collections import namedtuple, Counter

Match = namedtuple('Match', ['file', 'lineno', 'line'])

def is_line_comment(line):
	line = line.strip()
	return line.startswith('#') or line.startswith('//')

def is_todo(line):
	return line.find('TODO') != -1

def is_empty(line):
	return line.strip() in ['', '*']

def is_end_block_comment(line):
	return (line.find("'''") != -1 or
			line.find('"""') != -1 or
			line.find('*/') != -1 or
			line.find('-->') != -1 or
			line.find('}}') != -1 or
			line.find('-#}') != -1)

def is_trailing_comment(line):
	m = re.search('\S+\s*#\s*TODO.+$', line)
	return m is not None

def expand(match):
	all_lines = [match.line]
	if is_trailing_comment(match.line):
		pass
	elif is_line_comment(match.line):
		start = match.lineno + 1
		line = linecache.getline(match.file, start)
		while is_line_comment(line) and not is_todo(line):
			all_lines.append(linecache.getline(match.file, start))
			start += 1
			line = linecache.getline(match.file, start)
	elif not is_end_block_comment(match.line):
		start = match.lineno + 1
		line = linecache.getline(match.file, start)
		while (not is_empty(line) and
			   not is_todo(line) and
			   not is_end_block_comment(line)):
			all_lines.append(linecache.getline(match.file, start))
			start += 1
			line = linecache.getline(match.file, start)

	return all_lines
		
def extract_names(line):
	contents = re.findall('TODO\((.*?)\)', line)

	# names must be alphanumeric or _-. Commas and slash OK as seperators.
	if not all([re.match('^[a-zA-Z0-9_\-,/ ]+$', c) for c in contents]):
		return None

	names = []
	for name in contents:
		names.extend([x.strip() for x in re.split('[,/]', name)])

	return names

def get_todo_matches():
	try:
		matches = subprocess.check_output(['ack', '--with-filename', "TODO\\(.*\\)"])
	except subprocess.CalledProcessError, e:
		print e.output
		raise e
	matches = [l for l in matches.split('\n') if l.strip() != '']
	matches = [l.split(':', 2) for l in matches]
	matches = [Match(l[0], int(l[1]), l[2]) for l in matches]

	return matches

def interactive(match_names=None, show_count=False):
	matches = get_todo_matches()

	count = 0
	count_by_name = Counter()

	for match in matches:
		result_lines = expand(match)
		names = extract_names(match.line)

		if names == None:
			continue

		if match_names != []:
			if not any([n in names for n in match_names]):
				continue

		count += 1
		for n in names:
			count_by_name[n] += 1

		if not show_count:
			print '%s:%d' % (match.file, match.lineno), ', '.join(names)
			for l in result_lines:
				print l.strip()
			print
	if show_count and match_names != []:
		print '%d TODOs' % count
	elif show_count and match_names == []:
		for name, count in count_by_name.most_common():
			print name, count