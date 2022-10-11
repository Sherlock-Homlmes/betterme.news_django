from .main import r
import attr
from main.views.discord_user import get_discord_user

### command for linux :
# sudo service redis-server {start|stop|restart|force-reload|status}

def redis_add_dict(key,value):
	value = r.hmset(key,value)

def redis_find_dict(key):
	value = r.hgetall(key)
	print(value)

	if value == None:
		#do something
		pass

	return value

@attr.s(slots=True)
class DiscordUser(object):

	id : int = attr.ib(default=None)
	avatar_url : str = attr.ib(default=None)
	username : str = attr.ib(default=None)
	discriminator : str = attr.ib(default=None)
	is_verified :  bool = attr.ib(default=None)
	mail : str = attr.ib(default=None)

class DiscordUserOauth():

	@staticmethod
	def set_user(token):
		current_user = get_discord_user(token)
		if current_user:
			user_data = {
				'user_id': current_user.id,
				'avatar_url': current_user.avatar_url,
				'username': current_user.username,
				'discriminator': current_user.discriminator,
				'is_verified': str(current_user.is_verified),
				'email':current_user.email
			}

			r.hmset(token,user_data)
			r.expire(name=token, time=1800)
			return user_data

		else:
			return None

	@staticmethod
	def get_user(token):
		if token:
			user = r.hgetall(token)
		else:
			user = None

		if user:
			user_id =  user['user_id']
		else:
			user = DiscordUserOauth.set_user(token)
			if user:
				user_id = user['user_id']
			else:
				user_id = None

		if user_id:

			return DiscordUser(
				int(user_id),
				user['avatar_url'],
				user['username'],
				user['discriminator'],
				bool(user['is_verified']),
				user['email']
				)


	def __new__(self,request):

		self.token = request.COOKIES.get("discord_access_token")
		return self.get_user(self.token)




			


### build project
	# check position of news_post
				#
				# excist: take from redis
				#
				# not excist: take from database

### improve
	# build dict in redis function