import os
from bottle import route, run
import vk_api
import json
from dotenv import load_dotenv
load_dotenv()

project_folder = os.path.expanduser('./')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

# あとで共通化する

@route('/')
def main():
  return 'working!' 

@route('/user/<username>')
def scrape_all_tweet(username):
  return 'UserData: \n %s' % username

@route('/user/login')
def login():
  login, password = os.getenv("ID"), os.getenv("PASS")
  vk_session = vk_api.VkApi(login, password)
  try:
      vk_session.auth(token_only=True)
      return 'loggin!'
  except vk_api.AuthError as error_msg:
      print(error_msg)
      return

@route('/user/wall', 'GET')
def wall():
  login, password = os.getenv("ID"), os.getenv("PASS")
  vk_session = vk_api.VkApi(login, password)
  vk = vk_session.get_api()
  response = vk.wall.get()
  return response

@route('/items/example', 'GET')
def get_example_items():
  login, password = os.getenv("ID"), os.getenv("PASS")
  vk_session = vk_api.VkApi(login, password)
  vk_session.auth()

  vk = vk_session.get_api()
  items = vk.junction.getFeed(count=3, offset=1)
  json_data = json.dumps(items, ensure_ascii=False, indent=2)
  return json_data

@route('/items/categories', 'GET')
def get_categories():
  login, password = os.getenv("ID"), os.getenv("PASS")
  vk_session = vk_api.VkApi(login, password)
  vk_session.auth()

  vk = vk_session.get_api()
  # countは50でoffset を　150まで　3回回せば全部取れる
  items = vk.junction.getCategories(count=50, offset=1)
  json_data = json.dumps(items, ensure_ascii=False, indent=2)
  return json_data

@route('/items/ids', 'GET')
def get_by_ids():
  login, password = os.getenv("ID"), os.getenv("PASS")
  vk_session = vk_api.VkApi(login, password)
  vk_session.auth()

  vk = vk_session.get_api()
  items = vk.junction.getByIds(ids=32982960941)
  json_data = json.dumps(items, ensure_ascii=False, indent=2)
  return json_data

@route('/items/by_categories', 'GET')
def get_by_categories():
  login, password = os.getenv("ID"), os.getenv("PASS")
  vk_session = vk_api.VkApi(login, password)
  vk_session.auth()

  vk = vk_session.get_api()
  items = vk.junction.getByCategory(category_id=3, offset=1, limit=20)
  json_data = json.dumps(items, ensure_ascii=False, indent=2)
  return json_data  

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)