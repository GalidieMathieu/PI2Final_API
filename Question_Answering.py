from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import nltk
from Pipelines.Pipelines_fr import pipeline_fr
from Pipelines.Pipelines_en import pipeline_en

nlp_en = pipeline_en("question-generation")
nlp_fr = pipeline_fr("multitask-qa-qg")


class DataSingleton:
    __instance = None
    __nlp_fr = None
    __nlp_en = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DataSingleton.__instance is None:
            DataSingleton()
        return DataSingleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DataSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DataSingleton.__instance = self
            __nlp_en = pipeline_en("question-generation")
            __nlp_fr = pipeline_fr("multitask-qa-qg")

    def getNlp_fr(self):
        return self.__nlp_fr

    def getNlp_en(self):
        return self.__nlp_en


# return all possible question on a text
class Question_Answering:

    def getQuestion(text):
        texteDecouper = Question_Answering.decouperTexte(text)
        langue = Language.getLanguage(texteDecouper[0])
        print(langue)
        nlp = Question_Answering.language(langue)
        _liste_question = []
        for texte in texteDecouper:
            result = nlp(texte)
            for reponse in result:
                _liste_question.append(reponse)
        return _liste_question

    def language(langue):
        if langue == "english":
            return nlp_en
        if langue == "french":
            return nlp_fr

    """
    
    """
    def decouperTexte(txt):
        tokenized_sentence = nltk.sent_tokenize(txt)
        # Taille actuelle de one_input
        compteur = 0
        # résultat final
        all_inputs = []
        # Une entrée du transformers, i.e une ou plusieurs pharses d'au total 511 caractères ou moins
        one_input = ""
        # Pour chaque phrase
        for sentence in tokenized_sentence:
            # On récupère la taille de la phrase
            sentence_size = len(sentence)
            # Si la phrase à elle seule fait plus de 512 caractères
            if sentence_size > 511:
                # Pour conserver l'ordre du texte
                # Si notre entrée actuelle n'est pas vide, on l'ajoute à la liste des entrée
                if one_input != "":
                    all_inputs.append(one_input)
                    # La nouvelle taille de la nouvelle entrée est donc de 0
                    compteur = 0
                    # Notre nouvelle entrée est vide
                    one_input = ""
                # Notre phrase trop longue est tronquée
                sentence = sentence[0:511]
                # Puis ajoutée à la liste de toutes les entrées
                all_inputs.append(sentence)
            # Sinon
            else:
                # On regarde si la taille de l'entrée établie jusque là + celle de notre nouvelle phrase est inférieure à 512
                if compteur + sentence_size < 511:
                    # Si oui la nouvelle dimension de notre entrée est déterminée
                    compteur += sentence_size
                    # On ajpoute la phrase à notre entrée
                    one_input += sentence
                # Sinon
                else:
                    # Si on ajoute la phrase à notre entrée, on dépasse les 512 caractères
                    # On ajoute donc notre entrée actuelle à la liste de toutes les entrées
                    all_inputs.append(one_input)
                    # Notre nouvelle entrée actuelle devient la phrase sentence
                    one_input = sentence
                    # La nouvelle taille est la taile de la phrase sentence
                    compteur = sentence_size
        # Il faut ajouter à la fin la dernière entrée si elle existe
        if one_input != "":
            all_inputs.append(one_input)
        return all_inputs


# check the language
class Language:
    def calc_ratios(text):
        ratios = {}
        tokens = wordpunct_tokenize(text)
        words = [word.lower() for word in tokens]
        for lang in stopwords.fileids():
            stopwords_set = set(stopwords.words(lang))
            words_set = set(words)
            common_words = words_set.intersection(stopwords_set)
            ratios[lang] = len(common_words)

        return ratios

    def detect_language(text):
        ratios = Language.calc_ratios(text)
        most_rated_language = max(ratios, key=ratios.get)
        return most_rated_language

    def getLanguage(text):
        return str(Language.detect_language(text))
