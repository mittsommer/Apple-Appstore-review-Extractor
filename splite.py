import MeCab
def splite(review):
    review_splite = []
    for i in range(len(review)):
        mecab_tagger = MeCab.Tagger("-Owakati")
        rs = mecab_tagger.parse(review[i])
        review_splite.append(rs)
    return review_splite
