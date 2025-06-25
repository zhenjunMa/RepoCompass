from gitingest import ingest
from git import Repo

from src.tools.file import tree


def ingest_test():
    summary, tree, content = ingest("https://github.com/mosn/layotto",
                                    exclude_patterns="*.css,*.js,*.rs,*.ts,*.wasm,*.toml,*.java,*.c,*.go,*.env,*.json,*.yaml,*.yml,*.sh,*.proto,*.sum,*.mod,*.mk,*.conf")
    # summary, tree, content = ingest("/go/layotto", include_patterns="*.md")
    # print(summary)
    # print(tree)
    print(content)


def git_test():
    Repo.clone_from("https://github.com/mosn/layotto", "/Users/gujin/workspace/python/RepoCompass/layotto")



if __name__ == '__main__':
    # ingest_test()
    git_test()