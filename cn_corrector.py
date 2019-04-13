import kenlm
import torch
from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM

from utils import get_chinese_char_sets, get_sim_word_by_prounciation, edit1, get_sim_pronunciation


class Corrector():
    def __init__(self, ngram_model="people_chars_lm.klm", special_file="movies.txt"):
        """
        ngram模型来自pycorrector，也可以自己用Kenlm训练更大的模型，效果更好。
        """
        self.vocab = get_chinese_char_sets()
        if special_file:
            self.special_words = open(special_file, 'r', encoding="utf-8").read().split("\n")
        self.ngram = kenlm.Model(ngram_model)

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        self.model = BertForMaskedLM.from_pretrained('bert-base-chinese').cuda()
        self.model.eval()
    
    def get_ppl(self, sentence):
        return self.ngram.perplexity(sentence)

    def correct_special_word(self, word, mode="ed"):
        """
        mode只能为"ed"，或者"pinyin"
        寻找候选词有两种方式，一种是通过编辑距离，mode为"ed"，错误类型并不限定，但是速度较慢，另一种是通过音近字，mode为"pinyin"。
        错误类型限定为音近字
        """
        
        def get_sim_word(w):
            if mode == "ed":
                return edit1(w, self.vocab)
            elif mode == "pinyin":
                return get_sim_word_by_prounciation(w, self.vocab)
            else:
                raise Exception("mode不正确")
        
        if word in self.special_words:
            return word
        else:
            for candidate_word in get_sim_word(word):
                if candidate_word in self.special_words:
                    return candidate_word
        return word

    def correct_sentence(self, sentence, threshold=1.1):
        """
        用ngram模型纠正一句话。
        """
        ppl_sen = {}
        org_ppl = self.get_ppl(" ".join(sentence))
        candidate_sentences = get_sim_word_by_prounciation(sentence, self.vocab)
        for candidate_sen in candidate_sentences:
            ppl_sen[self.get_ppl(" ".join(candidate_sen))] = candidate_sen
        min_candidate_ppl = min(list(ppl_sen.keys()))
        if min_candidate_ppl * threshold < org_ppl:
            for i, o, c in zip(range(len(sentence)), sentence, ppl_sen[min_candidate_ppl]):
                if o != c:
                    return [i, c]
        else:
            return []

    def predict_mask(self, sentence, error_id):
        """
        用Bert进行mask预测
        sentence:  句子
        error_id:  mask的位置
        返回 前5个最有可能的字
        """
        text = "[CLS] "+" ".join(sentence)+" [SEP]"
        tokenized_text = self.tokenizer.tokenize(text)
        tokenized_text[error_id] = '[MASK]'

        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segments_ids = [0 for _ in range(len(sentence)+2)]

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        tokens_tensor = tokens_tensor.cuda()
        segments_tensors = segments_tensors.cuda()

        with torch.no_grad():
            predictions = self.model(tokens_tensor, segments_tensors)
        predicted_index = torch.topk(predictions[0, error_id], 5)[1].cpu().numpy()
        list_mask_items = []
        for i in predicted_index:
            predicted_token = self.tokenizer.convert_ids_to_tokens([i])[0]
            list_mask_items.append(predicted_token)
        return list_mask_items

    def correct_with_bert(self, sentence):
        """
        用bert的mask prediction预测一句话
        """
        correct_result = []
        for i, char in enumerate(sentence):
            org_char_pinyin = get_sim_pronunciation(char)
            list_maybe_right = self.predict_mask(sentence, i+1)
            for c in list_maybe_right:
                if get_sim_pronunciation(c) == org_char_pinyin:
                    if c != char:
                        correct_result.append([i, c])
                    break
        return correct_result




    
