from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from difflib import SequenceMatcher
import utils


model = joblib.load('categoriser_model.pkl')
scaler = joblib.load('min_max_scaler.pkl')


features = np.array(["same_mcc_group", "merchant_name_similarity", "merchant_name_shared_words",
            "merchant_name_longest_substring", "reference_text_similarity", "reference_text_shared_words",
            "reference_text_longest_substring"])


class transaction:
    def __init__(self, mcc, merchantName, referenceText):
        self.mcc = mcc
        self.merchantName = merchantName
        self.referenceText = referenceText


def is_same_mcc_group(g1, g2):
    if g1 == g2:
        return 1
    else:
        return 0


def similarity(s1, s2):
    seqmatch = SequenceMatcher(None, s1, s2)
    return seqmatch.ratio()


def shared_words(s1, s2):
    return utils.num_same_words(s1, s2)


def longest_substring(s1, s2):
    return utils.longest_substring(s1, s2)


def transactionSimilarity(t1, t2):
    X = [
        is_same_mcc_group(t1.mcc, t2.mcc),
        similarity(t1.merchantName, t2.merchantName),
        shared_words(t1.merchantName, t2.merchantName),
        longest_substring(t1.merchantName, t2.merchantName),
        similarity(t1.referenceText, t2.referenceText),
        shared_words(t1.referenceText, t2.referenceText),
        longest_substring(t1.referenceText, t2.referenceText)
    ]
    scaledX = MinMaxScaler.transform(scaler, X).astype(np.float)
    return GradientBoostingRegressor.predict(model, scaledX)