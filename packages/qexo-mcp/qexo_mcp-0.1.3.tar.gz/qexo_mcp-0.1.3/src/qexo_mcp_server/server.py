from typing import Optional, List
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
import requests
import os
import time
from pathlib import Path

# 创建MCP服务器
mcp = FastMCP(
    "Qexo CMS",
    description="连接到Qexo API并提供搜索、管理和改进功能的MCP服务器",
)

@dataclass
class QexoConfig():
    """Configuration for Qexo API"""
    api_url: str
    api_token: str

class QexoMCPServer():
    def __init__(self, config: QexoConfig):
        super().__init__()
        self.config = config

    def _make_request(self, method: str, endpoint: str, params: dict, data: dict) -> dict:
        response = requests.request(
            method,
            f"{self.config.api_url}/{endpoint}",
            params={
                "token": self.config.api_token,
                **params
            },
            data={
                **data
            }
        )
        print('response.status_code', response.status_code)
        return response.json()
    
    def get_posts(self, s: str = None) -> List[dict]:
        """Get posts from Qexo
        
        Args:
            s: Search string
        """
        return self._make_request(
            "POST",
            "pub/get_posts/",
            {
                "s": s,
            },{}
        )
    
    def save_file(self, file: str, content: str,commitchange:str =None) -> dict:
        """Save a file to Qexo
        
        Args:
            file: File path
            content: File content
        """
        return self._make_request(
            "POST",
            "pub/save/",
            {},
            {
                "file": file,
                "content": content,
                "commitchange": commitchange if commitchange else f"Update {file} by Qexo"
            }
        )
    
    def new_file(self, file: str, content: str) -> dict:
        """Create a new file in Qexo
        
        Args:
            file: File path
            content: File content
        """
        return self._make_request(
            "POST",
            "pub/new/",
            {},
            {
                "file": file,
                "content": content
            }
        )

    
    def delete_file(self, file: str) -> dict:
        """Delete a file from Qexo
        
        Args:
            file: File path
        """
        return self._make_request(
            "POST",
            "pub/delete/",
            {},
            {
                "file": file
            }
        )

    
    def delete_post(self, file: str) -> dict:
        """Delete a post from Qexo
        
        Args:
            file: Post name
        """
        return self._make_request(
            "POST",
            "pub/delete_post/",
            {},
            {
                "file": file
            }
        )



# 获取Qexo配置
def get_config() -> QexoConfig:
    from dotenv import load_dotenv
    load_dotenv()

    # 首先尝试从环境变量获取
    api_url = os.getenv("api_url")
    api_token = os.getenv("api_token") 
    

    if not api_url or not api_token:
        print("错误: 请在环境变量中设置api_url和api_token")
        exit(1)
    
    return QexoConfig(
        api_url=api_url,
        api_token=api_token
    )

config = get_config()
client = QexoMCPServer(config)


@mcp.tool()
def get_posts(s: str = None) -> List[dict]:
    """Get all posts"""
    return client.get_posts(s)

@mcp.tool()
def save_or_update_file(file: str, content: str) -> dict:
    """Save a file to Qexo
    
    Args:
        file: File path
        content: File content
    """
    return client.save_file(file, content)




def format_post_content( title,content, categories: List[str], tags: List[str]):
    template = """---
title: {}
categories: {}
tags: {}
date: {}
---

{}
""" 
    
    categories_str = ""
    tags_str = ""
    if categories:
        if len(categories) > 1:
            categories_str = "\n - "+"\n - ".join(categories)
        else:
            categories_str = categories[0]
    if tags:
        if len(tags) > 1:
            tags_str = "\n - "+"\n - ".join(tags)
        else:
            tags_str = tags[0]
    return template.format(
        title,
        categories_str,
        tags_str,
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        content
    )
    

def get_post_file_path(title):
    return "source/_posts/"+title+".md"

@mcp.tool()
def save_or_update_post(title: str, content: str, categories: List[str]=[], tags: List[str]=[],commitchange:str =None) -> dict:
    """Save or update a post to Qexo
    Args:
        title: Post title
        content: Post content
        categories: List of categories
        tags: List of tags
        commitchange: Commit message
    """
    content=format_post_content(title, content, categories, tags)
    return client.save_file(get_post_file_path(title), content,commitchange)


@mcp.tool()
def delete_post(title: str) -> dict:
    """Delete a post from Qexo
    
    Args:
        title: Post title
    """
    return client.delete_file(get_post_file_path(title))



def main():
    print("Qexo MCP Server starting...")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # main()
    # print(format_post_content("test2", "test", ["test1","test3"],[]))
    save_or_update_post("test3333", "test这是测试文本", ["test"], ["test","test1"],"这是测试提交")
    # delete_post("test3333")