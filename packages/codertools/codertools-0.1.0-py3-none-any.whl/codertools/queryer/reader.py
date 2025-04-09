import os
from llama_index.readers.github import GithubRepositoryReader, GithubClient

from llama_index.readers.github import (
    GitHubRepositoryIssuesReader,
    GitHubIssuesClient,
)

def read_github_issue(owner="pydantic",repo="pydantic",state=None,labelFilters = None):
    github_client = GitHubIssuesClient(github_token=os.environ["GITHUB_TOKEN"], verbose=True)

    reader = GitHubRepositoryIssuesReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        verbose=True,
    )


    documents = reader.load_data(
        state=state or GitHubRepositoryIssuesReader.IssueState.OPEN,# GitHubRepositoryIssuesReader.IssueState.OPEN or .CLOSED or .ALL
        labelFilters= labelFilters or [("bug V2", GitHubRepositoryIssuesReader.FilterType.INCLUDE)], # 根据标签过滤
    )
    return documents



def read_github_repo(owner="pydantic",repo="pydantic",filter_directories=None,
                    filter_file_extensions = None,branch="main"):
    github_client = GithubClient(github_token=os.environ["GITHUB_TOKEN"], verbose=False)

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=False,
        verbose=False,
        filter_directories=filter_directories or (
            ["docs/concepts"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
        filter_file_extensions=filter_file_extensions or (
            [
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