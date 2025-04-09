import os
import pickle
import pkg_resources


class KhmerWordLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/wild_khmer_data.pkl')
        else:
            self.filepath = filepath
        self.words = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Word file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_words(self):
        return self.words

    def __len__(self):
        return len(self.words)

    def get_first_word(self):
        return self.words[0] if self.words else None

    def get_n_first_words(self, n=5):
        return self.words[:n]

    def find_word(self, word):
        return word in self.words


class KhmerAddressLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/address_kh_data.pkl')
        else:
            self.filepath = filepath
        self.addresses = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Address file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_addresses(self):
        return self.addresses

    def __len__(self):
        return len(self.addresses)

    def get_first_address(self):
        return self.addresses[0] if self.addresses else None

    def get_n_first_addresses(self, n=5):
        return self.addresses[:n]

    def find_address(self, address):
        return address in self.addresses


class KhmerSentencesLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/wild_khmer_sentences.pkl')
        else:
            self.filepath = filepath
        self.sentences = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Sentence file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_sentences(self):
        return self.sentences

    def __len__(self):
        return len(self.sentences)

    def get_first_sentence(self):
        return self.sentences[0] if self.sentences else None

    def get_n_first_sentences(self, n=5):
        return self.sentences[:n]

    def find_sentence(self, sentence):
        return sentence in self.sentences
