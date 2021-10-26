---
title: git 常用操作流程实现
tags: [Git]
categories: [Blog]
index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
date: 2021-10-10 08:00:00
hide: false
---

## 一. 基础git命令

### 1. 身份设置实现: `git config`

```bash
git config --global user.name "Your name"  
git config --global user.email "Your email"
```

### 2. 版本查看实现: `git version`

```bash
git version
```

### 3. 储存库初始化实现: `git init`

```bash
$ git init
或者
$ git init <your repository name>
```

### 4. 储存库克隆: `git clone`

```bash
git clone <your project URL>
```

### 5. 储存库文件添加: `git add`

```bash
$ git add your_file_name
or
$ git add *         # 此命令添加所有修改过的文件
```

### 6. 将更改添加到本地储存库: `git commit`

```bash
git commit -m 'your useful commit message'
```

### 7. 查看需要关注的文件: `git status`

```bash
git status
```

### 8. 分支管理: `git branch`

- 列出本地所有分支

```bash
git branch
```

- 列出云端所有分支

```bash
git branch -a
```

- 创建新的分支

```bash
git branch <branch_name>
```

- 删除分支

```bash
git branch -d <branch_name>
```

### 9. 分支切换: `git checkout`

```bash
git checkout <branch_name>
```

- 创建检出分支

```bash
git checkout -b <your_new_branch_name>
```

## 二. 中级git命令

### 1. 远程连接: `git remote`

- 将本地储存库连接到远程

```bash
git remote add <shortname> <url>
```

- 样例

```bash
git remote add origin https;//gitee.com/you_git_name
```

### 2. 远程推送: `git push`

```bash
git push -u <short_name> <your_branch_name>
```

### 3. 远程设置: `git push --set-upstream`

> 在使用 git push 之前，我们应先设置好origin和upstream。

```bash
git push --set-upstream <short_name> <your_branch_name>
```

### 4. 下载更改: `git fetch`

> 当下载其他团队成员的更改时，就得使用`git fetch`  
> 此命令会下载有关提交，引用等所有信息，因此你可以在将这些更改应用于本地储存库之前对其进行检查。

```bash
git fetch
```

### 5. 更新本地储存库: `git pull`

> `git pull` 会将所有最新的内容更新到本地储存库

```bash
git pull <remote_url>
```

### 6. 临时储存已修改文件: `git stash`

- 用法

```bash
git stash
```

- 查看所有stash

```bash
git stash list
```

- 应用stash到分支

```bash
git stash apply
```

### 7. `git log`

> 在git log的帮助下，你可以看到所有之前的提交，并且最近的提交出现在最前面。

- 用法

```bash
git log
```

> 默认情况下，它将显示当前已检出分支的所有提交，但是你可以强制通过所有选项来查看所有分支的所有提交。

```bash
git log --all
```

### 8. `git shortlog`

> git shortlog命令会显示来自git log命令的摘要。如果你只对简短的摘要感兴趣，那么此命令就非常有用了。
这个命令有助于查看谁处理了什么，因为它对作者及其提交进行了分组。

- 用法

```bash
git shortlog
```

### 9. `git show`

> 与git log相比，此命令将显示有关特定提交的详细信息。

- 用法

```bash
git show <your_commit_hash>
```

### 10. `git rm`

> 有时你需要从代码库中删除文件，在这种情况下，可以使用git rm命令。
它可以从索引和工作目录中删除跟踪的文件。

- 用法

```bash
git rm <your_file_name>
```

### 11. `git merge`

> git merge可帮助将来自两个分支的更改集成到单个分支中。

- 用法

```bash
git merge <branch_name>
```

> 此命令会将<branch_name>合并到当前你选择的分支中。

<font color='#ff0000' face='楷体' size=5>注: 我们可以使用此命令实现合并内容到自己分支。</font>

## 三. 高级Git命令

### 1. `git rebase`

> git rebase类似于git merge命令。它把两个分支集成到一个分支中，但有一个不一样的地方：git rebase命令将会重写提交记录。
当你有多个私有分支合并到单个分支时，应使用git rebase命令。它将使得提交历史成为线性的。

- 用法

```bash
git rebase <base>
```

### 2. `git bisect`

> git bisect命令可帮助查找糟糕的提交。

- 用法

1. 启动git bisect

```bash
git bisect start
```

1. 让git bisect知道什么是好的提交

```bash
git bisect good a123
```

1. 让git bisect知道什么是糟糕的提交

```bash
git bisect bad z123
```

> 通过git bisect，只要几分钟你就可以缩小问题代码的范围。

### 3. `git cherry-pick`

> git cherry-pick是一个蛮有用的命令，允许你从任意分支中选择任意提交并将其应用于其他任意分支。

- 用法

```bash
git cherry-pick <commit-hash>
```

> git cherry-pick不会修改存储库的历史记录；相反，它会添加到历史记录。

### 4. `git archive`

> git archive命令会把多个文件合并为单个文件。就好像zip实用程序一样，所以你可以提取存档文件以获取单个文件。

- 用法

```bash
git archive --format zip HEAD > archive-HEAD.zip
```

> 它将创建当前修订的zip存档。

### 5. `git pull --rebase`

> 在大多数情况下，当你使用git pull时，你需要重新设置基准（并且不进行合并）。
此时，你就可以使用此选项。

- 用法

```bash
git pull --rebase
```

> 这将帮助保持干净的历史记录。另外，还可以避免多次合并。

### 6. `git blame`

> 如果你需要逐行检查任意文件的内容，则需要使用git blame命令。它可以帮助确定是谁对文件进行了更改。

- 用法

```bash
git blame <your_file_name>
```

### 7. `git tag`

> 在Git中，标签很有用，你可以使用它们来管理发布。你可以将git tag视为不会改变的分支。尤其是要公开发布的时候，则更为重要了。

- 用法

```bash
git tag -a v1.0.0
```

### 8. `git verify-commit`

> git verify-commit命令将检查gpg签名。GPG，GNU Privacy Guard，是sign文件中使用的工具，包含签名。

- 用法

```bash
git verify-commit <commit>
```

### 9. `git verify-tag`

> 可以以同样的方式确认标签。

- 用法

```bash
git verify-tag <tag>
```

### 10. `git diff`

> 大多数情况下，在提交或推送之前，你需要比较两个git文件或分支。用这个命令就方便多了。

- 用法

1. 将工作目录与本地存储库进行比较：

```bash
git diff HEAD <filename>
```

1. 比较两个分支：

```bash
git diff <source branch> <target branch>
```

### 11. `git citool`

> git citool是Git提交的图形化替代。

- 用法

```bash
git citool
```

### 12. `git mv`

> 重命名git文件。接受两个参数，源文件名和目标文件名。

- 用法

```bash
git mv <old-file-name> <new-file-name>
```

### 13. `git clean`

> 你可以使用git clean命令处理未跟踪的文件。可以使用此命令从工作目录中删除所有未跟踪的文件。如果要处理跟踪的文件，则需要使用git reset命令。

- 用法

```bash
git clean
```

### 14. `git help`

> Git中有许多命令，如果你需要其他命令的帮助，则可以随时在终端上使用git help。

- 用法

```bash
git help <git_command>
```

### 15. `git whatchanged`

> 此命令的作用与git log相同，但为原始格式。并且由于历史原因，它也是git的一份子。

- 用法

```bash
git whatchanged
```
