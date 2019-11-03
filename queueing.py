def add_to_queue(urls, url):
  """
  >>> urls = deque([])
  >>> list(add_to_queue(urls, 'test'))
  ['test']
  """
  urls.append(url)
  return urls

def read_from_queue(urls):
  """
  >>> urls = deque(['test', 'dwa', 'trzey'])
  >>> read_from_queue(urls)
  'test'
  """
  return urls.popleft()