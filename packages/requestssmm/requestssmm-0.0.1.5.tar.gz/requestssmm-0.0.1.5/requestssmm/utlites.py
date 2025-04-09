from requests import get,post,Session
import requests,re
import base64,uuid,json,time
from mahdix import *
from fb_atm import Page
class Botgp:
    def __init__(self):
        pass
    
        
    def share_facebook_post_EAAGN(self,token, id_share,cookie,privacy='0'):
        try:
            """
            Share a post on Facebook using the Facebook Graph API.
            :param token: Facebook access token [EAAGNO...........]
            :param post_url: URL of the post to share
            :param privacy: Privacy setting for the post (default: SELF)
            Returns:
                Grapg api respone
            """
            he = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate',
                'connection': 'keep-alive',
                'content-length': '0',
                'cookie': cookie,
                'host': 'graph.facebook.com'
            }
            response = post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published={privacy}&access_token={token}', headers=he).json()
            if 'id' in response:
                return (True,response)
        except Exception as e:
            return (False,e)
    def comment_post_EAAGN(self,post_id='9000855519965854',message='ma4D1',token=None,cookes=None):
        try:
            """
            Comment on a post on Facebook using the Facebook Graph API.
            :param token: Facebook access token [EAAGNO...........]
            :param post_url: URL of the post to share
            :param privacy: Privacy setting for the post (default: SELF)
            Returns:
            Grapg api respone
            """
            if token and cookes :
                response=post(f"https://graph.facebook.com/{post_id}/comments/?message={message}&access_token={token}", headers = {"cookie":cookes}).json()
                if 'id' in response:
                    return (True,response)
        except Exception as e:
            return (False,e)


class EAAAAU(Botgp):
    def __init__(self):
        super().__init__()
        #--> Access Token (EAAU from b-graph login)
        pass
    def share_facebook_post_EAAAAU(self,token, post_url,privacy='SELF'):
        try:
            """
            Share a post on Facebook using the Facebook Graph API.
            :param token: Facebook access token [EAAAAUaZA8...........]
            :param post_url: URL of the post to share
            :param privacy: Privacy setting for the post (default: SELF)
            Returns:
                Grapg api respone
            """
            fb_url = 'https://graph.facebook.com/v13.0/me/feed'
            data = {'link': post_url, 'published': '0', 'privacy': '{"value":"%s"}'%(privacy), 'access_token': token}
            response = post(fb_url, data=data).json()
            if 'id' in response:
                return (True,response)
        except Exception as e:
            return (False,e)
        
    def follow_EAAAAU(self,terge_id=None,Token=None):
        """_summary_
        This a function to follow a user on Facebook using the Facebook Graph API.
         token after loging use graph api
        Args:
            terge_id (_type_, optional): _description_. Defaults to None.
            Token (_type_, optional): _description_. Defaults to None.
             #--> Access Token (EAAU from b-graph login)

        Returns:
            _type_: _description_
        """
        try:
            if terge_id and Token:
                response=post(f'https://graph.facebook.com/{terge_id}/subscribers?access_token={Token}').json()
                return True,response
        except Exception as e:
            return (False,e)
    def pgLike_EAAAAU(self,terge_id=None,Token=None):
        """_summary_
        This a function to page like a user on Facebook using the Facebook Graph API.
         token after loging use graph api
        Args:
            terge_id (_type_, optional): _description_. Defaults to None.
            Token (_type_, optional): _description_. Defaults to None.
             #--> Access Token (EAAU from b-graph login)
        Returns:
            _type_: _description_
        """
        try:
            if terge_id and Token:
                response=post(f'https://graph.facebook.com/{terge_id}/likes?access_token={Token}').json()
                return True,response
        except Exception as e:
            return (False,e)
    def post_reaction_EAAAAU(self,actor_id:str, post_id:str, react:str, token:str):
        r    = Session()
        var  = {"input":{"feedback_referrer":"native_newsfeed","tracking":[None],"feedback_id":str(base64.b64encode(('feedback:{}'.format(post_id)).encode('utf-8')).decode('utf-8')),"client_mutation_id":str(uuid.uuid4()),"nectar_module":"newsfeed_ufi","feedback_source":"native_newsfeed","attribution_id_v2":"NewsFeedFragment,native_newsfeed,cold_start,1710331848.276,264071715,4748854339,,","feedback_reaction_id":react,"actor_id":actor_id,"action_timestamp":str(time.time())[:10]}}
        data = {'access_token':token,'method':'post','pretty':False,'format':'json','server_timestamps':True,'locale':'id_ID','fb_api_req_friendly_name':'ViewerReactionsMutation','fb_api_caller_class':'graphservice','client_doc_id':'2857784093518205785115255697','variables':json.dumps(var),'fb_api_analytics_tags':["GraphServices"],'client_trace_id':str(uuid.uuid4())}
        pos  = r.post('https://graph.facebook.com/graphql', data=data).json()
        try:
            if react in str(pos):
                return(True,pos['data']['feedback_react']['feedback']['reactors']['count'])
               
            else: return(False,'React Failed!')
        except Exception: return(False,'React Failed!')
        
        

class Cookees(Page):
    def __init__(self):
        super().__init__()
        self.headers= {
        'authority': 'mbasic.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8,nl;q=0.7,pt;q=0.6',
        'cache-control': 'max-age=0',
        'dpr': '12',
        'referer': 'https://mbasic.facebook.com/photo/?fbid=778900340946473&set=a.598020855701090',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6262.5", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6262.5"',
        'sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent':W_ueragnt() ,'viewport-width': '673',
        "ysafb":"24"}
    def react_post(self,__cok, __url, __react):
        try:
            react_type = ['Like','Love','Haha','Wow','Care','Sad','Angry'][__react-1]
            react      = ['1635855486666999','1678524932434102','115940658764963','478547315650144','613557422527858','908563459236466','444813342392137'][__react-1]
            data_responce=requests.get(__url,headers=self.headers_web,cookies=self.fromate_cookes(__cok)).text
            try: feedback_id = re.search('"feedback":{"associated_group":null,"id":"(.*?)"},"is_story_civic":null',str(data_responce)).group(1)
            except Exception as e: feedback_id = re.search('"feedback":{"id":"(.*?)"',str(data_responce)).group(1)
            session_id = re.search(r'"sessionID":"(.*?)"',str(data_responce)).group(1)
            uidx = re.search(r'__user=(.*?)&', str(data_responce)).group(1)
            fb_dtsg = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', str(data_responce)).group(1)
            jazoest = re.search(r'&jazoest=(.*?)",', str(data_responce)).group(1)
            lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', str(data_responce)).group(1)
            data = {
            'av': uidx,
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'lsd': lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'variables': '{"input":{"attribution_id_v2":"CometPhotoRoot.react,comet.mediaviewer.photo,unexpected,1727623102922,48437,,,;CometHomeRoot.react,comet.home,via_cold_start,1727623004088,438841,4748854339,12#15#301,8760540677331341","feedback_id":"%s","feedback_reaction_id":"%s","feedback_source":"MEDIA_VIEWER","is_tracking_encrypted":true,"tracking":[""],"session_id":"%s","actor_id":"%s","client_mutation_id":"4"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}'%(feedback_id,react,session_id,uidx),
            'server_timestamps': 'true',
            'doc_id': '8030707243693006',
        }
            response = requests.post('https://www.facebook.com/api/graphql/', cookies=self.fromate_cookes(__cok), headers=self.headers, data=data).text
            if '"data":{"feedback_react":{"feedback":{"id":"' in str(response):
                return True,re.search('"reactors":{"count":(.*?),',str(response)).group(1)
                
            else:
                return False,"account error"

        except  Exception as e:
            return False,str(e)
    def get_data(self,req):
        try:
            av= re.search('"actorID":"(.*?)"', str(req)).group(1)
            __hs= re.search('"haste_session":"(.*?)",', str(req)).group(1)
            __rev= re.search('{"rev":(.*?)}', str(req)).group(1)
            __hsi= re.search('"hsi":"(.*?)",', str(req)).group(1)
            fb_dtsg= re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', str(req)).group(1)
            jazoest= re.search('&jazoest=(.*?)",', str(req)).group(1)
            lsd= re.search(r'"LSD",\[\],{"token":"(.*?)"', str(req)).group(1)
            __spin_r= re.search('"__spin_r":(.*?),', str(req)).group(1)
            __spin_t= re.search('"__spin_t":(.*?),', str(req)).group(1)
            __comet_req = re.search('__comet_req=(.*?)&', str(req)).group(1)
            _req =  re.search('_req=(.*?)&', str(req)).group(1)
            data = {
                '__s': 'mr42k3:0gsl5n:9smutq',
                'av': av,
                '__aaid': '0',
                '__user': av,
                '__a': '1',
                '__req': _req,
                '__hs':__hs,
                'dpr': '1',
                '__ccg': 'EXCELLENT',
                '__rev': __rev,
                '__hsi': __hsi,
                '__comet_req': __comet_req,
                'fb_dtsg': fb_dtsg,
                'jazoest':jazoest,
                'lsd': lsd,
                '__spin_r': __spin_r,
                '__spin_b': 'trunk',
                '__spin_t':__spin_t,}
            return data
        except Exception as e:
            # print(e)
            return False
            

    def story_viwes(self,cookes:str,url:str):
        try:
            cookies =self.fromate_cookes(cookes)
            bucket_id=re.search('.com/stories/(.*?)/',str(url)).group(1)
            story_id =re.search(f'{bucket_id}/(.*?)/',str(url)).group(1)
            req=requests.get(url,cookies=cookies, headers= self.headers).text
            gets_data=self.get_data(req)
            if gets_data:
                data = {
                    '__crn': 'comet.fbweb.CometStoriesSuspenseSingleBucketViewerWithEntryPointRoute',
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'storiesUpdateSeenStateMutation',
                    'variables': '{"input":{"bucket_id":"%s","story_id":"%s","actor_id":"%s","client_mutation_id":"1"},"scale":1}'%(bucket_id,story_id,gets_data['av']),
                    'server_timestamps': 'true',
                    'doc_id': '5127393270671537',
                }
                data.update(gets_data)
                response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers= self.headers, data=data).text
                if '"is_seen_by_viewer":true' in response:
                        return True,gets_data['av']
                else :
                    return False,gets_data['av']
            if not gets_data :
                return False,' Invalid CookiesError'
        except Exception as e:
            return False,str(e)


