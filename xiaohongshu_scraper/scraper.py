import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

# Chrome浏览器路径
CHROME_PATH = "C:\\Program Files (x86)\\Chromebrowser\\chrome.exe"

class XiaohongshuScraper:
    def __init__(self):
        self.driver = None
        self.data = []
    
    def start_driver(self):
        """启动Chrome浏览器"""
        options = webdriver.ChromeOptions()
        options.binary_location = CHROME_PATH
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        
        # 使用系统Chrome驱动
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def login(self):
        """登录小红书"""
        self.driver.get("https://www.xiaohongshu.com")
        input("请在浏览器中完成登录，登录成功后按Enter键继续...")
    
    def search(self, keyword):
        """搜索关键词"""
        # 等待搜索框出现
        search_box = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='搜索']"))
        )
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        
        # 等待搜索结果加载
        time.sleep(5)
    
    def sort_by_time(self):
        """按时间倒序排序"""
        try:
            # 点击排序按钮
            sort_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '最热') or contains(text(), '最新')]"))
            )
            sort_button.click()
            
            # 选择按时间排序
            time_sort = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '最新')]"))
            )
            time_sort.click()
            time.sleep(3)
        except Exception as e:
            print(f"排序失败: {e}")
    
    def get_posts(self, max_posts=10):
        """获取帖子列表"""
        posts = []
        
        # 滚动加载更多帖子
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # 获取帖子元素
        post_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='note-item']")
        
        for i, post in enumerate(post_elements[:max_posts]):
            try:
                # 点击帖子
                post.click()
                time.sleep(3)
                
                # 切换到新打开的窗口
                if len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    
                    post_data = self.extract_post_data()
                    if post_data:
                        posts.append(post_data)
                    
                    # 关闭当前窗口
                    self.driver.close()
                    # 切换回主窗口
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(2)
            except Exception as e:
                print(f"处理帖子失败: {e}")
                continue
        
        return posts
    
    def extract_post_data(self):
        """提取帖子数据"""
        try:
            # 获取帖子ID
            post_id = self.driver.current_url.split("/")[-1].split("?")[0]
            
            # 获取帖子标题
            try:
                title = self.driver.find_element(By.CSS_SELECTOR, "h1[class*='title']").text
            except:
                title = ""
            
            # 获取帖子内容
            try:
                content = self.driver.find_element(By.CSS_SELECTOR, "div[class*='content']").text
            except:
                content = ""
            
            # 检查是否有评论
            try:
                comment_count = self.driver.find_element(By.CSS_SELECTOR, "div[class*='comment-count']").text
                if not comment_count or '评论' not in comment_count:
                    return None
            except:
                return None
            
            # 点击评论区
            try:
                comment_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='comment-button']"))
                )
                comment_button.click()
                time.sleep(2)
            except:
                pass
            
            # 滚动加载更多评论
            for _ in range(2):
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                except:
                    pass
            
            # 提取评论
            comments = []
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='comment-item']")
            
            for comment in comment_elements:
                try:
                    # 获取评论者信息
                    user_info = comment.find_element(By.CSS_SELECTOR, "div[class*='user-info']")
                    nickname = user_info.find_element(By.CSS_SELECTOR, "span[class*='nickname']").text
                    
                    # 获取评论内容
                    comment_content = comment.find_element(By.CSS_SELECTOR, "div[class*='comment-content']").text
                    
                    # 获取评论时间
                    comment_time = comment.find_element(By.CSS_SELECTOR, "span[class*='comment-time']").text
                    
                    # 分析是否对"岑村揽胜"感兴趣
                    interested, reason = self.analyze_interest(comment_content)
                    
                    comments.append({
                        "user_id": "",  # 小红书ID需要进一步解析
                        "nickname": nickname,
                        "content": comment_content,
                        "time": comment_time,
                        "interested": interested,
                        "reason": reason
                    })
                except Exception as e:
                    continue
            
            return {
                "post_id": post_id,
                "title": title,
                "content": content,
                "comments": comments
            }
        except Exception as e:
            print(f"提取帖子数据失败: {e}")
            return None
    
    def analyze_interest(self, comment):
        """分析用户是否对"岑村揽胜"感兴趣"""
        comment_lower = comment.lower()
        keywords = ['岑村揽胜', '揽胜', '路虎', 'land rover', 'range rover', '感兴趣', '想买', '好看', '不错', '喜欢']
        
        interested = False
        reason = ""
        
        if any(keyword in comment for keyword in keywords):
            interested = True
            reason = "评论中提到了相关关键词"
        
        return interested, reason
    
    def export_to_excel(self, posts, filename="xiaohongshu_data.xlsx"):
        """导出数据到Excel"""
        rows = []
        
        for post in posts:
            for comment in post.get("comments", []):
                rows.append({
                    "帖子ID": post.get("post_id"),
                    "帖子标题": post.get("title"),
                    "帖子内容": post.get("content"),
                    "评论者ID": comment.get("user_id"),
                    "评论者昵称": comment.get("nickname"),
                    "评论内容": comment.get("content"),
                    "评论时间": comment.get("time"),
                    "是否感兴趣": comment.get("interested"),
                    "思考原因": comment.get("reason")
                })
        
        df = pd.DataFrame(rows)
        df.to_excel(filename, index=False)
        print(f"数据已导出到 {filename}")
    
    def run(self, keyword="岑村揽胜", max_posts=10):
        """运行完整流程"""
        try:
            self.start_driver()
            self.login()
            self.search(keyword)
            self.sort_by_time()
            posts = self.get_posts(max_posts)
            self.export_to_excel(posts)
            print(f"共抓取 {len(posts)} 个帖子")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = XiaohongshuScraper()
    scraper.run()
