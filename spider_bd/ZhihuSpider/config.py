import os

# 需要爬取知乎回答问题的链接
urls = [
    'https://www.zhihu.com/question/627160401', # 如何看待全国捕杀流浪猫狗？
    'https://www.zhihu.com/question/627005901', # 对于当前全国处理流浪狗，你有什么想说的？
    'https://www.zhihu.com/question/412417900', # 为什么有些人愿意喂养流浪狗，却没几个愿意带回家？
    'https://www.zhihu.com/question/627145083', # 如何看待明星为流浪狗发声？
    'https://www.zhihu.com/question/627059587', # 一人被狗咬，所有流浪狗都要遭殃吗。?
    'https://www.zhihu.com/question/627176243', # 明星接二连三呼吁保护流浪狗，是真的善良还是为了热度？
    'https://www.zhihu.com/question/627135245', # 我国流浪狗高达4000万只，该如何处理？
    'https://www.zhihu.com/question/628287767', # 一只流浪狗犯错，却要所有流浪狗共同承担，这折射出了什么社会现实？
    'https://www.zhihu.com/question/627259475', # 怎样反驳“你觉得被捕杀的流浪狗可怜你就多收养”？
    ]

# 将爬取的数据存储于Results文件中
results_path = os.path.join(os.getcwd(), 'Results')