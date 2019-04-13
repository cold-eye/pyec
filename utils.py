from pypinyin import lazy_pinyin


def edit1(word, char_sets):
    """
    寻找编辑距离为1的所有词
    """
    candidate_sets = []
    for idx in range(len(word)):  # 替换
        for char in char_sets :
            candidate_sets.append(word[:idx] + char + word[idx + 1:])

    for idx in range(len(word) + 1):  # 增加
        for char in char_sets:
            candidate_sets.append(word[:idx] + char + word[idx:])

    for idx in range(len(word)):  # 删除
        candidate_sets.append(word[:idx] + word[idx + 1:])

    for idx in range(len(word) - 1):  # 颠倒
        candidate_sets.append(word[:idx] + word[idx + 1] + word[idx] + word[idx + 2:])

    return set(candidate_sets)

def edit2(word, char_sets):
    """
    寻找编辑距离为2的所有词，思路来自http://norvig.com/spell-correct.html
    """
    return set([e2 for d1 in edit1(word, char_sets) for e2 in edit1(word, char_sets)])


def get_chinese_char_sets():
    """
    得到5000常用汉字，来自https://github.com/howiehu/commonly-used-chinese-characters
    """
    return set(list(open("chinese_5039.txt", 'r', encoding="utf-8").read().strip()))


def get_sim_pronunciation(char):
    """
    得到某个中文汉字的音近字，
    不能处理多音字的情况，因为pypinyin的原因，多音字容易产生很多古汉语的歧义字
    """
    pronunciation = lazy_pinyin(char)[0]
    if "zh" in pronunciation or "ch" in pronunciation or "sh" in pronunciation or "ng" in pronunciation:
        pronunciation = pronunciation.replace("zh", "z").replace("ch", "c").replace("sh", "s").replace("ng", "n")
    return pronunciation

def get_sim_word_by_prounciation(word, char_sets):
    """
    参数word并不限于单词，
    由相似拼音得到候选集
    """
    sim_words = []
    for i, char in enumerate(word):
        org_pron = get_sim_pronunciation(char)
        for c in char_sets:
            if org_pron == get_sim_pronunciation(c):
                sim_words.append(word[:i]+c+word[i+1:])
    sim_words.remove(word)
    return set(sim_words)







