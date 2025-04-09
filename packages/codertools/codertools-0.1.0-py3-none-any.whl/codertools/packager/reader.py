import os
from llama_index.readers.github import GithubRepositoryReader, GithubClient

from llama_index.readers.github import (
    GitHubRepositoryIssuesReader,
    GitHubIssuesClient,
)


def read_github_repo(owner:str="pydantic",
                     repo:str="pydantic",
                     branch:str="main",
                     filter_directories:list=None,
                     filter_file_extensions:list = None
                     ):
    """
    读取github仓库中的文档或者其他文件内容   
    owner: str 作者   
    repo: str 仓库名   
    branch : 分支   
    filter_directories: 按照文件夹筛选(包含)  ["docs/concepts"]   
    filter_file_extensions: 按照文件类型筛选 (排除)   

    """
    github_client = GithubClient(github_token=os.environ["GITHUB_TOKEN"], verbose=False)

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=False,
        verbose=False,
        filter_directories=(
            filter_directories or ["docs/concepts"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
        filter_file_extensions=(
            filter_file_extensions or [
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".svg",
                ".ico",
                "json",
                ".ipynb",
            ],
            GithubRepositoryReader.FilterType.EXCLUDE,
        ),
    )

    documents = reader.load_data(branch=branch)
    return documents


def read_github_issue(owner:str="pydantic",
                      repo:str="pydantic",
                      state:GitHubRepositoryIssuesReader.IssueState=None,
                      labelFilter:list = None)->'documents':
    """
    读取github仓库中的 issue 问题集   
    owner: str 作者
    repo: str 仓库名
    state : 仓库状态 state or GitHubRepositoryIssuesReader.IssueState.CLOSED,# GitHubRepositoryIssuesReader.IssueState.OPEN or .CLOSED or .ALL
    labelFilters: 按照标签筛选内容 暂未开放
    """
    github_client = GitHubIssuesClient(github_token=os.environ["GITHUB_TOKEN"], verbose=True)

    reader = GitHubRepositoryIssuesReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        verbose=True,
    )


    documents = reader.load_data(
        state=state or GitHubRepositoryIssuesReader.IssueState.CLOSED,# GitHubRepositoryIssuesReader.IssueState.OPEN or .CLOSED or .ALL
        #labelFilters= labelFilters or [("bug V2", GitHubRepositoryIssuesReader.FilterType.INCLUDE)], # 根据标签过滤
    )
    return documents


