client_id = '350544127285579'
client_secret = '3a00165c394dff0bcf7c0bda05b1ed43'

# OAuth endpoints given in the Facebook API documentation
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
redirect_uri = 'https://127.0.0.1/facebook/'     # Should match Site URL

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
facebook = facebook_compliance_fix(facebook)

# Redirect user to Facebook for authorization
authorization_url, state = facebook.authorization_url(authorization_base_url)
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

 # Fetch the access token
facebook.fetch_token(token_url, client_secret=client_secret,
                     authorization_response=redirect_response)

print(facebook)
# Fetch a protected resource, i.e. user profile
r = facebook.get('https://graph.facebook.com/me?')
print(r.content)
r = facebook.get('https://graph.facebook.com/me/picture?type=square')
print(r.content)

