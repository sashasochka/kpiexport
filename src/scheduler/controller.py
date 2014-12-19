"""Controller

This is a module for controller/handlers
"""

import tornado

import os

from scheduler.view import BaseHandler


class MainHandler(BaseHandler):
    """Main Handler"""
    def get(self):
        self.render(os.path.join(self.settings['static_path'], 'index.html'))


class UserPortfolioHandler(BaseHandler):
    """Portfolio Handler"""
    #@tornado.web.authenticated
    def get(self):
        print(self.current_user)
        args = {}

        try:
            args['user'] = self.get_secure_cookie('facebook_name').decode('utf8')
        except:
            pass
        try:
            args['avatar'] = self.get_secure_cookie('facebook_picture_url').decode('utf-8')
        except:
            pass

        self._return('users/portfolio.html', **args)


class LoginHandler(BaseHandler):
    """Main Handler"""
    def get(self):
        self._return('users/login.html', user=self.get_secure_cookie('user')) \
                if not self.get_secure_cookie('user') else \
                self.redirect(self.get_argument('next','/'))

    def post(self):
        self.set_secure_cookie('user', self.get_argument('name'))
        self.redirect(self.get_argument('next','/'))


class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                    redirect_uri='{}/login/google'.format(self.settings['app_uri']),
                    code=self.get_argument('code'))
            #print(user)
            # Save the user with e.g. set_secure_cookie
            self.set_cookie('google_expires_in', str(user['expires_in']))
            self.set_cookie('google_access_token', user['access_token'])
            self.set_cookie('google_token_type', user['token_type'])
            self.set_cookie('google_id_token', user['id_token'])
            self.redirect('/')
        else:
            yield self.authorize_redirect(
                redirect_uri='{}/login/google'.format(self.settings['app_uri']),
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email', 'https://www.googleapis.com/auth/calendar'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


#class MainHandler(tornado.web.RequestHandler,
#                  tornado.auth.FacebookGraphMixin):
#    @tornado.web.authenticated
#    @tornado.gen.coroutine
#    def get(self):
#        new_entry = yield self.facebook_request(
#            "/me/feed",
#            post_args={"message": "I am posting from my Tornado application!"},
#            access_token=self.current_user["access_token"])
#
#        if not new_entry:
#            # Call failed; perhaps missing permission?
#            yield self.authorize_redirect()
#            return
#        self.finish("Posted a message!")


class FacebookGraphLoginHandler(LoginHandler, tornado.auth.FacebookGraphMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                redirect_uri='{}/login/facebook'.format(self.settings['app_uri']),
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))
            # Save the user with e.g. set_secure_cookie
            #print(self.reverse_url('login'))
            #print(user)
            self.set_secure_cookie('facebook_session_expires', user['session_expires'][0].decode())
            self.set_secure_cookie('facebook_access_token', user['access_token'])
            self.set_secure_cookie('facebook_id', user['id'])
            self.set_secure_cookie('facebook_link', user['link'])
            self.set_secure_cookie('facebook_locale', user['locale'])
            self.set_secure_cookie('facebook_name', user['name'])
            self.set_secure_cookie('facebook_last_name', user['last_name'])
            self.set_secure_cookie('facebook_first_name', user['first_name'])
            self.set_secure_cookie('facebook_picture_url', user['picture']['data']['url'])
            self.set_secure_cookie('user', user['name'])  # just a fallback
            self.redirect('/')
        else:
            yield self.authorize_redirect(
                redirect_uri='{}/login/facebook'.format(self.settings['app_uri']),
                client_id=self.settings["facebook_api_key"],
                extra_params={"scope": "read_stream,offline_access"})


#class MainHandler(tornado.web.RequestHandler,
#                  tornado.auth.FacebookMixin):
#    @tornado.web.authenticated
#    @tornado.web.asynchronous
#    def get(self):
#        self.facebook_request(
#            method="stream.get",
#            callback=self._on_stream,
#            session_key=self.current_user["session_key"])
#
#    def _on_stream(self, stream):
#        if stream is None:
#           # Not authorized to read the stream yet?
#           self.redirect(self.authorize_redirect("read_stream"))
#           return
#        self.render("stream.html", stream=stream)


class TwitterLoginHandler(tornado.web.RequestHandler,
                          tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            # Save the user using e.g. set_secure_cookie()
            print(user)
            self.set_secure_cookie('twitter_username', user['username'])
            self.set_secure_cookie('twitter_profile_image_url_https', user['profile_image_url_https'])
            self.set_secure_cookie('twitter_name', user['name'])
            self.set_secure_cookie('user', user['name'])  # just a fallback
            self.redirect('/')
        else:
            yield self.authorize_redirect()


#class MainHandler(tornado.web.RequestHandler,
#                  tornado.auth.TwitterMixin):
#    @tornado.web.authenticated
#    @tornado.gen.coroutine
#    def get(self):
#        new_entry = yield self.twitter_request(
#            "/statuses/update",
#            post_args={"status": "Testing Tornado Web Server"},
#            access_token=self.current_user["access_token"])
#        if not new_entry:
#            # Call failed; perhaps missing permission?
#            yield self.authorize_redirect()
#            return
#        self.finish("Posted a message!")


class FriendFeedLoginHandler(tornado.web.RequestHandler,
                             tornado.auth.FriendFeedMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            # Save the user using e.g. set_secure_cookie()
        else:
            yield self.authorize_redirect()


#class MainHandler(tornado.web.RequestHandler,
#                  tornado.auth.FriendFeedMixin):
#    @tornado.web.authenticated
#    @tornado.gen.coroutine
#    def get(self):
#        new_entry = yield self.friendfeed_request(
#            "/entry",
#            post_args={"body": "Testing Tornado Web Server"},
#            access_token=self.current_user["access_token"])
#
#        if not new_entry:
#            # Call failed; perhaps missing permission?
#            yield self.authorize_redirect()
#            return
#        self.finish("Posted a message!")


#@routes("/logout/", name="logout")
#class AuthLogoutHandler(AuthHandler):
class AuthLogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(self.get_argument("next", "/"))
