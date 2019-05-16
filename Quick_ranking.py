import requests,time,random,pymysql,threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def ip():
    url = 'http://www.data5u.com/'
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    ips = driver.find_elements_by_xpath('//ul[@class=\'l2\']/span[1]/li')  # 找到ip模块
    dks = driver.find_elements_by_xpath('//ul[@class=\'l2\']/span[2]/li')  # 端口
    lxs = driver.find_elements_by_xpath('//ul[@class=\'l2\']/span[4]/li')  # 类型数据
    try:
        for i in range(len(ips)):
            proxies = {
                lxs[i].text:ips[i].text+':'+dks[i].text
            }

            r = requests.get('http://icanhazip.com', proxies=proxies, timeout=5)#判断ip是否有效
            if r.status_code == 200:
                #将有效的ip写入ip_data数据库
                sql_insert = "INSERT IGNORE INTO ip_data(ip,port,types) VALUES ('%s','%s','%s')"%(ips[i].text,dks[i].text,lxs[i].text)
                cursor.execute(sql_insert)
                conn.commit()
        conn.close()
        driver.close()
    except:
        pass
        driver.close()


def xx():
    url = 'http://so.m.sm.cn/s?q=' + keyword
    #查询数据库
    sql = "select * from ip_data"
    cursor.execute(sql)
    ips = []
    for i in cursor.fetchall():
        ips.append(i[0])
    ip_data = random.choice(ips)#随机取出一个ip
    #从数据库中删除该数据
    delete = "DELETE FROM sheet WHERE ip=%s"
    cursor.execute(delete,ip_data)
    conn.close()

    PROXY = ip_data  # IP:PORT or HOST:PORT
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.set_page_load_timeout(10)


    #随机上下滑动函数
    def rand():
        time.sleep(random.randint(2,5))#随机停留1-5秒
        for i in range(random.randint(2,6)):
            driver.execute_script("window.scrollTo(%s,%s)"%(random.randint(1,300),random.randint(1,300)))
            time.sleep(random.randint(1,3))
            driver.execute_script("window.scrollTo(%s,%s)"%(random.randint(1,300),random.randint(1,300)))


    #随机点击函数
    def click():
        for i in range(3):
            time.sleep(1)
            for i in range(1,3):
                driver.execute_script("window.scrollTo(%s,%s)" % (random.randint(1, 800), random.randint(1, 500)))
                time.sleep(random.randint(1, 3))
                driver.execute_script("window.scrollTo(%s,%s)" % (random.randint(1, 800), random.randint(1, 500)))
            for j in range(30):
                time.sleep(0.5)
                x = random.randint(1,960)
                y = random.randint(1,1040)
                action = ActionChains(driver)
                action.move_by_offset(x, y).click()
                action.perform()


    num = 0
    while True:
        try:
            num += 1
            if num == 10:
                print("已查找到第十页没有数据，程序结束！")
                driver.close()
                break
            print("正在查找第",num,"页")
            divs = driver.find_elements_by_xpath('//h2/a')
            for i in divs:
                #如果指定元素在获取的元素里则点击
                if link in i.get_attribute('href'):
                    i.click()
                    click()
            rand()
            #如果不在则点击下一页
            driver.find_element_by_xpath('//div[@class="pager"]/a').click()
        except:
            driver.close()
            break


if __name__ == '__main__':
    # 创建数据表
    conn = pymysql.connect('localhost', user='root', passwd='123456', db='ip')
    cursor = conn.cursor()

    # cursor.execute('DROP TABLE IF EXISTS ip_data')
    # sql = """CREATE TABLE ip_data(
    #         ip VARCHAR(255) NOT NULL,
    #         port VARCHAR(255) NOT NULL,
    #         types VARCHAR(255) NOT NULL,
    #         PRIMARY KEY(ip)#ip主键
    # )
    # """
    # cursor.execute(sql)

    keyword = input("请输入搜索关键词：")
    link = input("请输入需要刷的域名：")
    thread = threading.Thread(target=ip)
    thread1 = threading.Thread(target=xx)
    thread.start()
    thread1.start()
    thread.join()
    thread1.join()
