#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# Chmouel Boudjnah <chmouel@chmouel.com>
#
# This is blatlantly copied almost word from word from this twitter
# oauth library : http://code.google.com/p/oauth-python-twitter/
#
import urllib2
import urlparse
import time

import simplejson
import oauth2 as oauth

REQUEST_TOKEN_URL = 'http://dailyburn.com/api/oauth/request_token'
ACCESS_TOKEN_URL = 'http://dailyburn.com/api/oauth/access_token'
AUTHORIZATION_URL = 'http://dailyburn.com/api/oauth/authorize'

class OAuthApi:
    def __init__(self, consumer_key, consumer_secret, token=None, token_secret=None):
        if token and token_secret:
            token = oauth.Token(token, token_secret)
        else:
            token = None
        self._Consumer = oauth.Consumer(consumer_key, consumer_secret)
        self._signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self._access_token = token 

    def _GetOpener(self):
        opener = urllib2.build_opener()
        return opener

    
    def _FetchUrl(self,
                  url,
                  http_method=None,
                  parameters=None):
        '''Fetch a URL, optionally caching for a specified time.
        
        Args:
        url: The URL to retrieve
        http_method: 
        One of "GET" or "POST" to state which kind 
        of http call is being made
        parameters:
        A dict whose key/value pairs should encoded and added 
        to the query string, or generated into post data. [OPTIONAL]
        depending on the http_method parameter
        
        Returns:
        A string containing the body of the response.
        '''
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
            extra_params.update(parameters)
        
        req = self._makeOAuthRequest(url, params=extra_params, 
                                     http_method=http_method)

        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
            # Removed the following line due to the fact that OAuth2 request objects do not have this function
            # This does not appear to have any adverse impact on the operation of the toolset
            #url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ""
            
        if encoded_post_data:
            url_data = opener.open(url, encoded_post_data).read()
        else:
            url_data = opener.open(url).read()
        opener.close()

        # Always return the latest version
        return url_data
    
    def _makeOAuthRequest(self, url, token=None,
                          params=None, http_method="GET"):
        '''Make a OAuth request from url and parameters
        
        Args:
        url: The Url to use for creating OAuth Request
        parameters:
        The URL parameters
        http_method:
        The HTTP method to use
        Returns:
        A OAauthRequest object
        '''
        
        oauth_base_params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time())
            }
        
        if params:
            params.update(oauth_base_params)
        else:
            params = oauth_base_params
        
        if not token:
            token = self._access_token
        request = oauth.Request(method=http_method,url=url,parameters=params)
        request.sign_request(self._signature_method, self._Consumer, token)
        return request

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        '''Create a signed authorization URL
        
        Authorization provides the user with a VERIFIER which they may in turn provide to
        the consumer.  This key authorizes access.  Used primarily for clients.
        
        Returns:
        A signed OAuthRequest authorization URL 
        '''
        return "%s?oauth_token=%s" % (url, token['oauth_token'])

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        '''Get a Request Token from Dailyburn
        
        Returns:
        A OAuthToken object containing a request token
        '''
        resp, content = oauth.Client(self._Consumer).request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        return dict(urlparse.parse_qsl(content))
    
    def getAccessToken(self, token, verifier=None, url=ACCESS_TOKEN_URL):
        '''Get a Request Token from Dailyburn
        
        Note: Verifier is required if you AUTHORIZED, it can be skipped if you AUTHENTICATED
        
        Returns:
        A OAuthToken object containing a request token
        '''
        token = oauth.Token(token['oauth_token'], token['oauth_token_secret'])
        if verifier:
            token.set_verifier(verifier)
        client = oauth.Client(self._Consumer, token)
        
        resp, content = client.request(url, "POST")
        return dict(urlparse.parse_qsl(content))

    def UrlCall(self, call, type="GET", parameters={}):
        print "https://dailyburn.com/api/" + call + ".json", type, parameters
        
    def ApiCall(self, call, type="GET", parameters={}):
        '''Calls the Dailyburn API
        
        Args:
        call: The name of the api call (ie. account/rate_limit_status)
        type: One of "GET" or "POST"
        parameters: Parameters to pass to the Dailyburn API call
        Returns:
        Returns the Dailyburn.User object
        '''
        # We use this try block to make the request in case we run into one of Dailyburn's many 503 (temporarily unavailable) errors.
        # Other error handling may end up being useful as well.
        try:
            json = self._FetchUrl("https://dailyburn.com/api/" + call + ".json", type, parameters)
            # This is the most common error type you'll get.
            # Dailyburn is good about returning codes, too Chances are
            # that most of the time you run into this, it's going to
            # be a 503 "service temporarily unavailable".  That's a
            # fail whale.
        except urllib2.HTTPError, e:
            return e
        # Getting an URLError usually means you didn't even hit
        # Dailyburn's servers.  This means something has gone
        # TERRIBLY WRONG somewhere.
        except urllib2.URLError, e:
            return e
        else:
            return simplejson.loads(json)

if __name__ == '__main__':
    pass
