import json


class SensitiveWordCheck:
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '/x00'  # 限定
        self.path = "./sensitiveword.json"
        self.parse(self.path)

    def add(self, keyword):
        keyword = keyword.lower()
        if not keyword:
            return
        level = self.keyword_chains

        for i in range(len(keyword)):
            if keyword[i] in level:
                level = level[keyword[i]]
            else:
                for j in range(i, len(keyword)):
                    level[keyword[j]] = {}
                    level = level[keyword[j]]
                level[self.delimit] = 0
                break
            if i == len(keyword) - 1:
                level[self.delimit] = 0
        
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(self.keyword_chains, f)
        
    def parse(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        self.keyword_chains = json_data
        # print(self.keyword_chains)
    
    def filter(self, message, repl='*'):
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            start += 1
        return ''.join(ret)

    def search(self, message):
        message = message.lower()
        # print(message)
        start = 0
        while start < len(message):
            level = self.keyword_chains
            for char in message[start:]:
                if char in level:
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        return True
                else:
                    break
            start += 1
        return False

    def delete(self, message):
        message = message.lower()
        if not self.search(message):
            return False
        level = self.keyword_chains
        for i in range(len(message)):
            level = level[message[i]]
        del level[self.delimit]
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(self.keyword_chains, f)
        return True
