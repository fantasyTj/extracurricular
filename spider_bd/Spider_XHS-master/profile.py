import requests
import pandas as pd

from xhs_utils.xhs_util import get_headers, check_cookies, handle_profile_info, download_media, check_and_create_path, norm_str, save_user_detail

class Profile:
    def __init__(self, cookies=None):
        if cookies is None:
            self.cookies = check_cookies()
        else:
            self.cookies = cookies

    # 个人信息主页
    def get_profile_info(self, url):
        headers = get_headers()
        response = requests.get(url, headers=headers, cookies=self.cookies)
        html_text = response.text
        userId = url.split('/')[-1]
        profile = handle_profile_info(userId, html_text)
        return profile

    def save_profile_info(self, url):
        profile = self.get_profile_info(url)
        # print(profile.ipLocation)
        print(f'开始保存用户{profile.nickname}基本信息')
        userId = profile.userId
        nickname = norm_str(profile.nickname)
        path = f'./datas/{nickname}_{userId}'
        check_and_create_path(path)
        download_media(path, 'avatar', profile.avatar, 'image', '用户头像')
        save_user_detail(path, profile)
        print(f'User {nickname} 信息保存成功')
        return profile

    def get_ip(self, url):
        try:
            profile = self.get_profile_info(url)
            return profile
        except:
            return ''
        # return profile


    # def main(self, user_url_list):
    #     for url in user_url_list:
    #         try:
    #             self.save_profile_info(url)
    #         except:
    #             print(f'user {url} 查询失败')

    def main(self, csv_list):
        base_url = 'https://www.xiaohongshu.com/user/profile'
        for csv in csv_list:
            print(f'begin {csv}')
            df = pd.read_csv(csv)
            for index, row in df.iterrows():
                print(f'begin {index}')
                user_id = row['user_id']
                user_url = '/'.join([base_url, user_id])
                ip = self.get_ip(user_url)
                df.loc[index, 'ip_location'] = ip
            df.to_csv(csv, index=False, encoding='utf_8')


            


if __name__ == '__main__':
    profile = Profile()
    csv_list = [
        # r'D:\Courses\AIplus\spider_bd\postprocess\xhs\data\detail_comment_2023-12-19.csv',
        # r'D:\Courses\AIplus\spider_bd\postprocess\xhs\data\search_comment_2023-12-23.csv',
        r'D:\Courses\AIplus\spider_bd\postprocess\xhs\data\search_comment_2023-12-24.csv'
    ]
    # user_url_list = [
    #     'https://www.xiaohongshu.com/user/profile/59d44fd66eea883eff45747f',
    #     'https://www.xiaohongshu.com/user/profile/6185ce66000000001000705b',
    # ]
    profile.main(csv_list)
